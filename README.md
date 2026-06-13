# E-Commerce Database System

A comprehensive E-Commerce Database Management System with customer management, product catalog, order processing, payment tracking, and automated inventory management using MySQL.

## Features

- Customer Management (20+ records)
- Product Catalog with 5 Categories (20+ products)
- Order Processing System
- Payment Tracking (UPI, Card, Cash)
- Stock Management with Automatic Updates
- Invoice Generation via Stored Procedures

## SQL Queries Implemented

1. Retrieve all products
2. Display products by specific category
3. Order and customer details (2-table JOIN)
4. Order, customer, and product details (3-table JOIN)
5. Count products per category (GROUP BY)
6. Categories with more than 3 products (HAVING)
7. Products above average price (Subquery)
8. Customers with more orders than specific customer (Correlated Subquery)
9. All customers including those with no orders (LEFT JOIN)
10. Products never ordered (NOT EXISTS)

## Stored Procedures

- **PlaceOrder** - Creates new order with automatic price calculation
- **GenerateInvoice** - Generates complete invoice for an order

## Triggers

- **update_stock** - Automatically reduces product stock after order
- **prevent_insufficient_purchase** - Prevents order if stock insufficient

## Sample Data Statistics

- Customers: 20 records
- Categories: 5 categories  
- Products: 20 products
- Orders: 20+ sample orders
- Payments: 20+ payment records

## Getting Started

1. Create database: `CREATE DATABASE EcommerceSystem;`
2. Run the complete SQL script to create tables, insert data, procedures, and triggers
3. Test queries and procedures

## Sample Queries

```sql
-- Get all electronics products
SELECT * FROM Product WHERE category_id = 101;

-- Get customer order summary
SELECT c.name, COUNT(o.order_id) as total_orders
FROM Customer c
JOIN Orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;

-- Place a new order
CALL PlaceOrder(404, 304, 1, 202, 2);

-- Generate invoice
CALL GenerateInvoice(301);
