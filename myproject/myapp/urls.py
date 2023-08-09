# urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blog/', views.blog, name='blog'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog_list, name='blog_list'), 
    #path('post_details/<int:pk>/', views.post_details, name='post_details'),
    path('post_details/<slug:post_slug>/', views.post_details, name='post_details'),
    path('blog/tag/<slug:tag_slug>/', views.blog_with_tag, name='blog_with_tag'),
    path('blog/<slug:category_slug>/', views.blog_with_category, name='blog_with_category'),
    path('subscribe/', views.subscribe, name='subscribe_newsletter'),
    path("newsletter/", views.newsletter, name="newsletter"),
    #path('subscribe/', views.subscribe, name='subscribe'),
    path('subscribe/', views.subscribe, name='subscribe_newsletter'),
    path('resources/', views.resource_list, name='resource_list'),
    #path('resources/<int:resource_id>/purchase/', views.purchase_resource, name='purchase_resource'),
    path('resources/<int:resource_id>/purchase/', views.purchase_resource_view, name='purchase_resource'),  # Updated view name
    #path('register/', views.register_user, name='register'),
    #path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
   # path('logout/', auth_views.LogoutView.as_view(next_page='resource_list'), name='logout'),  # Add the logout URL pattern
    # ...
   # path('resources/<int:resource_id>/add_to_cart/', views.add_to_cart, name='add_to_cart'),
     # Cart URLs
   # path('cart/add/<int:resource_id>/', views.add_to_cart, name='add_to_cart'),
    #path('cart/', views.view_cart, name='view_cart'),
    #path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/add/<int:resource_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),

 # Login, Logout, and Register URLs
    #path('login/', views.LoginView.as_view(template_name='myapp/login.html'), name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    #path('logout/', views.LogoutView.as_view(), name='logout'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout, name='logout'),
    path('clear_messages/', views.clear_messages, name='clear_messages'),
    path('checkout/', views.checkout, name='checkout'),
    path('resources/<int:resource_id>/', views.resource_detail, name='resource_detail'),
    path('update_cart_quantity/<int:cart_item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('cart_count/', views.cart_count, name='cart_count'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment_process/', views.payment_process, name='payment_process'), 
    path('order_success/', views.order_success, name='order_success'),
    path('generate_receipt/', views.generate_receipt, name='generate_receipt'),
    
    # ... other URL patterns ...
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
