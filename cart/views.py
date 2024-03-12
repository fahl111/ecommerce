from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from shop.models import Product
from cart.models import Cart,Account

from cart.models import Account


def cartview(request):
    total=0
    u=request.user
    cart=Cart.objects.filter(user=u)
    for i in cart:
        total+=i.quantity*i.product.price
    return render(request, 'cart.html',{'c':cart,'total':total})
@login_required
# Create your views here.
def cart(request,n):
    p = Product.objects.get(name=n)
    u = request.user
    try:
        cart = Cart.objects.get(user=u,product=p)
        if(cart.quantity<cart.product.stock):
            cart.quantity+=1
            cart.save()
    except:
        if(p.stock>0):
            cart = Cart.objects.create(product=p,user=u,quantity=1)
            cart.save()
    return redirect('cart:cartview')
def remove_from_cart(request, n):
    p = Product.objects.get(name=n)
    u = request.user
    try:
        cart_item = Cart.objects.get(user=u, product=p)
        cart_item.delete()
    except Cart.DoesNotExist:
        # Handle the case where the item is not in the cart
        raise Http404("Item not found in the cart")

    return redirect('cart:cartview')
def decrement_cart(request, n):
    p = Product.objects.get(name=n)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=p)

        if cart.quantity > 1:
            cart.quantity -= 1
            cart.save()
        else:
            cart.delete()

    except Cart.DoesNotExist:
        pass

    return redirect('cart:cartview')
def orderform (request):
    if request.method=="POST":
        a=request.POST['a']
        ph=request.POST['ph']
        an=request.POST['an']

        u=request.user
        cart=Cart.objects.filter(user=u)

        total=0
        for i in cart:
            total+=i.quantity*i.product.price


        try:
            ac=Account.objects.get(accnum=an)
            if(ac.amount >= total):
                ac=amount=ac.amount-total
                ac.save()
                return HttpResponse('Ordered')
            else:
                return HttpResponse('insufficent')

        except:
            pass
        return HttpResponse(total)



    return render(request, 'orderform.html')