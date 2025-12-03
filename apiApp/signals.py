from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ProductRating, Review, Product
from django.db.models import Avg

@receiver(post_save, sender=Review)
def update_product_rating_on_save(render, instance, **kwargs):
    """
    Signal to update product rating when a review is creates or updated"""
    product = instance.product
    reviews = product.reviews.all()
    total_reviews = reviews.count()

    review_average = reviews.aggregate(Avg("rating"))["rating__avg"] or 0.0 

    product_rating, created = ProductRating.objects.get_or_create(product=product)
    product_rating.average_rating = review_average
    product_rating.total_reviews = total_reviews
    