from django.urls import path
from core import views


app_name = "core"

urlpatterns = [
    
    path('', views.index, name='index'),
    
    path('book-filter/', views.bookFilter, name='book-filter'),
    path('category/', views.categoryFilter, name='categoryfilter'),
    path('category/<cid>/', views.bookCategory, name='book-category'),
    
    path('authors/', views.authors, name='authors'),
    path('author/<aid>/', views.author, name='author'),
    
    path('book/<bid>/', views.bookDetail, name='book-detail'),
    
    path('tags/<slug:tag_slug>/', views.tags, name='tags'),
    path('review/<int:bid>/', views.addReview, name='add-review'),
    
    path('search/', views.search, name='search'),
    path('filter-books/', views.filterBook, name='filter-book'),
    
    path('add-to-cart/', views.addToCart, name='add-to-cart'),
    path('cart/', views.cart, name='cart'),
    path('delete-from-cart/', views.deleteFromCart, name='delete-from-cart'),
    path('update-cart/', views.updateCartBook, name='update-cart'),
    
    path('checkout/', views.checkOut, name='checkout'),
    
    path('paypal-completed/', views.paypalCompleted, name='paypal-completed'),    
    path('paypal-failed/', views.paypalFailed, name='paypal-failed'), 
    
    path('dashboard/', views.customerDashboard, name='dashboard'),
    path('dashboard/order/<int:id>', views.orderDetail, name='order-detail'),
    
    path('make-default-address', views.defaultAddress, name='default-address'),
    
    path('add-to-wishlist/',views.addToWishlist, name='add-to-wishlist'),
    path('wishlist/',views.wishlist, name='wishlist'),
    path('remove-from-wishlist/',views.removeFromWishlist, name='remove-from-wishlist'),
    
    
]
