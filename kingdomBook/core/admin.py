from django.contrib import admin
from core.models import Category, CartOrder, CartOrderItem, Book, BookImages, BookReview, Address, Wishlist, Author


class BookImagesAdmin(admin.TabularInline):
    model = BookImages
    
    
class BookAdmin(admin.ModelAdmin):
    inlines = [BookImagesAdmin]
    list_display = ['user', 'title', 'book_image', 'price', 'featured', 'category', 'author', 'book_status', 'hardcopy', 'hardcopy']
    
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_image']
    
    
class AuthorAdmin(admin.ModelAdmin):
    list_editable = ['approved']
    list_display = ['title', 'author_image', 'approved']
    
    
class CartOrderAdmin(admin.ModelAdmin):
    list_editable = ['payment_status', 'order_status']
    list_display = ['user', 'price', 'payment_status', 'order_date', 'order_status']


class CartOrderItemAdmin(admin.ModelAdmin):
    list_display = ['cart_order', 'price', 'invoice_no', 'item', 'image', 'quantity', 'total_price']


class BookReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'review', 'rating', 'date', 'book']
    
    
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'book']
    
    
class AddressAdmin(admin.ModelAdmin):
    list_editable = ['address', 'status']
    list_display = ['user', 'address', 'status']
    
    

admin.site.register(Book, BookAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(CartOrder,  CartOrderAdmin)
admin.site.register(CartOrderItem, CartOrderItemAdmin)
admin.site.register(BookReview, BookReviewAdmin)
admin.site.register(Wishlist,  WishlistAdmin)
admin.site.register(Address, AddressAdmin)


