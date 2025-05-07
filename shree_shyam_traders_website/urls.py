"""
URL configuration for shree_shyam_traders_website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from. import views
from django.conf import settings
from django.conf.urls.static import static
from .views import track_order

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('about-us/',views.about,name='about'),
    path('explain/<eid>',views.explain,name='explain'),
   path('checkout/',views.checkout,name='check'),
    path("",include("shopping.urls")),
    path("blog/",include("blog.urls")),
    path('userdata/',include('userdata.urls')),
    path('success/', views.success, name='success'),
    path('profile/',views.profile,name='profile'),
    path('track-order/<str:order_id>/', track_order, name='track_order'),
    path('raise-ticket/', views.raise_ticket, name='raise_ticket'),
    path('refund-policy/', views.refund_policy, name='refund_policy'),

     
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

