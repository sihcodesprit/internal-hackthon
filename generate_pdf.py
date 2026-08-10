import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

def generate_pdf():
    pdf_path = "SmartCurriculum_Design_Document.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=letter,
                            rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54)
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#1A1A2E'),
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#6C63FF'),
        spaceAfter=25
    )
    
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontSize=16,
        leading=20,
        textColor=colors.HexColor('#1A1A2E'),
        spaceBefore=15,
        spaceAfter=10,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['BodyText'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#333333'),
        spaceAfter=10
    )

    code_style = ParagraphStyle(
        'CodeText',
        parent=styles['Code'],
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=8
    )

    story = []
    
    # Document Header
    story.append(Paragraph("Smart Curriculum Activity & Attendance", title_style))
    story.append(Paragraph("System Architecture & Solution Design Document (SIH 2026)", subtitle_style))
    story.append(Spacer(1, 10))
    
    # Executive Summary
    story.append(Paragraph("1. Executive Summary", h1_style))
    story.append(Paragraph(
        "The Smart Curriculum Activity & Attendance Web Application is a lightweight, responsive Django-based prototype "
        "designed to eliminate classroom administration overhead while optimizing students' empty periods. Through QR code "
        "verification, automated timetable parsing, and dynamic resource suggestions, it converts passive free time into active learning periods.",
        body_style
    ))
    story.append(Spacer(1, 10))
    
    # System Architecture
    story.append(Paragraph("2. Architecture & Design Patterns", h1_style))
    story.append(Paragraph(
        "The application utilizes Django's Model-View-Template (MVT) architecture for the backend. "
        "The frontend is decoupled with dynamic styling systems built using Vanilla CSS and Client-side jsQR library interfaces.",
        body_style
    ))
    story.append(Spacer(1, 10))
    
    # Database Schema
    story.append(Paragraph("3. Core Database Tables", h1_style))
    
    tables_info = [
        ("accounts_customuser", "Stores student/teacher metadata (department, roll number, section, role)."),
        ("attendance_subject", "Stores academic subject titles, unique course codes, and credits."),
        ("attendance_class", "Maps teachers to classrooms and enrolled students."),
        ("attendance_attendancesession", "UUID-identified QR attendance windows with expiration markers."),
        ("attendance_attendancerecord", "Tracks marked attendance metrics, IP address, and marking timestamps."),
        ("timetable_timeslot", "Stores weekly schedule entries, categorizing classes and free periods."),
        ("timetable_tasksuggestion", "Holds academic work recommendations categorized by priority and subject."),
        ("timetable_dailyplanner", "Student planner tracker logging completed tasks and custom daily notes.")
    ]
    
    table_data = [[Paragraph("<b>Table Name</b>", body_style), Paragraph("<b>Description</b>", body_style)]]
    for name, desc in tables_info:
        table_data.append([Paragraph(f"<code>{name}</code>", code_style), Paragraph(desc, body_style)])
        
    t = Table(table_data, colWidths=[2.2 * inch, 4.3 * inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#EEEEEE')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#DDDDDD')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))
    
    # Modules
    story.append(Paragraph("4. Key Modules & Features", h1_style))
    story.append(Paragraph(
        "<b>• Authentication Module:</b> Secure role-based login interfaces redirecting users automatically to dedicated Teacher/Student analytics portals.<br/>"
        "<b>• QR Code Attendance:</b> Automatic active session generation with countdown expirations. Students can upload or drop saved QR image files or mark directly using live webcams.<br/>"
        "<b>• Timetable & Planner:</b> Automatically detects free periods throughout the day and auto-suggests context-aware tasks linked to active courses.<br/>"
        "<b>• Analytics:</b> Visualization dashboard featuring line charts (daily trends), donut gauges, and a warning log flagging students falling under the required 75% attendance threshold.",
        body_style
    ))
    
    doc.build(story)
    print("PDF Generated successfully: SmartCurriculum_Design_Document.pdf")

if __name__ == "__main__":
    generate_pdf()
