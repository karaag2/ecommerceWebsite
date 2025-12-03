import os
import django
import random
from django.utils.text import slugify

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EcommerceWebsite.settings')
django.setup()

from apiApp.models import ProductCategory, Product, customuser

def create_superuser():
    if not customuser.objects.filter(username='admin').exists():
        customuser.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        print('Superuser created successfully!')

def seed_categories():
    categories = [
        {
            'name': 'Electronics',
            'image': 'category_img/electronics.jpg'
        },
        {
            'name': 'Clothing',
            'image': 'category_img/clothing.jpg'
        },
        {
            'name': 'Books',
            'image': 'category_img/books.jpg'
        },
        {
            'name': 'Home & Kitchen',
            'image': 'category_img/home.jpg'
        }
    ]

    for cat in categories:
        category = ProductCategory.objects.create(
            name=cat['name'],
            slug=slugify(cat['name']),
            image=cat['image']
        )
        print(f'Created category: {category.name}')

def seed_products():
    categories = ProductCategory.objects.all()
    
    products = [
        {
            'name': 'Smartphone X',
            'description': 'Latest smartphone with amazing features',
            'price': 999.99,
            'category': 'Electronics',
            'image': 'products_img/smartphone.jpg',
            'featured': True
        },
        {
            'name': 'Cotton T-Shirt',
            'description': 'Comfortable cotton t-shirt',
            'price': 19.99,
            'category': 'Clothing',
            'image': 'products_img/tshirt.jpg',
            'featured': True
        },
        {
            'name': 'Python Programming Guide',
            'description': 'Comprehensive guide to Python programming',
            'price': 49.99,
            'category': 'Books',
            'image': 'products_img/python_book.jpg',
            'featured': False
        },
        {
            'name': 'Coffee Maker',
            'description': 'Automatic coffee maker with timer',
            'price': 79.99,
            'category': 'Home & Kitchen',
            'image': 'products_img/coffee_maker.jpg',
            'featured': True
        }
    ]

    for prod in products:
        category = ProductCategory.objects.get(name=prod['category'])
        Product.objects.create(
            name=prod['name'],
            description=prod['description'],
            price=prod['price'],
            category=category,
            slug=slugify(prod['name']),
            image=prod['image'],
            featured=prod['featured']
        )
        print(f'Created product: {prod["name"]}')

def main():
    print('Starting database seeding...')
    
    # Create superuser
    create_superuser()
    
    # Create categories
    if ProductCategory.objects.count() == 0:
        seed_categories()
    else:
        print('Categories already exist, skipping...')
    
    # Create products
    if Product.objects.count() == 0:
        seed_products()
    else:
        print('Products already exist, skipping...')
    
    print('Database seeding completed!')

if __name__ == '__main__':
    main()