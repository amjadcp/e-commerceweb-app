from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse
from .form import *
import json

# Login
def login(request):
    try:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            username = User.objects.get(email=email).username
            user = authenticate(username=username, password=password)
            if user is not None:
                request.session['username'] = username
                messages.info(request, 'Successfull')
                print(User.objects.get(email=email))
                return redirect('home')
            else:
                messages.info(request, 'Wrong Email or Password')
                return redirect('login')
        else:
            return render(request, 'login.html')
    except:
        messages.info(request, 'Wrong Email or Password')
        return redirect('login')

def user_logout(request):
    del request.session['username']
    # auth.logout(request)
    return redirect('login')

#Signup
def signup(request):
    # if request.session.has_key('username'):
    #     return redirect('login')
    # else:
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email exists')
                return redirect('signup')
            else:
                if password1 == password2:
                    user = User.objects.create_user(username=username, email=email, password=password1)
                    user.save()
                    messages.info(request, 'Successfuly created')
                    return redirect('signup')
                else:
                    messages.info(request, 'Password doesn\'t match')
                    return redirect('signup')
        else:
            return render(request, 'signup.html')

def check_email(request):
    email = request.POST['email']
    try:
        user = User.objects.get(email=email)
        if User.objects.filter(username=user).exists():
            return JsonResponse({'message' : 'Email exists'})
    except:
        return JsonResponse({'message' : ''})

def check_username(request):
    username = request.POST['username']
    if len(username) >= 6 and username != '':
     if User.objects.filter(username=username).exists():
        return JsonResponse({'message' : 'User exists'})
     else:
         return JsonResponse({'message' : ''})
    else:
        return JsonResponse({'message' : ''})
        

#Admin
def admin_login(request):
    try:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            admin = User.objects.get(email=email)
            if admin.is_superuser == True:
                admin = admin.username
                user = authenticate(username=admin, password=password)
                if user is not None:
                   messages.info(request, 'Successful')
                   request.session['admin'] = admin
                   return redirect('item_data')
                else:
                   messages.info(request, 'Email or password is incorrect')
                   return redirect('admin_login')
            else:
                messages.info(request, 'Email or password is incorrect')
                return redirect('admin_login')
        else:
            return render(request, 'admin_login.html')
    except:
        messages.info(request, 'Email or password is incorrect')
        return redirect('admin_login')

def admin_logout(request):
    del request.session['admin']
    # auth.logout(request)
    return redirect('admin_login')

#User data
def user_data(request):
    if request.session.has_key('admin'):
        data = User.objects.all()
        admin = request.session['admin']
        return render(request, 'user_data.html', {'admin':admin, 'data':data})
    else:
        return redirect('admin_login')

def user_data_update(request, id):
    if request.session.has_key('admin'):
        user = User.objects.get(id=id)
        username = user.username
        email = user.email
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            user.username = username
            user.email = email
            user.save()
            return redirect('user_data')
        else: 
           return render(request, 'user_data_update.html', {'username':username, 'email':email})
    else:
           return redirect('admin_login')

def user_data_delete(request, id):
    if request.session.has_key('admin'):
        user = User.objects.get(id=id)
        user.delete()
        return redirect('user_data')
    else:
        return redirect('admin_login')


#item data
def item_data(request):
    if request.session.has_key('admin'):
        data = Item.objects.all()
        admin = request.session['admin']
        return render(request, 'item_data.html', {'data':data, 'admin':admin})
    else:
        return redirect('admin_login') 

def add_item(request):
    if request.session.has_key('admin'):
        if request.method == 'POST':
            form = Add_item_form(request.POST)
            item = form.cleaned_data['item']
            price = form.cleaned_data['price']
            disc = form.cleaned_data['disc']
            category = form.cleaned_data['category']
            img = form.cleaned_data['img']
            items = Item.objects.create(
                item=item,
                price=price,
                disc=disc,
                category=category,
                img=img
            )
            items.save()
        else:
            form = Add_item_form()
        return render(request, 'add_item.html', {'form':form})
    else:
        return redirect('admin_login')

def add_category(request):
    if request.session.has_key('admin'):
       form = Add_category_form()
       return render(request, 'add_category.html', {'form':form})
    else:
        return redirect('admin_login')

def home(request):
    if request.session.has_key('username'):
        user = request.session['username']
        items = Item.objects.all()
        return render(request, 'home.html', {'user':user, 'items':items})
    else:
        return redirect('login')

def cart(request):
    if request.session.has_key('username'):
        user = request.session['username']
        if request.method == 'POST':
           item = request.POST['item']
           try:
                op = 0
                carts = Cart.objects.filter(user=user)
                for cart in carts:
                    if cart.item == item:
                        op = op+1
                    else:
                        pass
                if op != 0:
                    return JsonResponse({'message' : 'Product already in your cart'})
                else:
                        Cart.objects.create(
                            user=user,
                            item=item,
                        )
                        return redirect('cart')
           except:
               Cart.objects.create(
                            user=user,
                            item=item,
                        )
               return redirect('cart')
        else:
            try:
                carts = Cart.objects.filter(user=user)
                items = []
                for cart in carts:
                   item= Item.objects.get(item=cart.item)
                   items.append(item)
                return render(request, 'cart.html', {'user':user, 'items':items})
            except:
                return JsonResponse({'message' : 'Your cart is empty'})

    else:
        return redirect('login')

def updater(request):
    if request.session.has_key('username'):
       id = request.POST['id']
       price = Item.objects.get(id=id).price
       qty = Item.objects.get(id=id).qty
       
       return JsonResponse({
           'id':id,
           'price' : price,
           'qty': qty
       })

def remove_cart(request):
    if request.session.has_key('username'):
       user = request.session['username']
       item = request.POST['remove']
       carts = Cart.objects.filter(user=user)
       for cart in carts:
           if cart.item == item:
               cart.delete()
           else:
               pass

       return redirect('cart')
       
def place_order(request):
    if request.session.has_key('username'):
       if request.method == 'POST':
        user = request.session['username']
        id = request.POST['id']
        id = json.loads(id)
        qty = request.POST['qty']
        qty = json.loads(qty)
        subTotel = request.POST['subTotel']
        name= request.POST['name']
        number= request.POST['number']
        email= request.POST['email']
        address= request.POST['address']
        address2= request.POST['address2']
        city= request.POST['city']
        state= request.POST['state']
        pin= request.POST['pin']
        print('--',id)
        for i in id['id']:
            print(qty['qty'][i])
            Order.objects.create(
                user=user,
                name = name,
                number=number,
                email=email,
                address=address,
                address2=address2,
                city=city,
                state=state,
                pin=pin,
                item = Item.objects.get(id=i).item,
                qty = qty['qty'][i],
                totel_price = (Item.objects.get(id=i).price) * qty['qty'][i]
            )

            item = Item.objects.get(id=i)
            print(item.qty)
            dif = (item.qty) - qty['qty'][i]
            item.qty = dif
            item.save()

        print(Order.objects.all())
      
        return JsonResponse({'message' : 'Your Order Placed as COD'})

def list_of_order(request):
    if request.session.has_key('admin'):
        orders = Order.objects.all()
        admin = request.session['admin']
        return render(request, 'list_of_order.html', {'orders':orders, 'admin':admin})