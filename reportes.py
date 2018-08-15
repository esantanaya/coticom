from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from os import startfile

pdfmetrics.registerFont(TTFont('Calibri', 'assets\\fonts\\calibri.ttf'))
pdfmetrics.registerFont(TTFont('CalibriB', 'assets\\fonts\\calibrib.ttf'))

nombre_archivo = 'orden_compra.pdf'
pdf = canvas.Canvas(nombre_archivo, pagesize=letter)

pdf.drawImage('assets\\logo.png', 4.97*mm, 244.59*mm, 41.48*mm, 28.15*mm)
pdf.drawImage('assets\\name.png', 46.45*mm, 257.62*mm, 86.16*mm, 13.55*mm)

pdf.setFillColor(black)
pdf.setFont('CalibriB', 14)
pdf.drawString(152.31*mm, 267.85*mm, 'Cotización')

pdf.showPage()
pdf.save()
startfile(nombre_archivo)
