from django.shortcuts import render
from . models import *
import razorpay
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def home(request):
    if request.method == "POST":
        name = request.POST.get("name")
        amount = int(request.POST.get("amount"))*100
        client = razorpay.Client(auth=("rzp_test_nnd6tvDCL0c83L", "1PZgDaz08ynTq7GcCkBT63DR"))
        payment = client.order.create({'amount':amount, 'currency':'INR', 'payment_capture':'1'})
        donation = Donation(name= name, amount=amount/100, payment_id= payment['id'])
        donation.save()
        return render (request, "index.html", {'payment':payment})
        
    return render(request, "index.html")


@csrf_exempt
def success(request):
    if request.method == "POST":
        a = request.POST
        print(a)
        order_id = ""
        for key, val in a.items():
            if key == "razorpay_order_id":
                order_id = val
                break
        
        user = Donation.objects.filter(payment_id=order_id).first()
        user.paid = True
        user.save()
            
    return render(request, "success.html")


