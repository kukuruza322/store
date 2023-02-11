

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
            self.cart = cart

    def __getitem__(self, key):
        if key in self.session.keys():
            return self.session[key]
        else:
            return "Not today."

    def __iter__(self):
        # for iterating over items in cart
        pass

    def __len__(self):
        # количество товаров в корзине
        pass

    def add(self, pk, quantity=1):
        # добавление товара
        pass

    def remove(self):
        # удаление товара
        pass

    def get_total_price(self):
        # получение общей стоимости
        pass

    def clear(self):
        # очистка корзины в сессии
        pass
