@echo off
REM Script to create sample data for testing
echo.
echo ========================================
echo   Load Sample Data
echo ========================================
echo.

cd /d "%~dp0"

REM Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)

echo [*] Loading sample products and customers...

python manage.py shell << EOF
from inventory.models import Category, Product, Customer
from decimal import Decimal

# Create categories
electronics, _ = Category.objects.get_or_create(
    name="Electronics",
    defaults={'description': 'Electronic items and gadgets'}
)
clothing, _ = Category.objects.get_or_create(
    name="Clothing",
    defaults={'description': 'Apparel and fashion items'}
)
groceries, _ = Category.objects.get_or_create(
    name="Groceries",
    defaults={'description': 'Food and grocery items'}
)

# Create sample products
products_data = [
    ("Laptop", "TECH001", electronics, Decimal("40000"), Decimal("55000"), 5),
    ("Mobile Phone", "TECH002", electronics, Decimal("15000"), Decimal("25000"), 10),
    ("T-Shirt", "CLT001", clothing, Decimal("300"), Decimal("699"), 50),
    ("Jeans", "CLT002", clothing, Decimal("1000"), Decimal("2499"), 20),
    ("Rice 10kg", "GRC001", groceries, Decimal("400"), Decimal("599"), 15),
    ("Sugar 5kg", "GRC002", groceries, Decimal("200"), Decimal("299"), 20),
]

for name, sku, category, purchase_price, selling_price, stock in products_data:
    product, created = Product.objects.get_or_create(
        sku=sku,
        defaults={
            'name': name,
            'category': category,
            'purchase_price': purchase_price,
            'selling_price': selling_price,
            'quantity_in_stock': stock,
            'reorder_level': 5
        }
    )
    if created:
        print(f"Created: {name}")

# Create sample customers
customers_data = [
    ("Ahmed Khan", "03001234567", "ahmed@email.com", "123 Main Street", "Karachi"),
    ("Fatima Ali", "03009876543", "fatima@email.com", "456 Market Road", "Lahore"),
    ("Muhammad Hassan", "03101234567", "hassan@email.com", "789 City Center", "Islamabad"),
    ("Ayesha Malik", "03215678901", "ayesha@email.com", "321 Commercial Area", "Rawalpindi"),
]

for name, phone, email, address, city in customers_data:
    customer, created = Customer.objects.get_or_create(
        name=name,
        defaults={
            'phone': phone,
            'email': email,
            'address': address,
            'city': city
        }
    )
    if created:
        print(f"Created customer: {name}")

print("\n[+] Sample data loaded successfully!")
EOF

echo.
echo [+] Sample data has been added!
echo [+] You can now login and see sample products and customers
echo.
pause
