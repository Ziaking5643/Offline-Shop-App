from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Sum, Q
from django.http import HttpResponse
from decimal import Decimal
from .models import Product, Category, Customer, Order, OrderItem, Payment, InventoryLog
from .forms import ProductForm, CategoryForm, CustomerForm, OrderForm, OrderItemForm, PaymentForm


# Dashboard
def dashboard(request):
    total_products = Product.objects.count()
    total_customers = Customer.objects.count()
    total_orders = Order.objects.count()
    
    # Calculate revenue
    revenue = Order.objects.filter(status='completed').aggregate(Sum('net_amount'))['net_amount__sum'] or 0
    
    # Low stock products
    low_stock = Product.objects.filter(quantity_in_stock__lte=models.F('reorder_level'))
    
    # Recent orders
    recent_orders = Order.objects.all().order_by('-created_at')[:10]
    
    context = {
        'total_products': total_products,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'revenue': revenue,
        'low_stock': low_stock,
        'recent_orders': recent_orders,
    }
    return render(request, 'inventory/dashboard.html', context)


# Product Management
def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    query = request.GET.get('q')
    
    if query:
        products = products.filter(Q(name__icontains=query) | Q(sku__icontains=query))
    
    context = {'products': products, 'query': query}
    return render(request, 'inventory/product_list.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    inventory_logs = product.inventory_logs.all()[:20]
    
    context = {'product': product, 'logs': inventory_logs}
    return render(request, 'inventory/product_detail.html', context)


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            InventoryLog.objects.create(
                product=product,
                action='add',
                quantity=product.quantity_in_stock,
                reason='Initial Stock'
            )
            messages.success(request, f'Product {product.name} created successfully!')
            return redirect('product-list')
    else:
        form = ProductForm()
    
    context = {'form': form, 'title': 'Add Product'}
    return render(request, 'inventory/product_form.html', context)


def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product {product.name} updated successfully!')
            return redirect('product-detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    
    context = {'form': form, 'product': product, 'title': 'Edit Product'}
    return render(request, 'inventory/product_form.html', context)


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('product-list')
    
    context = {'product': product}
    return render(request, 'inventory/confirm_delete.html', context)


# Customer Management
def customer_list(request):
    customers = Customer.objects.all().order_by('-created_at')
    query = request.GET.get('q')
    
    if query:
        customers = customers.filter(Q(name__icontains=query) | Q(phone__icontains=query))
    
    context = {'customers': customers, 'query': query}
    return render(request, 'inventory/customer_list.html', context)


def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            messages.success(request, f'Customer {customer.name} created successfully!')
            return redirect('customer-list')
    else:
        form = CustomerForm()
    
    context = {'form': form, 'title': 'Add Customer'}
    return render(request, 'inventory/customer_form.html', context)


def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    orders = customer.order_set.all().order_by('-created_at')
    
    context = {'customer': customer, 'orders': orders}
    return render(request, 'inventory/customer_detail.html', context)


def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer updated successfully!')
            return redirect('customer-detail', pk=customer.pk)
    else:
        form = CustomerForm(instance=customer)
    
    context = {'form': form, 'customer': customer, 'title': 'Edit Customer'}
    return render(request, 'inventory/customer_form.html', context)


def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == 'POST':
        customer.delete()
        messages.success(request, 'Customer deleted successfully!')
        return redirect('customer-list')
    
    context = {'customer': customer}
    return render(request, 'inventory/confirm_delete.html', context)


# Order Management
def order_list(request):
    orders = Order.objects.all().order_by('-created_at')
    status = request.GET.get('status')
    
    if status:
        orders = orders.filter(status=status)
    
    context = {'orders': orders, 'status': status}
    return render(request, 'inventory/order_list.html', context)


def order_create(request):
    if request.method == 'POST':
        customer_id = request.POST.get('customer')
        customer = get_object_or_404(Customer, pk=customer_id)
        
        order = Order.objects.create(customer=customer)
        messages.success(request, f'Order {order.order_number} created! Now add items.')
        return redirect('order-edit', pk=order.pk)
    
    customers = Customer.objects.all()
    context = {'customers': customers}
    return render(request, 'inventory/order_create.html', context)


def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    items = order.items.all()
    
    context = {'order': order, 'items': items}
    return render(request, 'inventory/order_detail.html', context)


def order_edit(request, pk):
    order = get_object_or_404(Order, pk=pk)
    items = order.items.all()
    
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save()
            
            # Calculate totals
            total = items.aggregate(Sum('total'))['total__sum'] or 0
            order.total_amount = total
            order.net_amount = total - order.discount + order.tax
            order.save()
            
            messages.success(request, 'Order updated successfully!')
            return redirect('order-detail', pk=order.pk)
    else:
        form = OrderForm(instance=order)
    
    products = Product.objects.filter(is_active=True)
    context = {'order': order, 'form': form, 'items': items, 'products': products}
    return render(request, 'inventory/order_edit.html', context)


def add_order_item(request, order_pk):
    order = get_object_or_404(Order, pk=order_pk)
    
    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = int(request.POST.get('quantity', 0))
        unit_price = Decimal(request.POST.get('unit_price', 0))
        
        product = get_object_or_404(Product, pk=product_id)
        
        if product.quantity_in_stock < quantity:
            messages.error(request, f'Insufficient stock! Available: {product.quantity_in_stock}')
        else:
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                unit_price=unit_price
            )
            messages.success(request, f'Added {product.name} to order')
    
    return redirect('order-edit', pk=order_pk)


def remove_order_item(request, item_pk):
    item = get_object_or_404(OrderItem, pk=item_pk)
    order_pk = item.order.pk
    item.delete()
    messages.success(request, 'Item removed from order')
    return redirect('order-edit', pk=order_pk)


def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    
    if request.method == 'POST':
        order.delete()
        messages.success(request, 'Order deleted successfully!')
        return redirect('order-list')
    
    context = {'order': order}
    return render(request, 'inventory/confirm_delete.html', context)


# Payment Management
def add_payment(request, order_pk):
    order = get_object_or_404(Order, pk=order_pk)
    
    if hasattr(order, 'payment'):
        return redirect('order-detail', pk=order.pk)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.order = order
            payment.save()
            
            order.status = 'completed'
            order.save()
            
            # Log inventory reduction for sale
            for item in order.items.all():
                InventoryLog.objects.create(
                    product=item.product,
                    action='sale',
                    quantity=-item.quantity,
                    reason=f'Order {order.order_number}'
                )
                item.product.quantity_in_stock -= item.quantity
                item.product.save()
            
            messages.success(request, 'Payment recorded successfully!')
            return redirect('order-detail', pk=order.pk)
    else:
        form = PaymentForm(initial={'amount': order.net_amount})
    
    context = {'form': form, 'order': order}
    return render(request, 'inventory/payment_form.html', context)


def receipt_view(request, order_pk):
    order = get_object_or_404(Order, pk=order_pk)
    items = order.items.all()
    
    context = {'order': order, 'items': items}
    return render(request, 'inventory/receipt.html', context)


# Inventory Management
def inventory_logs(request):
    logs = InventoryLog.objects.all().order_by('-created_at')[:100]
    product = request.GET.get('product')
    
    if product:
        logs = logs.filter(product__id=product)
    
    context = {'logs': logs, 'products': Product.objects.all()}
    return render(request, 'inventory/inventory_logs.html', context)


def low_stock_report(request):
    products = Product.objects.filter(quantity_in_stock__lte=models.F('reorder_level')).order_by('quantity_in_stock')
    
    context = {'products': products}
    return render(request, 'inventory/low_stock.html', context)


from django.db import models
