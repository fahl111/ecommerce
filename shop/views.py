from django.contrib.auth.models import User
from django.shortcuts import render
from shop.models import Category, Product
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate , logout
from django.contrib.auth.decorators import login_required

# Create your views here.


def allcategories(request):
    k = Category.objects.all()
    return render(request, 'category.html', context={'c': k})
def product(request,p):
    c=Category.objects.get(name=p)
    p=Product.objects.filter(category=c)
    return render(request, 'product.html', context={'c': c,'p':p})
def detail(request,p):
    p=Product.objects.get(name=p)
    return render(request, 'detail.html', context={'p': p})

def register(request):
    if (request.method == 'POST'):
        u = request.POST['u']
        q = request.POST['q']
        r = request.POST['r']
        f = request.POST['f']
        l = request.POST['l']
        e = request.POST['e']
        if(q==r):
            b = User.objects.create_user(username=u, password=q, first_name=f, last_name=l,email=e)
            b.save()
            return redirect('shop:allcat')
        else:
            return HttpResponse("pass same")
    return render(request, 'register.html')

def userlogin(request):
    if (request.method == 'POST'):
        u = request.POST['u']
        p = request.POST['p']
        user=authenticate(username=u,password=p)
        if user:
            login(request,user)
            return redirect('shop:allcat')
        else:
            return HttpResponse("Invalid credentials")
    return render(request, 'login.html')
@login_required
def user_logout(request):
    logout(request)
    return redirect('shop:userlogin')

