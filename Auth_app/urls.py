from django.urls import path
from Auth_app import views

urlpatterns = [
    path('',views.index, name='index'),
    path('dashboard',views.dashboard, name='dashboard'),
    path('signup', views.signup, name='signup'),
    # path('retrieve', views.retrieve, name='retrieve'),
    path('updation/<int:pk>', views.updation, name='updation'),
    path('deletion', views.deletion, name='deletion'),
    # path('success', views.success, name="success"),
    path('login', views.login, name='login'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('otp', views.otp, name='otp'),
    path('reset_password', views.reset_password, name='reset_password'),
    path('logout', views.logout, name='logout'),
]