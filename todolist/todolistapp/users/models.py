from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class MyUserManager(BaseUserManager):
    """ Class for work with users model """
    def _create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError("You didn't enter Email")
        if not username:
            raise ValueError("You didn't enter login")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password):
        return self._create_user(email, username, password)

    def create_superuser(self, email, username, password):
        return self._create_user(email, username, password, is_staff=True, is_superuser=True)


class User(AbstractBaseUser, PermissionsMixin):
    """ User model """
    id = models.AutoField(primary_key=True, unique=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'  # идентификатор для обращения
    REQUIRED_FIELDS = ['email']  # хранит список имён при регистрации администратор или суперюзера.

    objects = MyUserManager()

    def __str__(self):
        return self.email
