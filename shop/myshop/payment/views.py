import braintree

import weasyprint

from io import BytesIO

from orders.models import Order


from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import  EmailMessage

from orders.utils import html_to_pdf


def payment_process(request):
    order_id = request.session.get("order_id")
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        # Получение токена для создания транзакции.
        nonce = request.POST.get('payment_method_nonce', None)
        # Создание и сохранение транзакции.
        result = braintree.Transaction.sale({
            'amount': '{:.2f}'.format(order.get_total_cost()),
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })

        if result.is_success:
            # Отметка заказа как оплаченного
            order.paid = True
            # Сохранение ID транзакции в заказе
            order.braintree_id = result.transaction.id
            order.save()
            # Создание электронного сообщения.
            subject = 'My Shop - Invoice no. {}'.format(order.id)
            message = 'Please, find attached the invoice for your recent purchase.'
            email = EmailMessage(
                subject,
                message,
                'admin@gmail.com',
                [order.email],
            )
            
            # Формирование PDF
            html = render_to_string('orders/order/pdf.html', {'order': order})
            pdf, result = html_to_pdf(html)
            # Прикрепляем PDF к электронному сообщению.
            email.attach(
                'order_{}.pdf'.format(order.id),
                result.getvalue(),
            '   application/pdf')
            # Отправка сообщения.
            email.send()
            
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        # Формирование одноразового токена для JavaScript SDK.
        client_token = braintree.ClientToken.generate()
        return render(request, 
            'payment/process.html',
            {
                'order': order,
                'client_token': client_token
            }
        )
    

def payment_done(request):
    return render(request, 'payment/done.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')


