from products.models import Product
from products.serializers import CreateProductSerializer, ListProductSerializer
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from users.models import User


class ProductsViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.seller = User.objects.create_user(email='testedasilva@mail.com', password='coxinha123', first_name='teste', last_name='da silva', is_seller=True)
        cls.super = User.objects.create_superuser(email='superdasilva@mail.com', password='coxinha123', first_name='super', last_name='da silva')
        cls.seller_token = Token.objects.create(user=cls.seller)
        cls.super_token = Token.objects.create(user=cls.super)
        cls.products = [Product.objects.create(description=f'Product {product_id}', price=100.00, quantity=15, seller=cls.seller) for product_id in range(1, 6)]

    def test_can_list_all_products(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, 200)
      
        self.assertEqual(len(self.products), len(response.data))

        for product in self.products:
            self.assertIn(
                ListProductSerializer(instance=product).data,
                response.data
            )

    def test_can_retrieve_a_specific_product(self):
        product = self.products[0]
        response = self.client.get(f'/api/products/{product.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['description'], product.description)

        self.assertEqual(
            ListProductSerializer(instance=product).data,
            response.data
        )

    # def test_update_user_is_active_status_without_token(self):
    #     response = self.client.patch('/api/accounts/2/management/', {"is_active": False})
    #     expected_response = {"detail": "Authentication credentials were not provided."}
    #     self.assertEqual(response.status_code, 401)
    #     self.assertEqual(response.json(), expected_response)

    # def test_update_user_is_active_status_with_wrong_token(self):
    #     self.client.credentials(HTTP_AUTHORIZATION='Token 1' + self.super_token.key)
    #     response = self.client.patch('/api/accounts/2/management/', {"is_active": False})
    #     expected_response = {"detail": "Invalid token."}
    #     self.assertEqual(response.status_code, 401)
    #     self.assertEqual(response.json(), expected_response)

    # def test_update_user_is_active_status_without_permission(self):
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.seller_token.key)
    #     response = self.client.patch('/api/accounts/2/management/', {"is_active": False})
    #     expected_response = {"detail": "You do not have permission to perform this action."}
    #     self.assertEqual(response.status_code, 403)
    #     self.assertEqual(response.json(), expected_response)

    # def test_update_user_is_active_status(self):
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.super_token.key)
    #     response = self.client.patch('/api/accounts/2/management/', {"is_active": False})
    #     expected_response = {"is_active": False}
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json(), expected_response)

    # def test_update_user_without_token(self):
    #     response = self.client.patch('/api/accounts/2/', {"first_name": "novoName2", "last_name": "silvinha"})
    #     expected_response = {"detail": "Authentication credentials were not provided."}
    #     self.assertEqual(response.status_code, 401)
    #     self.assertEqual(response.json(), expected_response)

    # def test_update_user_with_wrong_token(self):
    #     self.client.credentials(HTTP_AUTHORIZATION='Token 1' + self.seller_token.key)
    #     response = self.client.patch('/api/accounts/2/', {"first_name": "novoName2", "last_name": "silvinha"})
    #     expected_response = {"detail": "Invalid token."}
    #     self.assertEqual(response.status_code, 401)
    #     self.assertEqual(response.json(), expected_response)

    # def test_update_user_without_permission(self):
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.super_token.key)
    #     response = self.client.patch('/api/accounts/2/', {"first_name": "novoName2", "last_name": "silvinha"})
    #     expected_response = {"detail": "You do not have permission to perform this action."}
    #     self.assertEqual(response.status_code, 403)
    #     self.assertEqual(response.json(), expected_response)

    # def test_update_user(self):
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.seller_token.key)
    #     response = self.client.patch('/api/accounts/2/', {"first_name": "novoName2", "last_name": "silvinha"})
    #     expected_response = {
    #         "email": self.seller.email,
    #         "first_name": "novoName2",
    #         "last_name": "silvinha",
    #         "is_seller": True,
    #         "date_joined": response.json()['date_joined']}
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json(), expected_response)

    # def test_login_with_wrong_credentials(self):
    #     response = self.client.post('/api/login/', {"email": self.seller.email,"password": 'coxinha1234'})
    #     expected_response = {"detail": "invalid email or password"}
    #     self.assertEqual(response.status_code, 401)
    #     self.assertEqual(response.json(), expected_response)

    # def test_login(self):
    #     response = self.client.post('/api/login/', {"email": self.seller.email,"password": 'coxinha123'})
    #     expected_response = {"token": self.seller_token.key}
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json(), expected_response)

    def test_create_product_without_permission(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.super_token.key)
        product_info = {"description": "Smartband XYZ 3.0",
                        "price": 100.99,
                        "quantity": 15}
        response = self.client.post('/api/products/', product_info)
        expected_response = {"detail": "You do not have permission to perform this action."}
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), expected_response)

    def test_create_product_with_negative_quantity(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.seller_token.key)
        product_info = {"description": "Smartband XYZ 3.0",
                        "price": 100.99,
                        "quantity": -15}
        response = self.client.post('/api/products/', product_info)
        expected_response = {"quantity": ["Ensure this value is greater than or equal to 0."]}
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), expected_response)

    def test_create_product_without_required_fields(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.seller_token.key)
        product_info = {"description": "Smartband XYZ 3.0",
                        "price": 100.99}
        response = self.client.post('/api/products/', product_info)
        expected_response = {"quantity": ["This field is required."]}
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), expected_response)

    def test_create_product(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.seller_token.key)
        product_info = {"description": "Smartband XYZ 3.0",
                        "price": 100.99,
                        "quantity": 15}
        response = self.client.post('/api/products/', product_info)
        seller_response = response.json()['seller']
        expected_response = {"id": self.products[-1].id + 1,
                            "description": product_info['description'],
                            "price": product_info['price'],
                            "quantity": product_info['quantity'],
                            "is_active": False,
                            "seller": {
                                "id": self.seller.id,
                                "email": self.seller.email,
                                "first_name": self.seller.first_name,
                                "last_name": self.seller.last_name,
                                "is_seller": self.seller.is_seller,
                                "date_joined": seller_response['date_joined']
                            }}
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), expected_response)

    def test_update_product_without_permission(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.super_token.key)
        product_info = {"price": 5.99}
        response = self.client.patch('/api/products/1/', product_info)
        expected_response = {"detail": "You do not have permission to perform this action."}
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), expected_response)

    def test_update_product(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.seller_token.key)
        product = self.products[0]
        product_info = {"price": 5.99}
        response = self.client.patch('/api/products/1/', product_info)
        seller_response = response.json()['seller']
        expected_response = {"id": product.id,
                            "description": product.description,
                            "price": product_info['price'],
                            "quantity": product.quantity,
                            "is_active": True,
                            "seller": {
                                "id": self.seller.id,
                                "email": self.seller.email,
                                "first_name": self.seller.first_name,
                                "last_name": self.seller.last_name,
                                "is_seller": self.seller.is_seller,
                                "date_joined": seller_response['date_joined']
                            }}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_response)

    # def test_register_with_duplicate_email(self):
    #     user_info = {"email": self.seller.email,
    #                 "password": "1234",
    #                 "first_name": "novo",
    #                 "last_name": "alves",
	#                 "is_seller": True}
    #     response = self.client.post('/api/accounts/', user_info)
    #     expected_response = {"email": ["user with this email already exists."]}
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(response.json(), expected_response)

    # def test_register_without_required_field(self):
    #     user_info = {"email": "novo2@mail.com",
    #                 "password": "1234",
    #                 "first_name": "novo",
	#                 "is_seller": True}
    #     response = self.client.post('/api/accounts/', user_info)
    #     expected_response = {"last_name": ["This field is required."]}
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(response.json(), expected_response)

        
