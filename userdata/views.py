from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from .utils import TokenGenerator,generate_token
from django.utils.encoding import force_bytes,DjangoUnicodeDecodeError
from django.views.generic import View
from django.contrib.auth import authenticate,login,logout
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.


def signup(request):
    if(request.method =='POST'):
        user_email=request.POST.get('email')
        passwd=request.POST.get("pass1")
        cnf_pass=request.POST.get("pass2")
        if(passwd!=cnf_pass):
            messages.warning(request,"Password is In-correct!")
            return render(request,'authentication/signup.html')
            
        try:
            if User.objects.get(username=user_email):
                messages.info(request,"Email Already exists!")
                return render(request,'authentication/signup.html')    
                # return HttpResponse("Email already exists!")
               # if email alredy exists then 
                
        except Exception as identifier:
            pass

        user=User.objects.create_user(user_email,user_email,passwd)
        user.is_active=False
        user.save()
        email_subject="Activate Your Account"
        message=render_to_string('authentication/activate.html',{
            'user':user,
            'domain':'127.0.0.1:8000', #hosting address but here is our localhost
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user)
        })
        
        send_mail(
                    email_subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [user_email],
                    fail_silently=False,
            )
        messages.success(request,"USER CREATED",user_email)
        messages.success(request,"Activate Your account by clicking the link in your gmail")
        return render(request,'authentication/login.html') 
        # return HttpResponse("USER CREATED",user_email)
    return render(request,'authentication/signup.html')



class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_bytes(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            messages.warning(request,"Account Activated Successfully!")
            user.save()
            return render(request,'authentication/login.html')
        return render(request,'authentication/activate_fail.html',{'pl':'Please enter the Valid Email! '})


def handle_login(request):
    if request.method == 'POST':
        u_name=request.POST.get('email')
        u_password=request.POST.get('pass1')
        my_user=authenticate(username=u_name , password=u_password)

        if my_user is not None:
            login(request,my_user)
            # messages.error(request,'finding the page')
            # print("now i am getting the pas and checking for the page redirection->")
            messages.success(request,'Login Success')
            return redirect("/")
        
        else:
            messages.error(request,'Invalid Credentials!')
            return render(request,'authentication/login.html')
        
    return render(request,'authentication/login.html')


def handle_logout(request):
    logout(request)
    messages.info(request,'Logout Success')
    return redirect("/")



import random


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import random

def forget(request):
    otp_stage = False
    password_stage = False
    email = request.session.get('email')  # Reuse saved email if available

    if request.method == 'POST':
        stage = request.POST.get('stage')

        # Step 1: Handle Email Submission
        if stage == 'email':
            email = request.POST.get('email')
            users = User.objects.filter(email=email)
            if users.exists():
                user = users.first()  # Safely get one user
                request.session['email'] = email
                otp = random.randint(100000, 999999)
                request.session['otp'] = str(otp)

                send_mail(
                    subject='Your OTP for Password Reset',
                    message=f'Your OTP is {otp}',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                    fail_silently=False,
                )
                messages.success(request, f'OTP sent to {email}.')
                otp_stage = True
            else:
                messages.error(request, 'Email is not registered.')

        # Step 2: Handle OTP Validation
        elif stage == 'otp':
            user_otp = request.POST.get('otp')
            session_otp = request.session.get('otp')
            if user_otp == session_otp:
                messages.success(request, 'OTP validated. Please set a new password.')
                password_stage = True
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
                otp_stage = True

        # Step 3: Handle Password Reset
        elif stage == 'password':
            new_password = request.POST.get('new_password')
            email = request.session.get('email')
            users = User.objects.filter(email=email)
            if users.exists():
                user = users.first()
                user.set_password(new_password)
                user.save()

                # Clean up session
                request.session.pop('email', None)
                request.session.pop('otp', None)

                messages.success(request, 'Password reset successfully. You can now login.')
                return redirect('login')
            else:
                messages.error(request, 'User not found. Please try again.')

    return render(request, 'authentication/forget.html', {
        'otp_stage': otp_stage,
        'password_stage': password_stage,
        'email': email
    })
