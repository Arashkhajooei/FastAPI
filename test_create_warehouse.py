import requests

# Replace this URL with your actual API URL
base_url = "http://localhost:8000"

def create_goods_transaction():
    endpoint = "/transactions/"
    url = base_url + endpoint

    # Sample data for a new transaction
    data = {
        "product_name": "Product X",
        "transaction_type": "entry",
        "quantity": 100
    }

    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("Transaction created successfully!")
        print(response.json())
    else:
        print("Error creating transaction:")
        print(response.json())

def read_root():
    endpoint = "/"
    url = base_url + endpoint

    response = requests.get(url)
    if response.status_code == 200:
        print("Root endpoint response:")
        print(response.json())
    else:
        print("Error accessing root endpoint:")
        print(response.json())


if __name__ == "__main__":
    read_root()
    create_goods_transaction()
