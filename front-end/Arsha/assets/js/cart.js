let cart = JSON.parse(localStorage.getItem('cart')) || {};
        updateCart(cart);
    
        $(document).on('click', '.cartadd button', function(event) {
            const idstr = event.target.id;
            const name = document.getElementById('name' + idstr).innerHTML;
            const price = document.getElementById('price' + idstr).innerHTML;
    
            if (cart[idstr]) {
                cart[idstr].qty += 1;
            } else {
                cart[idstr] = { qty: 1, name: name, price: price };
            }
    
            updateCart(cart);
            localStorage.setItem('cart', JSON.stringify(cart));
            console.log(cart);
        });
    
        function updatepopover(cart) {
            let popstr = '<h5><b>Cart items</b></h5>';
            let i = 1;
            let total = 0;
            for (const item in cart) {
                const itemTotal = cart[item].price * cart[item].qty;
                popstr += `<b>${i}.</b> ${cart[item].name.slice(0, 19)}... <b>${cart[item].qty}Qty </b>  ${itemTotal} Rs <br>`;
                popstr += `<b> Amount to be pay for single item:${cart[item].price}Rs</b> <br>`;
                total += itemTotal;
                i++;
            }
            popstr += `<h5><b>Total: ${total} Rs</b></h5><br>`; // Add total display.
            popstr += `<button type=button class='btn btn-danger' onclick='clearcart()'>Clear Cart</button>   `
            document.getElementById('popcart').setAttribute('data-bs-content', popstr);
            $('#popcart').popover('show');
        }
    
        function updateCart(cart) {
            let sum = 0;
            for (const item in cart) {
                sum += cart[item].qty;
            }
            document.getElementById('cart').innerHTML = sum;
            updatepopover(cart);
        
        }
    
        function clearCart() {
            localStorage.removeItem('cart');
            cart = {};
            updateCart(cart);
            $('#popcart').popover('hide');
        }
    
        document.getElementById('popcart').addEventListener('click', function() {
            updatepopover(cart);
            $('#popcart').popover('show');
        });
