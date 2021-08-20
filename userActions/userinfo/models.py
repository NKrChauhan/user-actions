from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
# Create your models here.


class UserManager(BaseUserManager):
    def create(self, email, username, password=None):
        if not email or not username:
            raise ValueError("Uesr model must have username and email")
        user_obj = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user_obj.set_password(password)
        user_obj.save(using=self._db)
        return user_obj

    def create_employeeuser(self, email, username, password=None):
        user_obj = self.create(
            email=email, username=username, password=password
        )
        user_obj.employee = True
        user_obj.client = False
        user_obj.save(using=self._db)
        return user_obj

    def create_manageruser(self, email, username, password=None):
        user_obj = self.create_employeeuser(
            email=email, username=username, password=password
        )
        user_obj.manager = True
        user_obj.client = False
        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(self, email, username, password=None):
        user_obj = self.create_employeeuser(
            email=email, username=username, password=password
        )
        user_obj.manager = True
        user_obj.admin = True
        user_obj.employee = True
        user_obj.client = True
        user_obj.save(using=self._db)
        return user_obj


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address',
                              max_length=255,
                              unique=True,)
    username = models.CharField(max_length=20, unique=True)
    active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    manager = models.BooleanField(default=False)
    employee = models.BooleanField(default=False)
    client = models.BooleanField(default=True)

    objects = UserManager()

    # both username and email is required but email will be used as login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def is_active(self):
        return self.active

    # employee actions
    @property
    def is_employee(self):
        return self.employee
    
    # manager actions
    @property
    def is_manager(self):
        return self.manager

    @property
    def is_admin(self):
        return self.admin
    
    # client actions
    @property
    def is_client(self):
        return self.client

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.password = make_password(self.password, None, 'pbkdf2_sha256')
        super(User, self).save(*args, **kwargs)