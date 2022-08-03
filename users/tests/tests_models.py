from django.test import TestCase
from users.models import User


class UserModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.email = "teste@teste.com"
        cls.password = "1234"
        cls.first_name = "Teste"
        cls.last_name = "Da Silva"
        cls.is_seller = True

        cls.user = User.objects.create_user(email=cls.email, password=cls.password, first_name=cls.first_name, last_name=cls.last_name, is_seller=cls.is_seller)

    def test_first_name_max_length(self):
        user = User.objects.get(pk=1)
        max_length = user._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 50)

    def test_last_name_max_length(self):
        user = User.objects.get(pk=1)
        max_length = user._meta.get_field('last_name').max_length
        self.assertEquals(max_length, 50)

    def test_user_has_information_fields(self):            
        self.assertEqual(self.user.email, self.email)
        self.assertEqual(self.user.first_name, self.first_name)
        self.assertEqual(self.user.last_name, self.last_name)
        self.assertEqual(self.user.is_seller, self.is_seller)
