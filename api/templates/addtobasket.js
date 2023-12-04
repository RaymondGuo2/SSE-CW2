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