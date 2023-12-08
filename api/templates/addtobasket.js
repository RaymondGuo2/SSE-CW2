document.querySelector('.btn-primary').addEventListener('click', addToCart);

function addToCart() {
    const size = document.getElementById('size').value;
    const quantity = document.getElementById('quantity').value;
    const price = document.getElementById('price').textContent; // Or calculate based on currency
    const productInfo = { size, quantity, price };
    
    fetch('/add-to-cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(productInfo),
    })
    .then(response => response.json())
    .then(data => {

        console.log(data);
        if(data.status === 'success') {
            alert('Product added to cart!');
        }
    })
    .catch(error => {
        console.error('Error adding product to cart:', error);
    });
}





<script>
function updatePriceDisplay(price, currencySymbol) {
    document.getElementById('price').innerText = price.toFixed(2);
    document.getElementById('currency-symbol').innerText = currencySymbol;
}

document.querySelector('.btn-primary').addEventListener('click', function(){
    var sizeSelect = document.getElementById('size');
    var selectedOption = sizeSelect.options[sizeSelect.selectedIndex];
    var uniqueId = selectedOption.getAttribute('data-id');
    var quantity = document.getElementById('quantity').value;
    addToCart(uniqueId, quantity);
    window.location.href = '/basket';
});

document.getElementById('currency-selector').addEventListener('change', function() {
    var selectedCurrency = this.value;
    var originalPrice = 12.00;

    fetch('/convert_currency?price=' + originalPrice + '&currency=' + selectedCurrency)
        .then(response => response.json())
        .then(data => {
            var currencySymbols = { 'USD': '$', 'EUR': 'x', 'GBP': '£' };
            var symbol = currencySymbols[selectedCurrency] || '£';
            updatePriceDisplay(data.convertedPrice, symbol);
        })
        .catch(error => console.error('Error:', error));
    });

    window.onload = function() {
        document.getElementById('currency-selector').dispatchEvent(new Event('change'));
    };
</script>