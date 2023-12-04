document.addEventListener('DOMContentLoaded', (event) => {
    const buyNowButton = document.querySelector('.btn-success');
    if (buyNowButton) {
        buyNowButton.addEventListener('click', buyNow);
    } else {
        console.error('Buy Now button not found');
    }
});

function buyNow(event) {
    event.preventDefault(); // Prevent default form submission if it's inside a form

    const size = document.getElementById('size').value;
    const quantity = document.getElementById('quantity').value;
    const price = document.getElementById('price').textContent;

    localStorage.setItem('checkoutDetails', JSON.stringify({ size, quantity, price }));

    window.location.href = '{{ url_for("checkout") }}'; // Replace with the correct path if necessary
}
