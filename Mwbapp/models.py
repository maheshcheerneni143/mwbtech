from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        confirm_password = extra_fields.pop('confirm_password', None)  # Remove confirm_password from extra_fields
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user._confirm_password = confirm_password
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)
    

    # def create_superuser(self, email, password=None, **extra_fields):
    #     extra_fields.setdefault('is_superuser', True)
    #     extra_fields.setdefault('is_staff', True)
    #     return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    mobile_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Mobile number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    mobile_number = models.CharField(validators=[mobile_regex], max_length=17, unique=True)
    confirm_password = models.CharField(max_length=20,null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)



    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    class Meta:
        db_table = 'CompanyUser'

    def __str__(self):
        return self.email
    # Override the Database
    @property
    def confirm_password(self):
        return None
    
    
    @property
    def last_login(self):
        return None

    
class Add_Product(models.Model):
    name = models.CharField(max_length=50)
    Category = models.CharField(max_length=12)
    brand = models.CharField(max_length=50)
    price = models.FloatField()
    quantity  = models.IntegerField()
    Description  = models.TextField(max_length=50)
    class Meta:
        db_table = 'AddProduct'
   
