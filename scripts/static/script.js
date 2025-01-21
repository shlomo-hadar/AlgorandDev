document.addEventListener('DOMContentLoaded', () => {
    const walletIdEl = document.getElementById('wallet-id');
    const walletBalanceEl = document.getElementById('wallet-balance');
    const transactionListEl = document.getElementById('transaction-list');
    const itemListEl = document.getElementById('item-list');
    const cartTotalEl = document.getElementById('cart-total');
    const clearCartBtn = document.getElementById('clear-cart');
    const purchaseBtn = document.getElementById('purchase');

    let cart = {};

    const fetchWallet = () => {
        fetch('/api/wallet')
            .then(response => response.json())
            .then(data => {
                walletIdEl.textContent = data.id;
                walletBalanceEl.textContent = data.balance;
            });
    };

    const fetchTransactions = () => {
        transactionListEl.innerHTML = '';
        fetch('/api/transactions')
            .then(response => response.json())
            .then(data => {
                data.forEach((tx, index) => {
                    const li = document.createElement('li');
                    li.textContent = `"confirmed-round": ${tx['confirmed-round']}`;
                    li.style.cursor = 'pointer';
                    li.dataset.expanded = 'false'; // Initial collapsed state
                    li.addEventListener('click', () => toggleTransactionDetails(li, tx));
                    transactionListEl.appendChild(li);
                });
            });
    };

    const toggleTransactionDetails = (element, transaction) => {
        const expanded = element.dataset.expanded === 'true';
        if (expanded) {
            element.textContent = `"confirmed-round": ${transaction['confirmed-round']}`;
            element.dataset.expanded = 'false';
        } else {
            element.textContent = JSON.stringify(transaction, null, 2);
            element.style.whiteSpace = 'pre-wrap'; // Preserve JSON formatting
            element.dataset.expanded = 'true';
            openTransactionInNewTab(transaction); // Only open new tab when expanding
        }
    };

    const openTransactionInNewTab = (transaction) => {
        const newTab = window.open();
        const pre = newTab.document.createElement('pre');
        pre.textContent = JSON.stringify(transaction, null, 2);
        newTab.document.body.appendChild(pre);
        newTab.document.title = `Transaction ${transaction['confirmed-round']}`;
    };

    const fetchItems = () => {
        fetch('/api/items')
            .then(response => response.json())
            .then(data => {
                itemListEl.innerHTML = '';
                data.forEach((item, index) => {
                    const itemDiv = document.createElement('div');
                    itemDiv.classList.add('item');
                    itemDiv.innerHTML = `
                        <p>${item.name} - ${item.price}</p>
                        <button data-index="${index}" data-action="-1">-</button>
                        <input type="text" id="item-${index}" value="0" readonly />
                        <button data-index="${index}" data-action="1">+</button>
                    `;
                    itemListEl.appendChild(itemDiv);
                });

                // Add event listeners to buttons
                itemListEl.querySelectorAll('button').forEach(button => {
                    button.addEventListener('click', (e) => {
                        const index = e.target.dataset.index;
                        const action = parseInt(e.target.dataset.action);
                        updateCart(index, action);
                    });
                });
            });
    };

    const updateCart = (itemIndex, quantity) => {
        cart[itemIndex] = (cart[itemIndex] || 0) + quantity;
        cart[itemIndex] = Math.max(0, cart[itemIndex]);
        document.getElementById(`item-${itemIndex}`).value = cart[itemIndex];
        calculateTotal();
    };

    const calculateTotal = () => {
        fetch('/api/items')
            .then(response => response.json())
            .then(items => {
                let total = 0;
                for (let index in cart) {
                    total += cart[index] * items[index].price;
                }
                cartTotalEl.textContent = total;
            });
    };

    const clearCart = () => {
        cart = {};
        document.querySelectorAll('input[id^="item-"]').forEach(input => (input.value = 0));
        calculateTotal();
    };

    const handlePurchase = () => {
        fetch('/api/purchase', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(cart),
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Purchase successful!');
                    clearCart();
                    fetchWallet();
                    fetchTransactions();
                } else {
                    alert('Purchase failed: ' + data.error);
                }
            });
    };

    clearCartBtn.addEventListener('click', clearCart);
    purchaseBtn.addEventListener('click', handlePurchase);

    // Initial data fetch
    fetchWallet();
    fetchTransactions();
    fetchItems();
});
