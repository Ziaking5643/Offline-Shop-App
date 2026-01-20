 Shop Management System - Offline Django App

A complete offline-capable Django web application for managing inventory, customers, and orders for small businesses with no internet access.

##  Features

### Inventory Management
-  Product CRUD (Create, Read, Update, Delete)
-  SKU tracking and categorization
-  Stock level monitoring with reorder alerts
-  Profit margin calculations
-  Inventory activity logging

### Customer Management
-  Customer database with contact details
-  Customer order history
-  Purchase statistics
-  City/Location tracking

### Order Management
-  Create and manage customer orders
-  Add/remove multiple items per order
-  Automatic order numbering
-  Order status tracking (Pending, Confirmed, Completed, Cancelled)
-  Discount and tax calculations
-  Order editing and deletion

### Payment & Receipts
-  Payment recording (Cash, Check, Bank Transfer, Credit)
-  Professional receipt generation
-  Print-friendly receipts
-  Payment method tracking

### Reporting
-  Dashboard with key metrics
-  Low stock alerts and reports
-  Inventory activity logs
-  Revenue tracking
-  Order status reports

### Admin Panel
-  Django admin interface for advanced management
-  Bulk operations support
-  Database management tools

## 🚀 Quick Start

### System Requirements
- Windows OS (7, 8, 10, 11)
- Python 3.8 or higher (download from https://www.python.org/)
- At least 100MB free disk space

### Installation

1. **Extract the project** to a folder on your computer
   - Example: `C:\ShopApp` or `E:\django\shop_app`

2. **Run Setup (First Time Only)**
   - Double-click `setup.bat`
   - This will create the virtual environment and install dependencies
   - Wait for the message "Setup complete!"

3. **Start the Application**
   - Double-click `run.bat`
   - Wait for the server to start
   - A command window will show: "Server is running at: http://127.0.0.1:8000/"

4. **Access the Web App**
   - Open your web browser (Chrome, Firefox, Edge, etc.)
   - Go to: `http://127.0.0.1:8000/`

5. **Login to Admin Panel**
   - Go to: `http://127.0.0.1:8000/admin/`
   - Username: `admin`
   - Password: `admin123`
   - ⚠️ **IMPORTANT**: Change this password immediately after first login!

## Using the Application

### Dashboard
- View total products, customers, orders
- Track total revenue from completed orders
- See low stock alerts
- Quick access to recent orders

### Managing Products
1. Go to **Inventory → Products**
2. Click "➕ Add Product" to create a new product
3. Fill in:
   - Product Name
   - SKU (unique code)
   - Category (optional)
   - Purchase and Selling Prices
   - Initial Stock Quantity
4. Click "Save"

### Managing Customers
1. Go to **Customers**
2. Click "➕ Add Customer"
3. Fill in customer details:
   - Name (required)
   - Phone number
   - Email
   - Address
   - City
4. Click "Save"

### Creating Orders
1. Go to **Orders**
2. Click "➕ Create Order"
3. Select a customer (create one if needed)
4. Click "Create Order"
5. Add items to the order:
   - Select product
   - Enter quantity
   - Unit price will auto-fill
6. Click "Add Item"
7. Adjust discount and tax if needed
8. Click "Save Changes"

### Recording Payments
1. Open an order from **Orders**
2. Scroll to "Payment Information"
3. Click "➕ Add Payment"
4. Fill in:
   - Amount Paid
   - Payment Method (Cash, Check, Transfer, Credit)
   - Transaction ID (optional)
5. Click "Record Payment"
6. Order status automatically changes to "Completed"

### Printing Receipts
1. Open a completed order
2. Click "🖨️ Print Receipt"
3. Review the receipt in the new window
4. Click the Print button or use Ctrl+P to print

##  Maintenance

### Backup Your Data
The database is stored in `db.sqlite3` file. Back this up regularly:
1. Make a copy of `db.sqlite3`
2. Store it in a safe location or USB drive
3. Restore by replacing the file if needed

### Reset to Default
If something goes wrong, you can reset:
1. Close the server (Ctrl+C in the command window)
2. Delete `db.sqlite3`
3. Run `run.bat` again
4. Login with admin/admin123

### Change Admin Password
1. Go to `http://127.0.0.1:8000/admin/`
2. Click your username (admin) in top right
3. Click "Change password"
4. Enter new password and confirm

##  Stopping the Server

1. Click on the command window with the server
2. Press **Ctrl+C**
3. Type **Y** and press Enter to confirm
4. The window will close

## Data Structure

### Products
- Name, SKU, Category
- Purchase & Selling Price
- Current Stock Level
- Reorder Level Alert
- Profit Margin

### Customers
- Name, Phone, Email
- Address, City
- Creation Date
- Order History

### Orders
- Order Number (auto-generated)
- Customer Details
- Order Items (with quantity & price)
- Status (Pending/Confirmed/Completed/Cancelled)
- Discount, Tax, Total
- Notes

### Payments
- Order Reference
- Amount Paid
- Payment Method
- Transaction ID
- Payment Date


## Troubleshooting

### Problem: "Python not found"
- **Solution**: Install Python from https://www.python.org/
- Check "Add Python to PATH" during installation

### Problem: "Port 8000 is already in use"
- **Solution**: 
  1. Close other instances of the app
  2. Or edit `run.bat` and change `8000` to another number like `8001`

### Problem: "Cannot access http://127.0.0.1:8000"
- **Solution**:
  1. Make sure `run.bat` is still running
  2. Check that port 8000 is not blocked by firewall
  3. Try opening in a different browser

### Problem: "Database locked error"
- **Solution**:
  1. Close all browser tabs with the app
  2. Stop the server (Ctrl+C)
  3. Wait 30 seconds
  4. Restart with `run.bat`

### Problem: "Admin login not working"
- **Solution**:
  1. Stop the server (Ctrl+C)
  2. Delete `db.sqlite3`
  3. Run `run.bat` again
  4. Use admin/admin123

## 📞 Support

For issues:
1. Check the troubleshooting section above
2. Make sure Python is installed correctly
3. Ensure database file `db.sqlite3` exists
4. Check that no other process is using port 8000

## 📝 File Structure

```
shop_app/
├── db.sqlite3              # Database (contains all your data)
├── manage.py               # Django management script
├── run.bat                 # ✅ Use this to START the app
├── setup.bat               # Use this for initial setup
├── README.md               # This file
├── shop_app/
│   ├── settings.py         # Configuration
│   ├── urls.py             # URL routing
│   └── ...
├── inventory/              # Main app folder
│   ├── models.py           # Database models
│   ├── views.py            # Business logic
│   ├── forms.py            # Forms
│   ├── admin.py            # Admin configuration
│   └── urls.py             # App URLs
└── templates/              # HTML files
    ├── base.html           # Main template
    └── inventory/          # App templates
        ├── dashboard.html
        ├── product_*.html
        ├── customer_*.html
        ├── order_*.html
        ├── receipt.html
        └── ...
```

 Security Notes

- This application is designed for **offline use in a secure environment**
- Do NOT expose this on the internet without proper security setup
- Change default admin credentials
- Keep database backups in a safe location
- Do not share `db.sqlite3` file without encryption

 📄 License

This application is provided as-is for offline shop management.

 Enjoy Your Shop Management System!

Thank you for using Shop Manager. For best results:
- Regular data backups
- Keep the system on a dedicated computer
- Use strong passwords
- Follow all the documentation

---

**Version**: 1.0  
**Created**: 2024  
**Python**: 3.8+  
**Django**: 5.2.4  
**Database**: SQLite3
#   O f f l i n e - S h o p - A p p 
 
 
