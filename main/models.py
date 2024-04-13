from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    mobile_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255)

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username


class Category(models.Model):
    images = models.ImageField(upload_to='category_images')
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    image = models.ImageField(upload_to='product_image')
    title = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    info = models.TextField()
    discount = models.IntegerField(null=True, blank=True)
    discount_price = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)


class Banner(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    banner_image = models.ImageField(upload_to='banner_images/')
    banner_title = models.CharField(max_length=100)
    banner_description = models.CharField(max_length=100)

    def __str__(self):
        return self.banner_title


class About(models.Model):
    image = models.ImageField(upload_to='about_images/')
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class OutResults(models.Model):
    happy_customers = models.IntegerField(default=0)
    branches = models.IntegerField(default=0)
    partner = models.IntegerField(default=0)
    awards = models.IntegerField(default=0)


class Info(models.Model):
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.CharField(max_length=255)
    website = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='logo_img/')

    def __str__(self):
        return self.website


class ContactUs(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Blog(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    text = models.TextField()
    text2 = models.TextField()
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    tag = models.ManyToManyField(to=Tag, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.CharField(max_length=255)
    blog = models.ForeignKey(to=Blog, on_delete=models.CASCADE)
    text = models.TextField()
    creates_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


class Order(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    products = models.TextField()
    total = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return self.firstname