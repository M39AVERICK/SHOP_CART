from django.shortcuts import render,HttpResponse,redirect
from shopping.models import PRODUCT,Contact,Orders,OrderUpdate
from math import ceil
from django.contrib import messages
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.decorators import login_required


import json
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.http import JsonResponse

def contact(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'LOGIN FIRST')
        return redirect('login')
    
    if request.method == 'POST':
        name = request.POST.get('uname')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        help_text = request.POST.get('help')
        
        # TODO: Save to DB or handle as needed
        print(name, email, mobile, help_text)  # For now, just print to verify

        messages.success(request, "Your message has been submitted.")
        return redirect('thank_you')  # Replace with your actual thank you page

    return render(request, 'contact.html')

def raise_ticket(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # Save to DB or notify support team
        # ...
        return redirect('thank_you')

def index(request):
    allprods = []
    catprod = PRODUCT.objects.values('P_category', 'id')
   
    cats = {item['P_category'] for item in catprod}
    for cat in cats:
        prod = PRODUCT.objects.filter(P_category=cat)
        n = len(prod)
        nslides = n//4 + ceil(n / 4) -(n//4)
        allprods.append([prod, range(1, nslides + 1), nslides])
    context = {'alldata': allprods}
    return render(request, 'index.html', context)


from django.shortcuts import render, redirect
from django.contrib import messages
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Razorpay API Credentials (Replace with your own)
RAZORPAY_KEY_ID = "rzp_test_96NFN1CuVxcyzR"
RAZORPAY_KEY_SECRET = "dUKOCqr5DYOs1UCBt9FavZMC"
import json

def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'LOGIN FIRST')
        return redirect('login')

    if request.method == "POST":
        try:
            # Retrieve form data
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            address = request.POST.get('address')  
            email=request.POST.get('email')
            state=request.POST.get('City'),
            pincode = request.POST.get('pincode')
            payment_method = request.POST.get('payment-method')
            items_json = request.POST.get('itemjson')
            amount = request.POST.get('amt')
            razorpay_payment_id = request.POST.get('razorpay_payment_id', '')

            # Debugging Prints
            # print(f"Received Data: {name}, {phone}, {address}, {pincode}, {items_json}, {amount}, {payment_method}, {razorpay_payment_id}")

            # Check if required fields are None
            if not all([name, phone, address, pincode, items_json, amount]):
                messages.error(request, "Missing required fields")
                return redirect('checkout')

            # Create Order Entry
            order = Orders(
                items_json=items_json,
                amount=amount,
                name=name,
                phone=phone,
                email=email,
                temp_address=address,
                per_address=address,  # Update based on model fields
                city=state,  # Not collected in form
                state=state,  # Not collected in form
                zipcode=pincode,
                oid=razorpay_payment_id if payment_method == "online" else "",
                amountpaid=amount if payment_method == "online" else "COD",
                paymentstatus="Paid" if payment_method == "online" else "Pending"
            )
            order.user = request.user
            order.save()
            # After order.save()
            OrderUpdate.objects.create(
                order=order,
                update_desc="Order placed successfully.",
                delivered=False
            )


            print("Order Saved Successfully")  # Debugging
            return redirect('success')

        except Exception as e:
            print(f"Error Occurred: {e}")
            messages.error(request, f"Error while saving order: {str(e)}")
            return redirect('checkout')

    return render(request, 'checkout.html')



def success(request):
    return render(request,'success.html')

def payment(request):
    if request.method == "POST":
        amt = int(float(request.POST.get("amt", 0)) * 100)  # Convert to paise (1 INR = 100 paise)
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        if amt <= 0:
            messages.error(request, "Invalid amount")
            return redirect('checkout')

        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        payment_data = {
            "amount": amt,
            "currency": "INR",
            "payment_capture": "1"
        }
        order = client.order.create(data=payment_data)

        context = {
            "order_id": order["id"],
            "amt": amt / 100,  # Convert back to INR
            "name": name,
            "email": email,
            "phone": phone,
            "razorpay_key": RAZORPAY_KEY_ID
        }
        return render(request, "payment.html", context)

    return redirect("checkout")

@csrf_exempt
def verify_payment(request):
    if request.method == "POST":
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        try:
            payment_id = request.POST.get("razorpay_payment_id")
            order_id = request.POST.get("razorpay_order_id")
            signature = request.POST.get("razorpay_signature")

            params_dict = {
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature,
            }

            client.utility.verify_payment_signature(params_dict)

            return JsonResponse({"status": "success", "payment_id": payment_id})
        except razorpay.errors.SignatureVerificationError:
            return JsonResponse({"status": "failure", "message": "Payment verification failed"})
    
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)
def about(request):
    return render(request,'about.html')

def service(request):
    return render(request,'services.html')

from django.shortcuts import get_object_or_404
# for passing the dynamic data roting->
def explain(request,eid):
    full = get_object_or_404(PRODUCT, id=eid)
    data={'detail':full}
    return  render(request,'explain.html',data)



def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'LOGIN FIRST AND THEN TRY AGAIN!')
        return redirect('login')

    cur_user_email = request.user.email
    items = Orders.objects.filter(email=cur_user_email).order_by('-oid')  # Get all orders (latest first)

    orders_list = []
    for order in items:
        try:
            items_data = json.loads(order.items_json)
        except json.JSONDecodeError:
            items_data = {}

        orders_list.append({
            'order_id': order.oid,
            'items': items_data,
            'amount': order.amount,
            'name': order.name,
            'email': order.email,
            'address': order.per_address,
            'city': order.city,
            'amount_paid': order.amountpaid,
            'payment_status': order.paymentstatus,
            'phone': order.phone,
            'tracking_id': order.tracking_id if hasattr(order, 'tracking_id') else None,
            'tracking_url': order.tracking_url if hasattr(order, 'tracking_url') else None,
        })

    if request.method == "POST":
        new_name = request.POST.get("name")
        new_address = request.POST.get("address")
        new_email = request.POST.get("email")  # Changed from 'Email' to 'email'
        new_phone = request.POST.get("phone")

        if new_name:
            request.user.first_name = new_name
            request.user.save()

        if new_email:
            request.user.email = new_email
            request.user.save()

        if new_address and items.exists():
            latest_order = items.first()
            latest_order.per_address = new_address
            latest_order.save()

        if new_phone and items.exists():
            latest_order = items.first()
            latest_order.phone = new_phone  # Fix the incorrect `order.phone`
            latest_order.save()

        messages.success(request, "Your details have been updated")

    data = {
        'name': request.user.first_name,
        'orders': orders_list,
        'email': request.user.email,
        
        
      
    }
    return render(request, 'profile.html', data)

def refund_policy(request):
    return render(request, 'refund_policy.html')



def track_order(request, order_id):
    order = Orders.objects.filter(oid=order_id).first()  # Fix: Use correct field name
    if order and order.tracking_url:
        return JsonResponse({"tracking_url": order.tracking_url})
    return JsonResponse({"error": "Tracking details not available"}, status=404)
