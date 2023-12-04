document.querySelector('.btn-success').addEventListener('click', buyNow);

function buyNow() {
    const size = document.getElementById('size').value;
    const quantity = document.getElementById('quantity').value;
    const price = document.getElementById('price').textContent;

    localStorage.setItem('checkoutDetails', JSON.stringify({ size, quantity, price }));

    window.location.href = '{{ url_for("checkout") }}';
}
