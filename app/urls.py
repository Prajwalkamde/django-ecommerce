from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.ProductView.as_view(), name='home'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('cart/', views.show_cart, name='show_cart'),
    path('plus_cart/', views.plus_cart, name='plus_cart'),
    path('minus_cart/', views.minus_cart, name='minus_cart'),
    path('remove_cart/', views.remove_cart, name='remove_cart'),
    path('add_to_cart/', views.add_to_cart, name='add-to-cart'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    # path('changepassword/', views.change_password, name='changepassword'),                             
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('watch/', views.watch, name='watch'),
    path('watch/<slug:data>', views.watch, name='watchdata'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('registration/', views.customerregistration, name='customerregistration'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('change_password/<token>/', views.change_password, name='change_password'),
    path('verify/<email_token>', views.user_verify,name='verify'),
    # path('forget_password/' , views.ForgetPassword , name="forget_password"),
    # path('change_password/<token>/' , views.ChangePassword , name="change_password"),
    
    path('checkout/', views.checkout, name='checkout'),
    path("payment_done/", views.payment_done, name='payment_done'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)       
                       
                                                                                                                                                                                                                                                            