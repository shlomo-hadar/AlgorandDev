# AlgoZon

**AlgoZon** is a simple Flask-based sandbox application, intended for educational and testing purposes only, that demonstrates how to integrate the [Algorand](https://www.algorand.com/) blockchain into an e-commerce-like platform. Users can view their wallet balance, see past transactions, add items to a cart, and simulate a purchase by transacting on the Algorand network.

## Table of Contents

1. [Overview](#overview)
2. [Folder Structure](#folder-structure)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Endpoints](#endpoints)
7. [Notes and Customization](#notes-and-customization)
8. [License](#license)

---

## Overview

This project demonstrates the following:

- **Flask Server (Python):** Serves the web application, processes API requests, and primarily orchestrates payment and transaction flows on the Algorand blockchain. This is the core functionality of the project.
- **HTML (index.html)**: The main layout of the web application, containing sections for wallet info, transactions, and items for purchase.
- **JavaScript (script.js)**: Dynamically fetches data from the Flask server, displays transactions and balances, and allows users to add/remove items from a cart before purchasing.

---

## Folder Structure

A typical layout might look like this:

```
├── static
│   ├── style.css       # (Optional) CSS file for styling
│   ├── script.js       # JavaScript file with event listeners and API calls
├── templates
│   └── index.html      # The main HTML template for rendering the page
├── app.py              # Flask server implementation (Python)
├── README.md           # This README file
└── requirements.txt    # Python dependencies (if you choose to create it)
```

> **Note**: Your actual project structure might differ slightly. The key is ensuring that Flask can serve `index.html` from the `templates` directory, and your static files (CSS, JS) are in a `static` directory.

---

## Prerequisites

1. **Python 3.10+**

   - [Download Python](https://www.python.org/downloads/)

2. **pip**

   - Usually included with Python. Run `pip --version` to check.

3. **Algorand Sandbox** (for local development)
   - You need a running Algorand node sandbox environment if you want to interact with a local Algorand network.
   - [Algorand Sandbox](https://github.com/algorand/sandbox)

---

## Installation

1. **Clone or Download** this repository:

   ```bash
   git clone https://github.com/shlomo-hadar/AlgorandDev.git
   cd AlgorandDev
   ```

2. **Install Dependencies**:
   Run:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Algorand Node (Optional)**:
   - Update the following variables in `app.py` with your own Algorand node details:
     ```python
     ALGOD_ADDRESS = "http://localhost:4001"
     ALGOD_TOKEN = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
     ```
   - Update the `SENDER_ADDRESS`, `RECEIVER_ADDRESS`, and `SENDER_MNEMONIC` as needed to reflect your accounts.

---

## Usage

1. **Start the Flask Application**:

   ```bash
   python app.py
   ```

   By default, Flask runs on `http://127.0.0.1:5000`.

2. **Access the Web App**:

   - Open your browser to [http://127.0.0.1:5000](http://127.0.0.1:5000).

3. **Explore the Application**:

   - **Wallet Section**: Displays the wallet ID and balance associated with `SENDER_ADDRESS`.
   - **Transactions Section**: Shows a list of recent transactions. Clicking a transaction toggles between a concise and detailed view.
   - **Items Section**: A list of items you can “purchase.” Press the `+` or `-` buttons to adjust the quantity in your cart.
   - **Cart Summary**: Shows the total cost of the selected items. Clicking **Purchase** attempts an Algorand payment transaction.

4. **Check Output**:
   - The balance of the wallet updates if the transaction is successful.

---

## Endpoints

The Flask server exposes the following endpoints:

- **`GET /api/wallet`**  
  Returns the wallet ID (`SENDER_ADDRESS`) and its current balance.

- **`GET /api/transactions`**  
  Returns a list of transaction objects recorded by the app.

- **`GET /api/items`**  
  Returns a JSON array of items available for purchase. Example:

  ```json
  [
    { "name": "Hedwig Pop", "price": 10000000000.0 },
    { "name": "Triangles Toaster", "price": 20000000000.0 }
  ]
  ```

- **`POST /api/purchase`**  
  Attempts to make a transaction on the Algorand network for the total cart cost.  
  The JSON request body should be a dictionary of item indexes and quantities:

  ```json
  {
    "0": 2,
    "3": 1
  }
  ```

  Returns a JSON object indicating success or failure and the new wallet balance.

- **`GET /`**  
  Renders `index.html` as the main landing page.

---

## Notes and Customization

1. **Algorand Node**

   - Ensure `ALGOD_ADDRESS` and `ALGOD_TOKEN` are correct for your node setup.
   - If will most surely have a different token, address, or port.

2. **Transaction Parameters**

   - The transaction fee, suggested parameters, or note fields may be customized in the `make_txn` function inside `app.py`.

3. **Item Prices**

   - In `app.py`, the `items` list has very large price values (in microAlgos or Algos). Adjust as needed.

4. **Mock Data**
   - The transaction list is initially empty. On each purchase, new transaction data is appended.
   - Real-world scenarios would record transactions in a database.

---
