from reportlab.lib import colors
from reportlab.lib.pagesizes import A3, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

def generatePdf(imageName,data1,data2,data3,data4,data5,pdfName):
    doc = SimpleDocTemplate(pdfName, pagesize=A3, rightMargin=30, leftMargin=30, topMargin=30,
                            bottomMargin=18)
    #doc.pagesize = landscape(A4)
    elements = []
    im = Image(imageName, 5 * inch, 5 * inch)
    elements.append(im)
    # TODO: Get this line right instead of just copying it from the docs
    style = TableStyle([('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
                        ('TEXTCOLOR', (1, 1), (-2, -2), colors.red),
                        ('VALIGN', (0, 0), (0, -1), 'TOP'),
                        ('TEXTCOLOR', (0, 0), (0, -1), colors.red),
                        ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
                        ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                        ('TEXTCOLOR', (0, -1), (-1, -1), colors.green),
                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.white),
                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                        ])

    # Configure style and word wrap
    s = getSampleStyleSheet()
    s = s["BodyText"]
    s.wordWrap = 'CJK'

    tableData1 = [[Paragraph(cell, s) for cell in row] for row in data1]
    tableData2 = [[Paragraph(cell, s) for cell in row] for row in data2]
    tableData3 = [[Paragraph(cell, s) for cell in row] for row in data3]
    tableData4 = [[Paragraph(cell, s) for cell in row] for row in data4]
    tableData5 = [[Paragraph(cell, s) for cell in row] for row in data5]

    t1 = Table(tableData1)
    t1.setStyle(style)

    t2 = Table(tableData2)
    t2.setStyle(style)

    t3 = Table(tableData3)
    t3.setStyle(style)

    t4 = Table(tableData4)
    t4.setStyle(style)

    t5 = Table(tableData5)
    t5.setStyle(style)

    # Send the data and build the file

    elements.append(t1)
    elements.append(Spacer(1, 10))

    elements.append(t2)
    elements.append(Spacer(1, 5))

    elements.append(t3)
    elements.append(Spacer(1, 5))

    elements.append(t4)
    elements.append(Spacer(1, 5))

    elements.append(t5)
    elements.append(Spacer(1,5))

    doc.build(elements)