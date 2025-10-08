from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class custom_user(AbstractUser):
    email = models.EmailField(unique=True)
    profile_picture_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.email
    
class product_category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='category_img', blank=True,null=True)

    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        if not self.slug:
            self.slug = slugify(self.name)
            # Handle duplicate slugs
            counter = 1
            while product_category.objects.filter(slug=self.slug).exists():
                self.slug = f"{slugify(self.name)}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(unique=True,blank=True)
    category = models.ForeignKey(product_category, on_delete=models.SET_NULL,related_name='products', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    featured = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='products_img', blank=True,null=True)
    
    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        if not self.slug:
            self.slug = slugify(self.name)
            # Handle duplicate slugs
            counter = 1
            while product.objects.filter(slug=self.slug).exists():
                self.slug = f"{slugify(self.name)}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name