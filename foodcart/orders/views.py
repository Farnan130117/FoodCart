from django.shortcuts import render
from cart.cart import Cart
from .models import OrderItem
from .forms import OrderCreateForm
#from .tasks import order_created


def order_create(request):
	cart = Cart(request)
	if request.method == 'POST':
		form = OrderCreateForm(request.POST)
		if form.is_valid():
			form.instance.first_name='test' #important 
			#getting submitted data from formdata to function 
			order = form.save()
			total = cart.get_total_price();
			amount=1000;
			#amount_return=amount-total;
			amount_return=order.first_name;
			for item in cart:
				OrderItem.objects.create(order=order,
										 product=item['product'],
										 price=item['price'],
										 quantity=item['quantity'])
			# clear the cart
			cart.clear()
			# launch asynchronous task
			# order_created.delay(order.id)
			return render(request,
						  'orders/order/created.html',
						  {
						   'order': order,
						   'total':total,
						   'amount_return':amount_return,
							})
	else:
		form = OrderCreateForm()
	return render(request,
				  'orders/order/create.html',
				  {'cart': cart, 'form': form})