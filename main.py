from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship,Session
from pydantic import BaseModel
from typing import Optional,Union,List
from datetime import date,datetime

# Create the FastAPI app
app = FastAPI()

# SQLAlchemy setup
DATABASE_URL = "sqlite:///./store.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ProductBase(BaseModel):
    product_name: str
    description: str
    category_id: int
    supplier_id: int
    quantity_in_stock: int
    date_added: datetime
    warehouse_id: int
    unit_price: float


class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    product_id: int
    warehouse_id: Optional[int]

    class Config:
        from_orm = True

class SupplierBase(BaseModel):
    supplier_name: str
    contact_information: str
    address: str

class SupplierCreate(SupplierBase):
    pass

class Supplier(SupplierBase):
    supplier_id: int

    class Config:
        from_orm = True

class OrderBase(BaseModel):
    order_date: datetime
    customer_name: str
    customer_contact: str
    total_amount: float

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    order_id: int

    class Config:
        from_orm = True

class OrderDetailsBase(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    subtotal: float

class OrderDetailsCreate(OrderDetailsBase):
    pass

class OrderDetails(OrderDetailsBase):
    order_detail_id: int

    class Config:
        from_orm = True

class WarehouseEntryBase(BaseModel):
    product_id: int
    entry_date_time: datetime
    quantity_entered: int
    entered_by: str
    historical: bool
    warehouse_id: int

class WarehouseEntryCreate(WarehouseEntryBase):
    pass

class WarehouseEntry(WarehouseEntryBase):
    entry_id: int

    class Config:
        from_orm = True

class WarehouseExitBase(BaseModel):
    product_id: int
    exit_date_time: datetime
    quantity_exited: int
    exited_by: str
    recipient_name: str
    recipient_contact: str
    historical: bool
    warehouse_id: int

class WarehouseExitCreate(WarehouseExitBase):
    pass

class WarehouseExit(WarehouseExitBase):
    exit_id: int

    class Config:
        from_orm = True

class DeliveryBase(BaseModel):
    order_id: int
    delivery_date_time: datetime
    delivered_by: str
    recipient_name: str
    recipient_contact: str

class DeliveryCreate(DeliveryBase):
    pass
class DeliveryCreate(BaseModel):
    delivery_date_time: datetime
    delivered_by: str
    recipient_name: str
    recipient_contact: str

class Delivery(DeliveryBase):
    delivery_id: int

    class Config:
        from_orm = True

class TransactionBase(BaseModel):
    transaction_date_time: datetime
    product_id: int
    transaction_type: str
    quantity: int
    related_id: int

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    transaction_id: int

    class Config:
        from_orm = True

class CategoryBase(BaseModel):
    category_name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    category_id: int

    class Config:
        from_orm = True

class WarehouseDetailBase(BaseModel):
    location_name: str
    address: str
    contact_information: str

class WarehouseDetailCreate(WarehouseDetailBase):
    pass

class WarehouseDetail(WarehouseDetailBase):
    warehouse_id: int

    class Config:
        from_orm = True




# SQLAlchemy models
class ProductModel(Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, index=True)
    description = Column(String)
    category_id = Column(Integer, ForeignKey("categories.category_id"))
    supplier_id = Column(Integer, ForeignKey("suppliers.supplier_id"))
    quantity_in_stock = Column(Integer)
    unit_price = Column(Float)
    date_added = Column(DateTime, default=datetime.utcnow)
    warehouse_id = Column(Integer, ForeignKey("warehouses.warehouse_id"))
    deliveries = relationship("DeliveryModel", back_populates="product")
    category = relationship("CategoryModel", back_populates="products")
    supplier = relationship("SupplierModel", back_populates="products")
    warehouse = relationship("WarehouseDetailModel", back_populates="products")
    exits = relationship("WarehouseExitModel", back_populates="product")
    entries = relationship("WarehouseEntryModel", back_populates="product")
    transactions = relationship("TransactionModel", back_populates="product")

class SupplierModel(Base):
    __tablename__ = "suppliers"
    supplier_id = Column(Integer, primary_key=True, index=True)
    supplier_name = Column(String, index=True)
    contact_information = Column(String)
    address = Column(String)

    products = relationship("ProductModel", back_populates="supplier")

class OrderModel(Base):
    __tablename__ = "orders"
    order_id = Column(Integer, primary_key=True, index=True)
    order_date = Column(DateTime, index=True)
    customer_name = Column(String)
    customer_contact = Column(String)
    total_amount = Column(Float)

    order_details = relationship("OrderDetailsModel", back_populates="order")
    deliveries = relationship("DeliveryModel", back_populates="order")  # Add this line

class OrderDetailsModel(Base):
    __tablename__ = "order_details"
    order_detail_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"))
    product_id = Column(Integer, ForeignKey("products.product_id"))
    quantity = Column(Integer)
    subtotal = Column(Float)

    order = relationship("OrderModel", back_populates="order_details")

class WarehouseEntryModel(Base):
    __tablename__ = "warehouse_entries"
    entry_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"))
    entry_date_time = Column(DateTime, index=True)
    quantity_entered = Column(Integer)
    entered_by = Column(String)
    historical = Column(Boolean)
    warehouse_id = Column(Integer, ForeignKey("warehouses.warehouse_id"))
    product = relationship("ProductModel", back_populates="entries")

class WarehouseExitModel(Base):
    __tablename__ = "warehouse_exits"
    exit_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"))
    exit_date_time = Column(DateTime, index=True)
    quantity_exited = Column(Integer)
    exited_by = Column(String)
    recipient_name = Column(String)
    recipient_contact = Column(String)
    historical = Column(Boolean)
    warehouse_id = Column(Integer, ForeignKey("warehouses.warehouse_id"))
    product = relationship("ProductModel", back_populates="exits")

class DeliveryModel(Base):
    __tablename__ = "deliveries"
    delivery_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"))
    delivery_date_time = Column(DateTime, index=True)
    delivered_by = Column(String)
    recipient_name = Column(String)
    recipient_contact = Column(String)
    delivered_by = Column(String)
    recipient_name = Column(String)

    # Add the relationship to ProductModel
    product_id = Column(Integer, ForeignKey("products.product_id"))
    product = relationship("ProductModel", back_populates="deliveries")
    order = relationship("OrderModel", back_populates="deliveries")  # Add this line

class TransactionModel(Base):
    __tablename__ = "transactions"
    transaction_id = Column(Integer, primary_key=True, index=True)
    transaction_date_time = Column(DateTime, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"))
    transaction_type = Column(String)
    quantity = Column(Integer)
    related_id = Column(Integer)
    transaction_description = Column(String)
    product_id = Column(Integer, ForeignKey("products.product_id"))
    product = relationship("ProductModel", back_populates="transactions")


class CategoryModel(Base):
    __tablename__ = "categories"
    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String, index=True)

    products = relationship("ProductModel", back_populates="category")

class WarehouseDetailModel(Base):
    __tablename__ = "warehouses"
    warehouse_id = Column(Integer, primary_key=True, index=True)
    location_name = Column(String, index=True)
    address = Column(String)
    contact_information = Column(String)

    products = relationship("ProductModel", back_populates="warehouse")

# Create the tables in the database
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoints for CRUD operations
@app.get('/', tags=["Root"])
def read_root():
    return {"message": "Welcome to the Warehouse API"}

#Example endpoint to create a product
# @app.post("/products/", response_model=Product)
# def create_product(product: ProductBase, db: Session = Depends(get_db)):
#     db_product = ProductModel(**product.dict())
#     db.add(db_product)
#     db.commit()
#     db.refresh(db_product)
#     return db_product


@app.post("/products/", response_model=Product)
def create_product(product: ProductCreate, delivery_info: DeliveryCreate, db: Session = Depends(get_db)):
    try:
        # Create the product in the database
        db_product = ProductModel(**product.dict())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)

        # Create the delivery entry for the product
        delivery = DeliveryModel(
            order_id=0,  # Assuming this is a placeholder value for the order_id
            delivery_date_time=delivery_info.delivery_date_time,
            delivered_by=delivery_info.delivered_by,
            recipient_name=delivery_info.recipient_name,
            recipient_contact=delivery_info.recipient_contact,
            product_id=db_product.product_id
        )
        db.add(delivery)
        db.commit()

        transaction = TransactionModel(
            transaction_date_time=datetime.utcnow(),
            product_id=db_product.product_id,
            transaction_type="addition",
            quantity=product.quantity_in_stock,
            related_id=db_product.product_id
        )
        db.add(transaction)
        db.commit()

        return db_product

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@app.get("/products/", response_model=List[Product])
def get_products_by_dates(
    start_date: datetime = Query(None),
    end_date: datetime = Query(None),
    db: Session = Depends(get_db)
):
    try:
        # Convert the dates to strings in the format of your 'date_added' field
        start_date_str = start_date.strftime('%Y-%m-%d %H:%M:%S') if start_date else None
        end_date_str = end_date.strftime('%Y-%m-%d %H:%M:%S') if end_date else None

        # Query the products with date_added between the specified start_date and end_date
        products_with_deliveries = db.query(ProductModel, DeliveryModel).\
            join(DeliveryModel, ProductModel.product_id == DeliveryModel.product_id).\
            filter(DeliveryModel.delivery_date_time.between(start_date_str, end_date_str)).all()

        # Create a list to store the response data
        result = []

        # Iterate through the products and extract the relevant data
        for product, delivery in products_with_deliveries:
            product_data = {
                "product_id": product.product_id,
                "product_name": product.product_name,
                "description": product.description,
                "category_id": product.category_id,
                "supplier_id": product.supplier_id,
                "quantity_in_stock": product.quantity_in_stock,
                "date_added": product.date_added,
                "warehouse_id": product.warehouse_id,
                "unit_price": product.unit_price,
                "delivery_date_time": delivery.delivery_date_time,
                "delivered_by": delivery.delivered_by,
                "recipient_name": delivery.recipient_name,
                "recipient_contact": delivery.recipient_contact,
            }
            result.append(product_data)

        # Return the products with delivery and recipient information
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/products/{product_id}/exit/", response_model=Product)
def exit_product(
    product_id: int,
    quantity_exited: int,
    exited_by: str,
    recipient_name: str,
    recipient_contact: str,
    db: Session = Depends(get_db)
):
    try:
        # Get the product from the database
        product = db.query(ProductModel).filter(ProductModel.product_id == product_id).first()

        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")

        # Check if there's enough quantity to exit
        if product.quantity_in_stock < quantity_exited:
            raise HTTPException(status_code=400, detail="Insufficient quantity in stock")

        # Update the quantity_in_stock
        product.quantity_in_stock -= quantity_exited

        # Create a new warehouse exit entry
        db_exit = WarehouseExitModel(
            product_id=product_id,
            exit_date_time=datetime.utcnow(),
            quantity_exited=quantity_exited,
            exited_by=exited_by,
            recipient_name=recipient_name,
            recipient_contact=recipient_contact,
            historical=False,
            warehouse_id=product.warehouse_id
        )
        db.add(db_exit)
        db.commit()
        db.refresh(db_exit)

        transaction = TransactionModel(
            transaction_date_time=datetime.utcnow(),
            product_id=product_id,
            transaction_type="exit",
            quantity=quantity_exited,
            related_id=db_exit.exit_id
        )
        db.add(transaction)
        db.commit()

        # Update the product with the new quantity_in_stock
        db.commit()

        return product

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/products/{product_id}/deliver/", response_model=Product)
def deliver_product(
    product_id: int,
    quantity_delivered: int,
    delivered_by: str,
    recipient_name: str,
    recipient_contact: str,
    db: Session = Depends(get_db)
):
    try:
        # Get the product from the database
        product = db.query(ProductModel).filter(ProductModel.product_id == product_id).first()

        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")

        # Update the quantity_in_stock
        product.quantity_in_stock += quantity_delivered

        # Create a new warehouse entry
        db_entry = WarehouseEntryModel(
            product_id=product_id,
            entry_date_time=datetime.utcnow(),
            quantity_entered=quantity_delivered,
            entered_by=delivered_by,
            historical=False,
            warehouse_id=product.warehouse_id
        )
        db.add(db_entry)
        db.commit()
        db.refresh(db_entry)

        # Create a delivery transaction
        transaction = TransactionModel(
            transaction_date_time=datetime.utcnow(),
            product_id=product_id,
            transaction_type="delivery",
            quantity=quantity_delivered,
            related_id=db_entry.entry_id
        )
        db.add(transaction)
        db.commit()
        # Update the product with the new quantity_in_stock
        db.commit()

        return product

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/products/{product_id}/transactions/", response_model=List[Transaction])
def get_product_transactions(product_id: int, db: Session = Depends(get_db)):
    try:
        # Query transactions for the given product_id
        transactions = db.query(TransactionModel).filter(TransactionModel.product_id == product_id).all()
        return transactions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))