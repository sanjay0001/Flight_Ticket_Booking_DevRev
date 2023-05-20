from django.urls import path
from . import views

urlpatterns=[
    path('login', views.login, name='login'),
    path('', views.login, name='login'),
    path('register', views.register, name='register'),
    path('profile', views.profile, name='profile'),
    path('adminlogin', views.adminlogin, name='adminlogin'),
    path('addflight', views.addflight, name='addflight'),
    path('removeflight/<int:flight_id>', views.removeflight, name='removeflight'),
    path('adminprofile', views.adminprofile, name='adminprofile'),
    path('logout', views.logout, name='logout'),
    path('bookflight/<int:flight_id>', views.bookflight, name='bookflight'),
    path('buyticket', views.buyticket, name='buyticket'),
    path("verify_email", views.verify_email, name="verify_email"),
    path("adminview", views.adminview, name='adminview'),
]
