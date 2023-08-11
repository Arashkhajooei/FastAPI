# FastAPI Warehouse Management System

This FastAPI application represents my implementation of a Warehouse Management System (WMS). Through this system, I've designed a platform to efficiently oversee products, deliveries, exits, and transactions within a warehouse setting. The foundation of this application is built upon the powerful combination of SQLAlchemy for seamless database interaction and Pydantic for ensuring robust data validation.

## Dependencies and Imports

The application starts with importing the required modules and libraries:

- **FastAPI**: This is the main module for creating the FastAPI application.
- **HTTPException**: This is used to raise HTTP exceptions with specific status codes and detail messages.
- **create_engine**: This is used to create a database engine using SQLAlchemy.
- **Column, Integer, String**, etc.: These are SQLAlchemy constructs for defining the database schema.
- **declarative_base**: This is used to create a base class for declarative models in SQLAlchemy.
- **sessionmaker**: This is used to create a session factory for creating database sessions.
- **relationship**: This is used to define relationships between tables in the database.
- **BaseModel**: This is used to define Pydantic models for data validation and serialization.
- **Optional, Union, List**: These are used to define types for function parameters.
- **date, datetime**: These are used for working with dates and times.

## Application Structure

The FastAPI Warehouse Management System is organized into several sections:

- **Imports and Dependencies**: I start by importing the necessary modules and libraries. These include FastAPI, SQLAlchemy, Pydantic, and more. These modules are crucial for building the web application, defining the database schema, handling data validation, and managing dependencies.
- **Creating the FastAPI App**: I create the FastAPI app using the FastAPI class. This app handles incoming HTTP requests, processes them, and generates appropriate responses.
- **SQLAlchemy Setup**: I configure the connection to the database in this section. I specify the URL for the database and create an SQLAlchemy engine. Additionally, I define a session factory called SessionLocal to handle individual database sessions.
- **Pydantic Models**: I use Pydantic models for data validation and serialization. These models define the structure and data types of various entities within the application, such as products, deliveries, exits, and transactions.
- **SQLAlchemy Models**: The SQLAlchemy models represent the database tables and their relationships. These models define the schema for storing information about products, suppliers, orders, deliveries, and other entities.
- **Creating Database Tables**: The SQLAlchemy models are used to create the corresponding database tables using the create_all method. This ensures that the database schema aligns with the application's model definitions.
- **Dependency for Database Session**: The get_db function serves as a dependency that provides a database session to the endpoint functions. This helps manage database connections and sessions efficiently.
- **Root Endpoint**: The root endpoint / is defined to provide a welcome message to users accessing the API.
- **Endpoints for CRUD Operations**: The application defines several endpoints for performing CRUD (Create, Read, Update, Delete) operations on different entities. These endpoints handle product creation, fetching products with deliveries, exiting products from the warehouse, delivering products to the warehouse, and fetching transaction records.

## Mechanisms

Here's how the FastAPI Warehouse Management System operates:

- **Product Creation**: Users can create new products by sending a POST request to /products/. This endpoint expects a JSON payload containing product information. Upon creation, the product details are stored in the database, and a corresponding delivery entry is created to mark the product's arrival in the warehouse.
- **Fetching Products with Deliveries**: Users can fetch a list of products along with their associated delivery details. They can specify date ranges using query parameters to filter the results to products delivered within a specific timeframe. The application retrieves the relevant data from the database and structures it for response.
- **Exiting Products from Warehouse**: Users can initiate the process of removing products from the warehouse by sending a POST request to /products/{product_id}/exit/. This decreases the quantity of the specified product in stock, creates a warehouse exit entry, and records a transaction.
- **Delivering Products to Warehouse**: Users can deliver products to the warehouse by sending a POST request to /products/{product_id}/deliver/. This increases the quantity of the specified product in stock, creates a warehouse entry, and records a transaction.
- **Fetching Product Transactions**: Users can fetch a list of transactions associated with a specific product by sending a GET request to /products/{product_id}/transactions/. The application retrieves the relevant transaction records from the database and returns them as a response.
