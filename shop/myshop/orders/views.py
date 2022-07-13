from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string

from .utils import html_to_pdf
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from . import tasks



def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order, 
                                        product=item['product'], 
                                        price=item['price'], 
                                        quantity=item['quantity'])
            # Очищаем корзину.
            cart.clear()   
            tasks.order_create(order.id)
            # Сохранение заказа в сессии.
            request.session['order_id'] = order.id
            # Перенаправление на страницу оплаты.
            return redirect(reverse('payment:process'))         
    else:
        form = OrderCreateForm()
    return render(request,
                'orders/order/create.html',
                {'cart': cart, 'form': form}
            )               
        

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 
        'admin/orders/order/detail.html', {
            'order': order
        })


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)   
    html = render_to_string('orders/order/pdf.html', {'order': order})
    pdf, result = html_to_pdf(html)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf; charset=UTF-8')
    return None