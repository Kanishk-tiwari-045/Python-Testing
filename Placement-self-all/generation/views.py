# views.py
from django.shortcuts import render
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from .models import Details

def generate_pdf(request):
    email = input("Enter the email address of the user: ")
    if email:
        try:
            user_detail = Details.objects.get(email=email)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{email}_resume.pdf"'
            doc = SimpleDocTemplate(response, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
            elements = []
            styles = getSampleStyleSheet()
            
            title_style = ParagraphStyle(
                'TitleStyle',
                parent=styles['Heading1'],
                fontSize=28,
                alignment=1,
                spaceAfter=20,
                textColor=colors.HexColor('#003366')
            )
            header_style = ParagraphStyle(
                'HeaderStyle',
                parent=styles['Heading2'],
                fontSize=16,
                textColor=colors.HexColor('#003366'),
                spaceAfter=12,
                spaceBefore=20
            )
            normal_style = ParagraphStyle(
                'NormalStyle',
                parent=styles['Normal'],
                fontSize=12,
                leading=16
            )
            bold_style = ParagraphStyle(
                'BoldStyle',
                parent=styles['Normal'],
                fontSize=12,
                leading=16,
                textColor=colors.HexColor('#003366'),
                spaceAfter=6
            )
            title = Paragraph("Personal Profile", title_style)
            elements.append(title)

            elements.append(Paragraph(f"Name: {user_detail.first_name} {user_detail.last_name}", bold_style))
            elements.append(Paragraph(f"Email: {user_detail.email}", normal_style))
            elements.append(Paragraph(f"Phone Number: {user_detail.phone_number}", normal_style))
            elements.append(Paragraph(f"Address: {user_detail.address}", normal_style))
            elements.append(Spacer(1, 20))

            elements.append(Paragraph("Work Experience", header_style))
            elements.append(Paragraph(f"Title: {user_detail.title}", bold_style))
            elements.append(Paragraph(f"Tech Stack: {user_detail.techstack}", normal_style))
            elements.append(Paragraph(f"Company: {user_detail.company}", normal_style))
            elements.append(Spacer(1, 20))

            elements.append(Paragraph("Education", header_style))
            elements.append(Paragraph(f"Degree: {user_detail.degree}", bold_style))
            elements.append(Paragraph(f"Field of Study: {user_detail.field_of_study}", normal_style))
            elements.append(Paragraph(f"School: {user_detail.school}", normal_style))
            elements.append(Spacer(1, 20))

            doc.build(elements)
            return response
        
        except Details.DoesNotExist:
            return HttpResponse("User not found.")
    else:
        return HttpResponse("Please provide an email address.")
