from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.utils.encoding import smart_str

def generate_invoice_pdf(order):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="invoice_{order.id}.pdf"'

    font_path = "static/fonts/NotoSans-Regular.ttf"
    pdfmetrics.registerFont(TTFont('NotoSans', font_path))

    p = canvas.Canvas(response, pagesize=letter)
    p.setFont('NotoSans', 12)

    start_x, start_y = 100, 800
    p.drawString(start_x, start_y, f'Order ID: {order.id}')

    y_position = start_y - 20

    heading = smart_str("Кассовый чек")
    p.drawString(start_x, y_position, heading)
    y_position -= 15

    for item in order.items.all():
        product_info = [
            smart_str(""),
            smart_str(f"Продукт: {item.product.name}"),
            smart_str(f"Количество: {item.quantity}"),
            smart_str(f"Размер: {item.product.size}"),
            smart_str(f"Итого: {item.get_total_price()}"),
            smart_str("----------------------------")
        ]

        for info in product_info:
            p.drawString(start_x, y_position, info)
            y_position -= 15

    p.showPage()
    p.save()
    return response
