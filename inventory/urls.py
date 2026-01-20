from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Products
    path('products/', views.product_list, name='product-list'),
    path('products/create/', views.product_create, name='product-create'),
    path('products/<int:pk>/', views.product_detail, name='product-detail'),
    path('products/<int:pk>/edit/', views.product_edit, name='product-edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product-delete'),
    
    # Customers
    path('customers/', views.customer_list, name='customer-list'),
    path('customers/create/', views.customer_create, name='customer-create'),
    path('customers/<int:pk>/', views.customer_detail, name='customer-detail'),
    path('customers/<int:pk>/edit/', views.customer_edit, name='customer-edit'),
    path('customers/<int:pk>/delete/', views.customer_delete, name='customer-delete'),
    
    # Orders
    path('orders/', views.order_list, name='order-list'),
    path('orders/create/', views.order_create, name='order-create'),
    path('orders/<int:pk>/', views.order_detail, name='order-detail'),
    path('orders/<int:pk>/edit/', views.order_edit, name='order-edit'),
    path('orders/<int:pk>/delete/', views.order_delete, name='order-delete'),
    path('orders/<int:order_pk>/add-item/', views.add_order_item, name='add-order-item'),
    path('order-items/<int:item_pk>/remove/', views.remove_order_item, name='remove-order-item'),
    
    # Payments & Receipts
    path('orders/<int:order_pk>/payment/', views.add_payment, name='add-payment'),
    path('orders/<int:order_pk>/receipt/', views.receipt_view, name='receipt'),
    
    # Inventory
    path('inventory/logs/', views.inventory_logs, name='inventory-logs'),
    path('inventory/low-stock/', views.low_stock_report, name='low-stock'),
]
