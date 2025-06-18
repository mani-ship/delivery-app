

from collections import Counter
from .models import OrderItem, Product

def get_frequently_bought_together(product_id, limit=3):
    # Get all order IDs that contain the given product
    order_ids = OrderItem.objects.filter(product_id=product_id).values_list('order_id', flat=True)

    # Get all other products in those orders
    other_items = OrderItem.objects.filter(order_id__in=order_ids).exclude(product_id=product_id)

    # Count product frequencies
    product_counts = Counter(other_items.values_list('product_id', flat=True))

    # Get top product IDs
    top_ids = [pid for pid, _ in product_counts.most_common(limit)]

    # Return queryset
    return Product.objects.filter(id__in=top_ids)
