from io import BytesIO 
import xhtml2pdf.pisa as pisa

def html_to_pdf(html):
    result = BytesIO()
    pdf = pisa.CreatePDF(BytesIO(html.encode("utf-8")), result, encoding='utf-8')
    return pdf, result