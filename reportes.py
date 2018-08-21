from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from os import startfile

pdfmetrics.registerFont(TTFont('Calibri', 'assets\\fonts\\calibri.ttf'))
pdfmetrics.registerFont(TTFont('CalibriB', 'assets\\fonts\\calibrib.ttf'))
pdfmetrics.registerFont(TTFont('Arial', 'assets\\fonts\\arial.ttf'))
pdfmetrics.registerFont(TTFont('ArialB', 'assets\\fonts\\arialbd.ttf'))

nombre_archivo = 'assets\\orden_compra.pdf'
pdf = canvas.Canvas(nombre_archivo, pagesize=letter)

pdf.drawImage('assets\\logo.png', 4.97*mm, 244.59*mm, 41.48*mm, 28.15*mm)
pdf.drawImage('assets\\name.png', 46.45*mm, 257.62*mm, 86.16*mm, 13.55*mm)


#Cabecera
pdf.setFillColor(black)
pdf.setFont('CalibriB', 14)
pdf.drawString(152.31*mm, 267.85*mm, 'Cotización')
pdf.setFont('Calibri', 14)
pdf.drawString(193*mm, 267.85*mm, '#NumCot') #Variable
pdf.setFont('CalibriB', 11)
pdf.drawString(152.31*mm, 262.71*mm, 'Fecha')
pdf.setFont('Calibri', 11)
pdf.drawString(189.63*mm, 262.71*mm, '#dd/mm/aaaa') #Variable
pdf.setFont('CalibriB', 9)
pdf.drawString(
    46*mm,
    252.55*mm,
    'Prolongación 16 de Septiembre No. 4-PA1, Col. Diligencias'
)
pdf.drawString(46*mm, 248.67*mm, 'C.P. 76020  Querétaro, Qro. México.')
pdf.drawString(
    46*mm,
    244.9*mm,
    'ventas1cimarr@gmail.com   Tel. 01 442 213 28 51'
)
pdf.setFont('Calibri', 9)
pdf.drawString(5.5*mm, 236.78*mm, '#Razón Social') #Variable
pdf.drawString(5.5*mm, 231.78*mm, '#Nombre Contacto') #Variable
pdf.drawString(5.5*mm, 226.78*mm, '#Correo Contacto') #Variable
pdf.drawString(5.5*mm, 221.78*mm, '#Tel Contacto') #Variable
pdf.drawString(5.5*mm, 216.78*mm, '#Cel Contacto') #Variable
pdf.setFont('CalibriB', 9)
pdf.drawString(141.5*mm, 236.78*mm, 'Vigencia')
pdf.drawString(141.5*mm, 231.78*mm, 'Pago')
pdf.drawString(141.5*mm, 226.78*mm, 'Moneda')
pdf.drawString(141.5*mm, 221.78*mm, 'Asesor')
pdf.drawString(141.5*mm, 216.78*mm, 'Móvil')
pdf.setFont('Calibri', 9)
pdf.drawString(163.5*mm, 236.78*mm, '#Vigencia') #Variable
pdf.drawString(163.5*mm, 231.78*mm, '#Pago') #Variable
pdf.drawString(163.5*mm, 226.78*mm, '#Moneda') #Variable
pdf.drawString(163.5*mm, 221.78*mm, '#Asesor') #Variable
pdf.drawString(163.5*mm, 216.78*mm, '#Móvil') #Variable

#Lineas para los titulos de las columnas
pdf.line(5*mm, 211.78*mm, 209.22*mm, 211.78*mm)
pdf.line(5*mm, 206.78*mm, 209.22*mm, 206.78*mm)
pdf.setFont('ArialB', 9)
pdf.drawString(11.5*mm, 208*mm, 'MODELO')
pdf.drawString(59.14*mm, 208*mm, 'DESCRIPCIÓN')


#Linea de fin de detalle
pdf.line(5*mm, 54.65*mm, 209.22*mm, 54.65*mm)

pdf.showPage()
pdf.save()
startfile(nombre_archivo)
