from django.shortcuts import render,HttpResponse
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

from datetime import datetime
from home.models import Contact
from home.models import Donator

from django.contrib import messages

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


# Create your views here.
def index(request):
    
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def do(request):
    return render(request,'do.html')

def projects(request):
    return render(request,'projects.html')

def blog(request):
    return render(request,'blog.html')

def contact(request):
    if request.method =="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        message=request.POST.get('message')
        contact=Contact(name=name,email=email,message=message,date=datetime.today())
        contact.save()
        messages.success(request, 'Your message has been sent')
    return render(request,'contact.html')

def donation(request):
#     if request.method =="POST":
#         name=request.POST.get('name')
#         email=request.POST.get('email')
#         amount=request.POST.get('amount')
#         donator=Donator(name=name,email=email,amount=amount,date=datetime.today())
#         donator.save()
#         # messages.success(request, 'Thank you for your contribution')
#     return render(request,'donation.html')


# def donation(request):
    currency = 'INR'
    amount = 20000  # Rs. 200
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    if request.method =="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        amount=request.POST.get('amount')
        donator=Donator(name=name,email=email,amount=amount,date=datetime.today())
        donator.save()
        # messages.success(request, 'Thank you for your contribution')
    return render(request, 'donation.html', context=context)
 
 
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        
    
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is None:
                amount = 20000  # Rs. 200
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
 
                    # render success page on successful caputre of payment
                    return render(request, 'paymentsuccess.html')
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:
 
                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()     