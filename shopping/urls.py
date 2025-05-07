from django.urls import path
from . import views
urlpatterns = [
    # path("",views.index,name="shop"),
    path('contact/',views.contact,name='contact') 
    
]