from core.models import Category, CartOrder, CartOrderItem, Book, BookImages, BookReview, Address, Wishlist, Author
from django.db.models import Count, Min, Max
from django.contrib import messages


def baseView(request):
    categories = Category.objects.all()
    author = Author.objects.filter(approved=True)
    
    min_max_price= Book.objects.aggregate(Min('price'), Max('price'))
    
    try:
        address = Address.objects.get(user=request.user)
    except:
        address = None
    
    try:
        wishlist = Wishlist.objects.filter(user=request.user)
    except:
        messages.warning(request, "Please login to access your wishlist")
        wishlist = 0
        
    return {
        'categories': categories,
        'address': address,
        'author': author,
        'min_max_price': min_max_price,
        'wishlist': wishlist,
    }
    