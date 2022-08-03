from django.test import TestCase
from products.models import Product
from users.models import User


class ProductModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        
        cls.seller_email = "teste@teste.com"
        cls.seller_password = "1234"
        cls.seller_first_name = "Teste"
        cls.seller_last_name = "Da Silva"
        cls.seller_is_seller = True

        cls.seller = User.objects.create_user(email=cls.seller_email, password=cls.seller_password, first_name=cls.seller_first_name, last_name=cls.seller_last_name, is_seller=cls.seller_is_seller)

        cls.description = "Smartband XYZ 3.0"
        cls.price = 100.99
        cls.quantity = 15

        cls.product = Product.objects.create(description=cls.description, price=cls.price, quantity=cls.quantity, seller=cls.seller)

    def test_description_max_length(self):
        product = Product.objects.get(pk=1)
        max_length = product._meta.get_field('description').max_length
        self.assertEquals(max_length, 255)

    def test_product_has_information_fields(self):            
        self.assertEqual(self.product.description, self.description)
        self.assertEqual(self.product.price, self.price)
        self.assertEqual(self.product.quantity, self.quantity)
        self.assertEqual(self.product.seller, self.seller)
