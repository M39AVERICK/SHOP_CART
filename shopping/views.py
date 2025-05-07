from django.shortcuts import render
from shopping.models import PRODUCT,Contact
from django.contrib import messages

def contact(request):
    if request.method=='POST':
        uname=request.POST.get('uname')
        uemail=request.POST.get('email')
        desc=request.POST.get('help')
        phone=request.POST.get('mobile')
        myquery=Contact(c_name=uname,c_phone=phone,c_email=uemail,c_desc=desc)
        myquery.save()
        messages.info(request,'We will get in touch with you shortly!')
       
    return render(request,'contact.html')
