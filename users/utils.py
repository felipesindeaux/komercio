from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email is required')

        email = self.normalize_email(email)

        user = self.model(email=email, is_superuser=True, is_seller=False, **extra_fields)

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_user(self, email, password, is_seller, **extra_fields):
        if not email:
            raise ValueError('Email is required')

        email = self.normalize_email(email)

        user = self.model(email=email, is_superuser=False, is_seller=is_seller, **extra_fields)

        user.set_password(password)

        user.save(using=self._db)

        return user

