from django.urls import path
from .views import home, signup,signin,verify_code

urlpatterns = [
    path('', home, name='home'),
    path('signup', signup, name='signup'),
    path('login', signin, name='signin'),
    path('verify', verify_code, name='verify'),
]
