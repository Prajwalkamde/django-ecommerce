import uuid
from django.shortcuts import render,redirect
from django.views import View
from .models import *
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from .forms import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q



# def home(request):
#  return render(request, 'app/home.html')

class ProductView(View):
    def get(self, request):
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        tvs = Product.objects.filter(category='TV')
        watches = Product.objects.filter(category='W')
        fridges = Product.objects.filter(category='FG')
        earphones = Product.objects.filter(category='EP')
        printers = Product.objects.filter(category='PR')
        return render(request, 'app/home.html', {'mobiles': mobiles, 'laptops': laptops, 'tvs': tvs, 'watches': watches, 'fridges': fridges, 'earphones': earphones, 'printers': printers})


# def product_detail(request):
#  return render(request, 'app/productdetail.html')

class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'app/productdetail.html', {'product': product})



def add_to_cart(request):
    if request.user.is_anonymous:
        return redirect('login')

    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    cart_obj = Cart(user=user, product=product )
    cart_obj.save()
    return redirect('/cart')

@login_required(login_url='/login/')
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70
        cart_product = [p for p in Cart.objects.all() if p.user == user]

        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
    
            return render(request, 'app/addtocart.html', {'carts':cart, 'totalamount':totalamount, 'amount':amount})
        return render(request, 'app/empty_cart.html')




def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        data = {
            'quantity' : c.quantity,
            'amount' : amount,
            'totalamount' : amount + shipping_amount
        }
        return JsonResponse(data)



def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        data = {
            'quantity' : c.quantity,
            'amount' : amount,
            'totalamount' : amount + shipping_amount
        }
        return JsonResponse(data)




def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        data = {
            'amount' : amount,
            'totalamount' : amount + shipping_amount
        }
        return JsonResponse(data)


@login_required(login_url='/login/')
def buy_now(request):
 return render(request, 'app/buynow.html')



class ProfileView(View):
    def get(self, request): 
        if request.user.is_anonymous:
            return redirect('login')       
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form' : form, 'active':'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            phone = form.cleaned_data['phone']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            customer_profile = Customer(user=user, name=name, locality=locality, city=city, phone=phone, state=state, zipcode=zipcode)
            customer_profile.save()
            messages.success(request, 'Profile Updated Successfully !')
        return render(request, 'app/profile.html', {'form' : form, 'active':'btn-primary'})



@login_required(login_url='/login/')
def address(request):
    address = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'address': address, 'active':'btn-primary'})


@login_required(login_url='/login/') 
def orders(request):
    user = request.user
    op = OrderPlaced.objects.filter(user=user)
    return render(request, 'app/orders.html', {'order_placed' : op})



def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category="M")

    elif data == "Redmi" or data == "Samsung":
        mobiles = Product.objects.filter(category="M").filter(brand=data)

    elif data == "OnePlus":
        mobiles = Product.objects.filter(category="M").filter(brand=data)

    elif data == "below-10000":
        mobiles = Product.objects.filter(category="M").filter(discounted_price__lt=10000)

    elif data == "above-10000":
        mobiles = Product.objects.filter(category="M").filter(discounted_price__gt=10000)

    return render(request, 'app/mobile.html', {'mobiles': mobiles})




def watch(request, data=None):
    if data == None:
        watches = Product.objects.filter(category="W")

    elif data == "Boat" or data == "Realme":
        watches = Product.objects.filter(category="W").filter(brand=data)

    elif data == "below-2000":
        watches = Product.objects.filter(category="W").filter(discounted_price__lt=2000)

    elif data == "above-2000":
        watches = Product.objects.filter(category="W").filter(discounted_price__gt=2000)

    return render(request, 'app/watch.html', {'watches': watches})



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.warning(request,"Oops! No user found!")
            return redirect('login')

        profile_obj = Profile.objects.filter(user=user_obj).first()
        if not profile_obj.is_email_verified:
            messages.warning(request,"Your account is not verified. please check your mail.")
            return redirect('login')

        user_obj = authenticate(username=username,password=password)

        # else:
        #     try:
        #         user_obj = authenticate(username=User.objects.get(email=username),password=password)
        #     except:
        #         user_obj = authenticate(username=username,password=password)
         

        if user_obj is not None:
            login(request,user_obj)
            messages.success(request,"Log in Successful !")
            return redirect('/')

        else:
            messages.warning(request,"Invalid Credentials! Please enter correct username or password !")
            return redirect('login')

    return render(request, 'app/login.html')



def customerregistration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        

        if User.objects.filter(username=username).first():
            messages.warning(request,"Username is already taken")
            return HttpResponseRedirect(request.path_info)

        if User.objects.filter(email=email).first():
            messages.warning(request,"Email is already taken")
            return HttpResponseRedirect(request.path_info)

        if pass1 != pass2:
            messages.warning(request,"Both passwords should match!")
            return HttpResponseRedirect(request.path_info)


        user_obj = User.objects.create_user(username=username, email=email, password=pass1)
        user_obj.save()
        email_token = str(uuid.uuid4())

        profile_obj = Profile.objects.create(user=user_obj, email_token=email_token)
        profile_obj.save()
        send_mail_after_signup(email, email_token)
        messages.success(request,"Email has been sent to verify your account!")
        return redirect('customerregistration')


    
    return render(request, 'app/customerregistration.html')




def user_verify(request, email_token):
    try:
        profile_obj = Profile.objects.filter(email_token=email_token).first()

        if profile_obj:
            if profile_obj.is_email_verified:
                messages.info(request,"Your account is already verified.")
                print(messages)
                return redirect('login')


            profile_obj.is_email_verified = True
            profile_obj.save()
            messages.success(request,"Your account has been verified. Now you can login.")
            return redirect('login')

        else:
            return redirect('error')
    except Exception as e:
        print(e)
        return render(request, 'login.html')






def send_mail_after_signup( email, email_token):
    subject = "Action Needed!!! Your account needs to be verify!"
    message = f"Please click on the link to verify your account. http://127.0.0.1:8000/verify/{email_token}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)



def user_logout(request):
    logout(request)
    messages.success(request," Logged out !")
    return redirect('login')





def change_password(request , token):
    context = {}
    
    try:
        profile_obj = Profile.objects.filter(forget_password_token = token).first()
        context = {'user_id' : profile_obj.user.id}
        
        if request.method == 'POST':
            new_password = request.POST.get('pass1')
            confirm_new_password = request.POST.get('pass2')
            user_id = request.POST.get('user_id')
            
            if user_id is  None:
                messages.warning(request, 'No user id found.')
                return redirect(f'/change_password/{token}/')
                
            
            if  new_password != confirm_new_password:
                messages.warning(request, 'Both passwords should  be equal!')
                return redirect(f'/change_password/{token}/')
                         
            
            user_obj = User.objects.get(id = user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            messages.success(request,"Your password has been changed. login with new password")
            return redirect('login')
            
            
            
        
        
    except Exception as e:
        print(e)
    return render(request, 'app/change_password.html', context)
    # return render(request , 'change_password.html' , context)





# for sending forget password link
def send_forgot_password_mail(email , token ):
    subject = 'Your password reset link '
    message = f'Hi , click on the link to reset your password http://127.0.0.1:8000/change_password/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True



import uuid
def forgot_password(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            
            if not User.objects.filter(username=username).first():
                messages.warning(request, 'No user found with this username.')
                return redirect('/forgot_password/')
            
            user_obj = User.objects.get(username = username)
            token = str(uuid.uuid4())
            profile_obj= Profile.objects.get(user = user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forgot_password_mail(user_obj.email , token)
            messages.success(request, f'We have sent an email to reset your password.')
            return redirect('/forgot_password/')
                
    
    
    except Exception as e:
        print(e)
    return render(request, 'app/forgot_password.html')




@login_required(login_url='/login/')
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        totalamount = amount +shipping_amount

    return render(request, 'app/checkout.html', {'add':add, 'totalamount':totalamount, 'cart_items':cart_items})


# @login_required(login_url='/login/')
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for cart_item in cart:
        order = OrderPlaced(user=user, customer=customer, product=cart_item.product, quantity=cart_item.quantity)
        order.save()
        cart_item.delete()
    return redirect('orders')