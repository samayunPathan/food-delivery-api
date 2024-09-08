# Food Delivery API with Django Rest Framework

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
   - [User Authentication and Authorization](#user-authentication-and-authorization)
   - [Restaurant Management](#restaurant-management)
   - [Order Management](#order-management)
   - [Menu Details](#menu-details)
3. [Technology Stack](#technology-stack)
4. [System Requirements](#system-requirements)
5. [Setup Instructions](#setup-instructions)
   - [Step 1: Clone the Repository](#step-1-clone-the-repository)
   - [Step 2: Create and Activate a Virtual Environment](#step-2-create-and-activate-a-virtual-environment)
   - [Step 3: Install Dependencies](#step-3-install-dependencies)
   - [Step 4: Configure Environment Variables](#step-4-configure-environment-variables)
   - [Step 5: Apply Migrations](#step-5-apply-migrations)
   - [Step 6: Create a Superuser](#step-6-create-a-superuser)
   - [Step 7: Run the Development Server](#step-7-run-the-development-server)
   - [Step 8: Add a Restaurant](#step-8-add-a-restaurant)
   - [Step 9: Swagger API Documentation](#step-9-swagger-api-documentation)
6. [API Endpoints](#api-endpoints)
   - [User Registration and Authentication](#user-registration-and-authentication)
   - [Restaurant Management](#restaurant-management)
   - [Order Management](#order-management)
7. [Database Design](#database-design)
   - [Key Relationships](#key-relationships)
8. [Future Enhancements](#future-enhancements)

## Project Overview

This is a **Food Delivery API** built with Django Rest Framework. It provides functionality for managing multiple restaurants, handling user registration and authentication, managing menus, and placing orders. The project adheres to DRY and SOLID principles and includes role-based access control for restaurant owners and employees.

## Features

1. **User Authentication and Authorization**:
   - Custom user roles: **Owner** and **Employee**.
   - Permission checks for creating, modifying, and viewing menu items, categories, and modifiers.
   - Token-based authentication (non-JWT) with user details returned upon registration and login.
   
2. **Restaurant Management**:
   - APIs for owners and employees to create menus, menu items, categories, and modifiers.
   - Role-based access ensures that only authorized users can modify or view menu items.

3. **Order Management**:
   - API for placing orders with support for payment methods (card or cash).
   - User can view menus and place orders directly.
   
4. **Menu Details**:
   - API provides menu details, including items, categories, and modifiers.

## Technology Stack

- **Backend Framework**: Django, Django Rest Framework
- **Database**: PostgreSQL (recommended) or SQLite (for development)
- **Authentication**: Django's built-in token authentication
- **Python Version**: Latest version of Python 3.x
- **Django Version**: Latest version of Django
- **Other Dependencies**: `djangorestframework`, `django-environ`, `psycopg2` (PostgreSQL support)

## System Requirements

1. Python 3.x
2. Django (latest)
3. PostgreSQL (recommended for production)

## Setup Instructions

### Step 1: Clone the Repository

```bash
git clone https://github.com/samayunPathan/food-delivery-api.git
```
```bash
cd food-delivery-api
```
### Step 2: Create and Activate a Virtual Environment
```bash 
python3 -m venv venv # On Windows: python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```
### Step 4: Configure Environment Variables

> [!NOTE]
>  Create postgresql database.
> Create `.env` file in your ** project directory with the following content:
This GitHub repo includes a `.env.sample` file for better maintainability.
  
```bash
host=localhost
port=port
dbname=db_name
user=db_user
password=db_password
```

### Step 5: Apply Migrations
```bash 
python manage.py makemigrations
python manage.py migrate
```
### Step 6: Create a Superuser
```bash
python manage.py createsuperuser
```
### Step 7: Run the Development Server
```bash
python manage.py runserver
```
The API should now be available at http://127.0.0.1:8000/.
### Step 8: Add a Restaurant
After creating the superuser, you must first create a restaurant in the database.
Only after adding a restaurant can users register under it.

Log in to the Django Admin panel (http://127.0.0.1:8000/admin/) using your superuser account.
Navigate to the Restaurants section and add your first restaurant.
### Step 9: Swagger API Documentation
Visit the following URL to access the Swagger OpenAPI documentation for exploring available endpoints:
http://127.0.0.1:8000/swagger/
## API Endpoints 

### User Registration and Authentication

#### Register a new user
**Users can only register under an existing restaurant.Super user first add restaurant and that restaurant id user will get from superuser then user can register as owner or employee under that restaurant.**
- **POST** `/user/register/`- Registers a new user.


#### Login
- **POST** `/user/login/` - Authenticates a user and returns tokens.


---

### Restaurant Management

#### List and Create Restaurants
- **GET** `/restaurants/restaurants/` - Lists all restaurants.
- **POST** `/restaurants/restaurants/` - Creates a new restaurant (Owner or Employee only).

#### List and Create Menus
- **GET** `/restaurants/menus/` - Lists all menus for restaurants.
- **POST** `/restaurants/menus/` - Creates a new menu (Owner or Employee only).

#### List and Create Categories
- **GET** `/restaurants/categories/` - Lists all categories for menus.
- **POST** `/restaurants/categories/` - Creates a new category (Owner or Employee only).

#### List and Create Menu Items
- **GET** `/restaurants/menu-items/` - Lists all menu items.
- **POST** `/restaurants/menu-items/` - Creates a new menu item (Owner or Employee only).

#### List and Create Modifiers
- **GET** `/restaurants/modifiers/` - Lists all modifiers for menu items.
- **POST** `/restaurants/modifiers/` - Creates a new modifier (Owner or Employee only).

---

### Order Management

#### List and Create Orders
- **GET** `/orders/orders/` - Lists all orders for a user.
- **POST** `/orders/orders/` - Creates a new order (payment by card or cash).

#### View Order Detail
- **GET** `/orders/orders/<int:pk>/` - Retrieves the details of a specific order.

---
## Database Design

The following diagram outlines the database architecture for the system:
```
+---------------------------------+              +-----------------------------------+
|              User               |              |           Restaurant             |
|---------------------------------|              |-----------------------------------|
| id (PK)                         |              | id (PK)                           |
| username (Unique)               |              | name (Unique)                     |
| email (Unique)                  |              | address (Text)                    |
| is_owner (Boolean)              | <---------+  | owner_id (FK)                     |
| is_employee (Boolean)           |              |                                   |
| restaurant_id (FK)              |              +-----------------------------------+
| groups (M2M)                    |
| user_permissions (M2M)          |
+---------------------------------+                            |
                                                                |
                          1                                    (has many)
                          |                                      |
                         (can have multiple restaurants)         |
                          |                                      v
                          |                                
+---------------------------------+              +-----------------------------------+
|             Menu                |              |          Category                |
|---------------------------------|              |-----------------------------------|
| id (PK)                         |              | id (PK)                          |
| name (Text)                     |              | name (Text)                      |
| restaurant_id (FK)              | <---------+  | menu_id (FK)                     |
+---------------------------------+              +-----------------------------------+
                          |
                          |
                         (has many)
                          |
                          v
+---------------------------------+              +-----------------------------------+
|          MenuItem               |              |            Modifier              |
|---------------------------------|              |-----------------------------------|
| id (PK)                         |              | id (PK)                          |
| name (Text)                     |              | name (Text)                      |
| description (Text)              |              | price (Decimal)                  |
| price (Decimal)                 |              | menu_item_id (FK)                |
| category_id (FK)                |              +-----------------------------------+
+---------------------------------+
                          |
                          |
                         (has many)
                          |
                          v
+---------------------------------+              +-----------------------------------+
|             Order               |              |           OrderItem              |
|---------------------------------|              |-----------------------------------|
| id (PK)                         |              | id (PK)                          |
| user_id (FK)                    |              | order_id (FK)                    |
| restaurant_id (FK)              |              | menu_item_id (FK)                |
| total_amount (Decimal)          |              | quantity (Integer)               |
| payment_method (Text)           |              +-----------------------------------+
| created_at (DateTime)           |
| updated_at (DateTime)           |
+---------------------------------+

```
#### Key Relationships:
- User and Restaurant: A User can own or be associated with multiple Restaurants (via the restaurant_id foreign key in the User table).
- Restaurant and Menu: Each Restaurant has multiple Menus, and each Menu is linked to one Restaurant.
- Menu and Category: A Menu has multiple Categories, and each Category belongs to one Menu.
- Category and MenuItem: Each Category contains multiple MenuItems, and each MenuItem belongs to a Category.
- MenuItem and Modifier: A MenuItem can have multiple Modifiers (add-ons like toppings, etc.).
- Order and MenuItem: An Order contains multiple MenuItems via the OrderItem table, which tracks the items and their quantities.
- OrderItem: Links each Order to its corresponding MenuItem and the quantity of that item in the order.

## Future Enhancements
- Implement JWT authentication for better scalability.
- Add real-time notifications for order status using WebSockets.
- Implement additional payment gateways for more options.



