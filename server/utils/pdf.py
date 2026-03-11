from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def render_text_to_pdf_stream(text: str, filename: str = "document.pdf"):
    """Render text to PDF stream"""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    margin_x, margin_top, margin_bottom = 72, 72, 72
    
    def new_textobject():
        t = c.beginText(margin_x, height - margin_top)
        t.setLeading(14)
        return t
    
    t = new_textobject()
    for line in (text or "").splitlines() or [""]:
        if t.getY() <= margin_bottom:
            c.drawText(t)
            c.showPage()
            t = new_textobject()
        t.textLine(line)
    
    c.drawText(t)
    c.showPage()
    c.save()
    buffer.seek(0)
    
    headers = {"Content-Disposition": f"attachment; filename={filename}"}
    return buffer, headers