# botrista-backend-pre-test
Create an API service using Python with sqlite and Flask.

API document has been written in swagger.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [DB diagram](#db-diagram)
- [API Documentation](#api-documentation)
- [API usage](#api-usage)

## Features

- Sign-up/log-in a role user (customer and manager)
  - Logged in user would become expired in 600 senconds
  - Permission:
    - 0: Customer
    - 1: Manager
- Product management (manager permission)
  - CRUD of product (product can only be deleted when there is no its order)
- Order management
  - Create orders (customer permission)
  - Retrieve order list

## Installation

1. Clone this repository to your local machine:
    ```sh
    git clone git@github.com:mrwenwei/botrista-backend-pre-test.git
    cd botrista-backend-pre-test
    ```

2. Run in docker:
    ```sh
    docker-compose up --build
    ```

3. Open the document url http://127.0.0.1:8080/apidocs

## DB diagram


## API Documentation

Written in http://127.0.0.1:8080/apidocs

## API Usage

All the apis can be called on swagger.

1. Create account
    ```
    /POST signup
    ```
    Create customer (permission=0) or manager (permission=1) by using this endpoint.

2. Login
    ```
    /POST login
    ```
    Login with the username and password. After successfully login, API will return login token (user_id) in response and service will cache the user for 600 seconds. After 600s user needs to login again.

3. Manager create product
    ```HTTP
    /POST product

    Body:
    {
        "name": "Iphone 16",
        "price": 999.99,
        "stock": 10
    }

    Authentication:
    token
    ```
    Create unique name product with manager logged in token (user_id). 

    After successfully created product, it will return the `product_id` in response.

4. Manager update/delete product
    ```HTTP
    /PUT product

    Parameter:
    product_id

    Body (optional, you can edit any of it):
    {
        "name": "Iphone 16",
        "price": 999.99,
        "stock": 10
    }

    Authentication:
    token
    ```

    ```HTTP
    /DELETE product

    Parameter:
    product_id

    Authentication:
    token
    ```
    The product can not be deleted if there exists any order of the product.

5. Get product info (logged in required)
    Get specific product
    ```HTTP
    GET /product

    Parameter:
    product_id

    Authentication:
    token
    ```

    Get all filtered products
    ```HTTP
    GET /products

    Parameters: (optional)
    price_lower_bound
    price_upper_bound
    stock_lower_bound
    stock_upper_bound
    ```

6. Customer create order

    ```HTTP
    POST /order

    Body:
    [
        {
            "product_id": 1,
            "quantity": 3
        }
    ]

    Authentication:
    token
    ```
    Multiple products can be assigned. If the product exists and the stock is enough, then the order will be created sucessfully. 

7. Get order list
    If you are a customer, you will get your orders only.
    If you are a manager, you could get all orders that created by customers.
    ```HTTP
    GET /orders

    Parameters: (optional)
    order_id
    product_id

    Authentication:
    token
    ```