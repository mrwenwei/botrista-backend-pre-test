# flask-backend-sample
Create an API service using Python with sqlite and Flask.

API document was written in swagger.

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
DB queries are utilized by ORM package `SQLAlchemy`

<img width="600" alt="截圖 2024-06-30 下午5 00 56" src="https://github.com/mrwenwei/botrista-backend-pre-test/assets/11289450/335e2539-9498-4c54-a09e-e85a1e413a8d">


## API Documentation

Written in http://127.0.0.1:8080/apidocs

## API Usage

All the APIs can be called on swagger.

1. Create account
    ```HTTP
    POST /signup

    Body:
    {
      "password": "string",
      "permission": 0 or 1,
      "username": "string"
    }
    ```
    Create customer (permission=0) or manager (permission=1) by using this endpoint.

2. Login and Logout
    ```HTTP
    POST /login
    ```
    Login with the username and password. After successfully login, API will return login token (To simplify the mechanism here I use `user_id`) in response and service will cache the user for 600 seconds. After 600s the user needs to login again.

   ```HTTP
   POST /logout

   Authentication:
   token
   ```

4. Manager create product
    ```HTTP
    POST /product

    Body:
    {
        "name": "string",
        "price": float,
        "stock": integer
    }

    Authentication:
    token
    ```
    Create unique name product with manager logged in token (user_id). 

    After successfully created product, it will return the `product_id` in response.

5. Manager update/delete product
    ```HTTP
    PUT /product

    Parameter:
    product_id

    Body (optional, you can edit any of it):
    {
        "name": "string",
        "price": float,
        "stock": integer
    }

    Authentication:
    token
    ```

    ```HTTP
    DELETE /product

    Parameter:
    product_id

    Authentication:
    token
    ```
    The product can not be deleted if there exists any order of the product.

6. Get product info (logged in required)
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

7. Customer create order

    ```HTTP
    POST /order

    Body:
    [
        {
            "product_id": integer,
            "quantity": positive integer
        }
    ]

    Authentication:
    token
    ```
    Multiple products can be assigned. If the product exists and the stock is enough, then the order will be created sucessfully. 

8. Get order list
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
