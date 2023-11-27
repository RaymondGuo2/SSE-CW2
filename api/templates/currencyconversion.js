document.getElementById('currency-selector').addEventListener('change', function() {
    var selectedCurrency = this.value;
    var originalPrice = 10.00;

    fetch('/convert_currency?price=' + originalPrice + '&currency=' + selectedCurrency)
        .then(response => response.json())
        .then(data => {
            document.getElementById('price').innerText = data.convertedPrice.toFixed(2);
        });
});
