from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from users.models import User
from users.serializers import UserSerializer


class UsersViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.super = User.objects.create_superuser(email='superdasilva@mail.com', password='coxinha123', first_name='super', last_name='da silva')
        cls.seller = User.objects.create_user(email='testedasilva@mail.com', password='coxinha123', first_name='teste', last_name='da silva', is_seller=True)
        cls.super_token = Token.objects.create(user=cls.super)
        cls.seller_token = Token.objects.create(user=cls.seller)
        cls.users = User.objects.all()

    def test_can_list_all_users(self):
        response = self.client.get('/api/accounts/')
        self.assertEqual(response.status_code, 200)
      
        self.assertEqual(len(self.users), len(response.data))

        for user in self.users:
            self.assertIn(
                UserSerializer(instance=user).data,
                response.data
            )

    def test_can_list_all_users_by_newest(self):
        response = self.client.get('/api/accounts/newest/2/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['email'], self.seller.email)
        self.assertEqual(response.json()[1]['email'], self.super.email)

    def test_update_user_is_active_status_without_token(self):
        response = self.client.patch('/api/accounts/2/management/', {"is_active": False})
        expected_response = {"detail": "Authentication credentials were not provided."}
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), expected_response)

    def test_update_user_is_active_status_with_wrong_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token 1' + self.super_token.key)
        response = self.client.patch('/api/accounts/2/management/', {"is_active": False})
        expected_response = {"detail": "Invalid token."}
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), expected_response)

    def test_update_user_is_active_status_without_permission(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.seller_token.key)
        response = self.client.patch('/api/accounts/2/management/', {"is_active": False})
        expected_response = {"detail": "You do not have permission to perform this action."}
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), expected_response)

    def test_update_user_is_active_status(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.super_token.key)
        response = self.client.patch('/api/accounts/2/management/', {"is_active": False})
        expected_response = {"is_active": False}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_response)

    def test_update_user_without_token(self):
        response = self.client.patch('/api/accounts/2/', {"first_name": "novoName2", "last_name": "silvinha"})
        expected_response = {"detail": "Authentication credentials were not provided."}
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), expected_response)

    def test_update_user_with_wrong_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token 1' + self.seller_token.key)
        response = self.client.patch('/api/accounts/2/', {"first_name": "novoName2", "last_name": "silvinha"})
        expected_response = {"detail": "Invalid token."}
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), expected_response)

    def test_update_user_without_permission(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.super_token.key)
        response = self.client.patch('/api/accounts/2/', {"first_name": "novoName2", "last_name": "silvinha"})
        expected_response = {"detail": "You do not have permission to perform this action."}
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), expected_response)

    def test_update_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.seller_token.key)
        response = self.client.patch('/api/accounts/2/', {"first_name": "novoName2", "last_name": "silvinha"})
        expected_response = {
            "email": self.seller.email,
            "first_name": "novoName2",
            "last_name": "silvinha",
            "is_seller": True,
            "date_joined": response.json()['date_joined']}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_response)

    def test_login_with_wrong_credentials(self):
        response = self.client.post('/api/login/', {"email": self.seller.email,"password": 'coxinha1234'})
        expected_response = {"detail": "invalid email or password"}
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), expected_response)

    def test_seller_login(self):
        response = self.client.post('/api/login/', {"email": self.seller.email,"password": 'coxinha123'})
        expected_response = {"token": self.seller_token.key}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_response)

    def test_super_login(self):
        response = self.client.post('/api/login/', {"email": self.super.email,"password": 'coxinha123'})
        expected_response = {"token": self.super_token.key}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_response)

    def test_register(self):
        user_info = {"email": "novo@mail.com",
                    "password": "1234",
                    "first_name": "novo",
                    "last_name": "alves",
	                "is_seller": True}
        response = self.client.post('/api/accounts/', user_info)
        expected_response = {"email": user_info['email'],
                            "first_name": user_info['first_name'],
                            "last_name": user_info['last_name'],
                            "is_seller": user_info['is_seller'],
                            "date_joined": response.json()['date_joined']}
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), expected_response)

    def test_register_with_duplicate_email(self):
        user_info = {"email": self.seller.email,
                    "password": "1234",
                    "first_name": "novo",
                    "last_name": "alves",
	                "is_seller": True}
        response = self.client.post('/api/accounts/', user_info)
        expected_response = {"email": ["user with this email already exists."]}
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), expected_response)

    def test_register_without_required_field(self):
        user_info = {"email": "novo2@mail.com",
                    "password": "1234",
                    "first_name": "novo",
	                "is_seller": True}
        response = self.client.post('/api/accounts/', user_info)
        expected_response = {"last_name": ["This field is required."]}
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), expected_response)

        
