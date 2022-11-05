import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.deletion import CASCADE


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        username,
        email,
        password,
        first_name=None,
        last_name=None,
        address=None,
        phone_number=None,
    ):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(username, email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


# Create your models here.
class Profile(AbstractUser):
    object = UserManager()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)
    address = models.CharField(max_length=300)
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=20)
    password = models.CharField(max_length=200)
    date_joined = models.DateTimeField(auto_now_add=True, null=False)
    last_login = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    is_admin = models.BooleanField(default=False)  # a superuser

    USERNAME_FIELD = "username"

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    def __str__(self):
        return self.username


class Pitch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=300, unique=True)
    size = models.CharField(max_length=5, unique=False)
    price = models.CharField(max_length=10, unique=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class Booking(models.Model):

    TIMESLOT_LIST = (
        (0, '08:00 - 09:00'),
        (1, '09:00 - 10:00'),
        (2, '10:00 - 11:00'),
        (3, '11:00 - 12:00'),
        (4, '12:00 - 13:00'),
        (5, '13:00 - 14:00'),
        (6, '14:00 - 15:00'),
        (7, '15:00 - 16:00'),
        (8, '16:00 - 17:00'),
        (9, '17:00 - 18:00'),
        (10, '18:00 - 19:00'),
        (11, '19:00 - 20:00'),
        (12, '20:00 - 21:00'),
        (13, '21:00 - 22:00'),
        (14, '22:00 - 23:00'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pitch_id = models.ForeignKey(Pitch, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Profile, on_delete=CASCADE)
    pitch_name = models.CharField(max_length=300, null=False)
    pitch_price = models.CharField(max_length=10, unique=False, null=False)
    pitch_size = models.CharField(max_length=20, unique=False, null=False)
    timeslot = models.IntegerField(choices=TIMESLOT_LIST, null=False)
    date = models.DateField(help_text="YYYY-MM-DD", null=False)
    time = models.TimeField(null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

