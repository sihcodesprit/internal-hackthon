from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from .models import AttendanceSession, AttendanceRecord, Class


class SessionSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='class_obj.name')
    subject_name = serializers.CharField(source='class_obj.subject.name')
    present_count = serializers.SerializerMethodField()

    class Meta:
        model = AttendanceSession
        fields = ['session_id', 'class_name', 'subject_name', 'date', 'status', 'expires_at', 'present_count']

    def get_present_count(self, obj):
        return obj.records.filter(status='present').count()


class AttendanceRecordSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name')
    roll_number = serializers.CharField(source='student.roll_number')
    subject = serializers.CharField(source='session.class_obj.subject.name')

    class Meta:
        model = AttendanceRecord
        fields = ['id', 'student_name', 'roll_number', 'subject', 'status', 'marked_at']


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_mark_attendance(request):
    import json
    session_data = request.data.get('session_id', '')
    try:
        data = json.loads(session_data)
        sid = data.get('session_id')
    except (json.JSONDecodeError, TypeError):
        sid = session_data

    try:
        session = AttendanceSession.objects.get(session_id=sid)
        if not session.is_active():
            return Response({'success': False, 'message': 'Session expired.'}, status=status.HTTP_400_BAD_REQUEST)

        if not request.user.enrolled_classes.filter(pk=session.class_obj.pk).exists():
            request.user.enrolled_classes.add(session.class_obj)

        record, created = AttendanceRecord.objects.get_or_create(
            session=session, student=request.user,
            defaults={'status': 'present', 'ip_address': request.META.get('REMOTE_ADDR')}
        )
        if created:
            return Response({'success': True, 'message': f'Attendance marked for {session.class_obj.subject.name}!'})
        return Response({'success': False, 'message': 'Already marked.'}, status=status.HTTP_409_CONFLICT)
    except AttendanceSession.DoesNotExist:
        return Response({'success': False, 'message': 'Session not found.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_session_status(request, session_id):
    try:
        session = AttendanceSession.objects.get(session_id=session_id)
        records = session.records.select_related('student')
        serializer = AttendanceRecordSerializer(records, many=True)
        return Response({
            'session': SessionSerializer(session).data,
            'records': serializer.data,
            'present_count': records.filter(status='present').count(),
            'total_students': session.class_obj.students.count(),
        })
    except AttendanceSession.DoesNotExist:
        return Response({'error': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_student_attendance(request):
    if not request.user.is_student():
        return Response({'error': 'Student access only'}, status=status.HTTP_403_FORBIDDEN)
    records = AttendanceRecord.objects.filter(student=request.user).select_related('session__class_obj__subject')
    serializer = AttendanceRecordSerializer(records, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_active_sessions(request):
    if not request.user.is_student():
        return Response({'error': 'Student access only'}, status=status.HTTP_403_FORBIDDEN)
    enrolled = request.user.enrolled_classes.all()
    sessions = AttendanceSession.objects.filter(
        class_obj__in=enrolled,
        status='active'
    ).exclude(records__student=request.user)
    serializer = SessionSerializer(sessions, many=True)
    return Response(serializer.data)
