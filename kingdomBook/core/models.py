from django.db import models
from django.utils.html import mark_safe 
from shortuuid.django_fields import ShortUUIDField
from userauth.models import User
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField


ORDER_STATUS = (
    ('processing', 'Processing'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered')
)


BOOK_STATUS = (
    ('draft', 'Draft'),
    ('rejected', 'rejected'),
    ('disabled', 'Disabled'),
    ('in_review', 'In Review'),
    ('published', 'Published'),
)


RATING = (
    (1, '⭐☆☆☆☆'),
    (2, '⭐⭐☆☆☆'),
    (3, '⭐⭐⭐☆☆'),
    (4, '⭐⭐⭐⭐☆'),
    (5, '⭐⭐⭐⭐⭐'),
)


# BOOK_TYPE = (
#     ('softcopy', 'Soft Copy'),
#     ('hardcopy', 'Hardcopy'),
#     ('hardcover', 'Hardcover'),
    
# )



def user_directory_path(instance, filename):
    return 'user{0}/{1}'.format(instance.user.id, filename)


class Category(models.Model):
    cat_id = ShortUUIDField(unique=True,  length=10, max_length=30, prefix='CAT-', alphabet='ABCDEFGH12345')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="category")
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def category_image(self):
        return mark_safe('<img src="%s" width="50"/>' % (self.image.url))
    
    def __str__(self):
        return self.title
    
    
class Tags(models.Model):
    pass

    
class Author(models.Model):
    aut_id = ShortUUIDField(unique=True,  length=10, max_length=20, prefix='AU-', alphabet='ABCDEFGHi12345')
    
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='user_directory_path')
    cover_image = models.ImageField(upload_to='user_directory_path', default='a1.jpg')
    
    chat_resp_time = models.CharField(max_length=100, default='state in %')
    ship_on_time = models.CharField(max_length=100, default='state in %')
    authentic_rating = models.CharField(max_length=100, default='100')
    # days_return = models.CharField(max_length=100, default='100')
    # warranty_period = models.CharField(max_length=100, default='100')
    
    address = models.CharField(max_length=100, default='10, Gado Nasko road, Kubwa, Abuja.')
    bio = RichTextUploadingField(max_length=100, default='A seasoned book writer with over 10 years of experience.')
    phone = models.CharField(max_length=14, default='+234 0000 000 000')
    email = models.EmailField(max_length=254, default='sam@book.ng')
    date = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    top_rated = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = 'Authors'
    
    def author_image(self):
        return mark_safe('<img src="%s" width="50"/>' % (self.image.url))
    
    def __str__(self):
        return self.title
    

class Book(models.Model):
    b_id = ShortUUIDField(unique=True,  length=10, max_length=18, prefix='BK-', alphabet='ABCDEFGH12345')
    
    title = models.CharField(max_length=100)
    isbn_no = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='user_directory_path')
    book_description = RichTextUploadingField(null=True, blank=True, default='Please write a description of your book, make it as detailed as possible')
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='book_category')
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name='author_book')
    
    price = models.DecimalField(max_digits=99999999999, decimal_places=2, default="199.99")
    old_price = models.DecimalField(max_digits=99999999999, decimal_places=2, default="299.99")
    pre_order = models.BooleanField(default=False)
    launched = models.BooleanField(default=False)
    no_in_stock = models.CharField(max_length=100, default='100')
    return_policy = models.CharField(max_length=100, default='No Return Policy')
    warranty = models.CharField(max_length=100, default='No Warranty Policy')
    
    # specification = models.TextField(null=True, blank=True)
    # tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)
    
    book_status = models.CharField(choices=BOOK_STATUS, max_length=15, default='in_review')
    # book_type = models.CharField(choices=BOOK_TYPE, max_length=15)
    
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    
    softcopy = models.BooleanField(default=False)
    hardcopy = models.BooleanField(default=True)
    tags = TaggableManager(blank=True)
    
    sku_no = ShortUUIDField(unique=True,  length=5, max_length=10, prefix='sku_', alphabet='1234567890')
    
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(null=True, blank=True)
    launch_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    
    
    class Meta:
        verbose_name_plural = 'Books'
    
    def book_image(self):
        return mark_safe('<img src="%s" width="50"/>' % (self.image.url))
    
    def __str__(self):
        return self.title
    
    def getPercentage(self):
        new_price = (self.price / self.old_price) * 100
        return new_price 
    
    
class BookImages(models.Model):
    images = models.ImageField(upload_to='product-images')
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, related_name='b_images')
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Book Images'
    


################################################Cart, Order, Description and Address###############################################


# THIS IS THE CART
class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9999999999, decimal_places=2, default='199.90')
    payment_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(choices=ORDER_STATUS, max_length=15, default='Processing')
    
    class Meta:
        verbose_name_plural = 'Cart Order'
    
        
# THIS IS FOR EACH ITEMS IN CART     
class CartOrderItem(models.Model):
    cart_order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200, default=127652)
    book_status = models.CharField(max_length=150)
    item = models.CharField(max_length=150)
    image = models.CharField(max_length=150)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=9999999999, decimal_places=2, default='199.90')
    total_price = models.DecimalField(max_digits=9999999999, decimal_places=2, default='199.90')
    
    class Meta:
        verbose_name_plural = 'Cart Order Items'
        
    def order_image(self):
        return mark_safe('<img src="/media/%s" width="50"/>' % (self.image))
    
    def category_image(self):
        return mark_safe('<img src="%s" width="50"/>' % (self.image.url))
    
    
    
    
################################################Product review, Wishlist, Address###############################################




class BookReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, related_name='book_review')
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Book Reviews'
    
    def __str__(self):
        return self.book.title
    
    def get_rating(self):
        return self.rating
    

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Wishlists'
    
    def __str__(self):
        return self.book.title
    

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    mobile = models.CharField(max_length=250, null=True)
    address = models.CharField(max_length=250, null=True)
    status = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = 'Addresses'
    