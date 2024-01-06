from django.shortcuts import render, get_object_or_404, redirect
from core.models import Category, CartOrder, CartOrderItem, Book, BookImages, BookReview, Address, Wishlist, Author
from userauth.models import Profile
from taggit.models import Tag
from core.forms import BookReviewForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import calendar
from django.db.models.functions import ExtractMonth
from django.db.models import Avg, Count

# PAYPAL IMPORTS
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm



def index(request):
    # books = Book.objects.all().order_by('-id')
    books = Book.objects.filter(book_status='published').order_by('-id')[0:20]
    bk = Book.objects.filter(book_status='published').order_by('-id')[0:3]
    
    context = {
        'books': books,
        'bk': bk,
        }
    return render(request, 'core/index.html', context)


def bookFilter(request):
    books = Book.objects.filter(book_status='published').order_by('-id')
    context = {'books': books}
    
    return render(request, 'core/book-filter.html', context)
    
    
def categoryFilter(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    
    return render(request, 'core/category.html', context)
    
    
def bookCategory(request, cid):
    category = Category.objects.get(cat_id=cid)
    books = Book.objects.filter(book_status='published', category=category)
    
    context = {
        'category': category,
        'books': books
    }
    return render(request, 'core/book-category.html', context)


def authors(request):
    authors = Author.objects.filter(approved=True)
    
    context ={
        'authors': authors
    }
    return render(request, 'core/authors.html', context)


def author(request, aid):
    author = Author.objects.get(approved=True, aut_id=aid)
    books = Book.objects.filter(author=author, book_status='published')
    
    context ={
        'author': author,
        'books': books
    }
    return render(request, 'core/author.html', context)


def bookDetail(request, bid):
    book = get_object_or_404(Book, b_id=bid)
    p_image = book.b_images.all()
    categories = Category.objects.all()
    
    books = Book.objects.filter(category=book.category).exclude(b_id=bid)
    reviews = BookReview.objects.filter(book=book).order_by('-date')
    average_rating = BookReview.objects.filter(book=book).aggregate(rating=Avg('rating'))
    
    rform = BookReviewForm()
    
    make_review = True
    
    if request.user.is_authenticated:
        user_review_count = BookReview.objects.filter(user=request.user, book=book).count()
        
        if user_review_count > 0:
            make_review = False
            
    context = {
        'book': book,
        'img': p_image,
        'categories': categories,
        
        'books': books,
        'reviews': reviews,
        'average_rating': average_rating,
        
        'rform': rform,
        'make_review': make_review,
    }
    return render(request, 'core/book-details.html', context)


def tags(request, tag_slug=None):
    books = Book.objects.filter(book_status='published').order_by('-id')
    
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        books = books.filter(tags__in=[tag])
        
    context = {
        'books': books,
        'tag': tag,
    }
    
    return render(request, 'core/tags.html', context)


def addReview(request, bid):
    book = Book.objects.get(pk=bid)
    user = request.user
    
    review = BookReview.objects.create(
        user=user,
        book=book,
        review = request.POST['review'],
        rating = request.POST['rating'],
    )

    context = {
        'user': user.username,
        'review': request.POST['review'],
        'rating': request.POST['rating'],
    }

    average_rating = BookReview.objects.filter(book=book).aggregate(rating=Avg("rating"))
    
    return JsonResponse(
        {
        'bool': True,
        'context': context,
        'average_rating': average_rating,
        }
    )
    
    
def search(request):
    query = request.GET.get("q")
    # query = request.GET['q']
    
    books = Book.objects.filter(title__icontains=query).order_by('-id')
    
    context = {
        'books': books,
        'query': query,
    }
    return render(request, 'core/search.html', context)



def filterBook(request):
    categories = request.GET.getlist('category[]')
    authors = request.GET.getlist('author[]')
    
    min_price = request.GET['min_price']
    max_price = request.GET['max_price']
    
    
    books = Book.objects.filter(book_status='published').order_by('-id').distinct()
    
    books = books.filter(price__gte=min_price)
    books = books.filter(price__lte=max_price)
    
    if len(categories) > 0:
        books = books.filter(category__id__in=categories).distinct()
        
    if len(authors) > 0:
        books = books.filter(author__id__in=authors).distinct()
    
    context = render_to_string('core/async/book-list.html', {'books': books})
    
    return JsonResponse({
        'context': context
    })
    
    
def addToCart(request):
    cart_book = {}
    
    # THIS IS THE CODE HE WROTE THAT DID NOT
    cart_book[str(request.GET['id'])] = { 
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
        'image': request.GET['image'],
        'pid': request.GET['pid'],
        
    # cart_book[str(request.POST.get("id"))] = {
    #     'title' : request.POST.get("title"),
    #     'qty' : request.POST.get("qty"),
    #     'price' : request.POST.get("price"),
    #     'image' : request.POST.get("image"),
    #     'pid' : request.POST.get("pid"),
    }
    
    if 'cart_data_books' in request.session:
        if str(request.GET['id']) in request.session['cart_data_books']:
            cart_data = request.session['cart_data_books']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_book[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_books'] = cart_data
        else:
            cart_data = request.session['cart_data_books']
            cart_data.update(cart_book)
            request.session['cart_data_books'] = cart_data
        
        # if str(request.POST.get("id")) in request.session['cart_data_books']:
        #     cart_data = request.session['cart_data_books']
        #     cart_data[str(request.POST.get("id"))]['qty'] = int(cart_book[str(request.GET['id'])]['qty'])
        #     cart_data.update(cart_data)
        #     request.session['cart_data_books'] = cart_data
        # else:
        #     cart_data = request.session['cart_data_books']
        #     cart_data.update(cart_book)
        #     request.session['cart_data_books'] = cart_data
            
    else:
        request.session['cart_data_books'] = cart_book
        
    return JsonResponse({'data':request.session['cart_data_books'], 
                         'totalcartbooks': len(request.session['cart_data_books'])})
               
 
def cart(request):
    cart_total_amount = 0
    if 'cart_data_books' in request.session:
        for pid, item in request.session['cart_data_books'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            
        # context = 
            
        return render(request, 'core/cart.html', {'cart_data':request.session['cart_data_books'], 
                        'totalcartbooks': len(request.session['cart_data_books']),
                        'cart_total_amount': cart_total_amount})
    
    else:
        messages.warning(request, 'There is no book in your cart!')
        return redirect("core:index")

    return render(request, 'core/cart.html')


def deleteFromCart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_books' in request.session:
        if product_id in request.session['cart_data_books']:
            cart_data = request.session['cart_data_books']
            del request.session['cart_data_books'][product_id]
            request.session['cart_data_books'] = cart_data
            
    cart_total_amount = 0
    if 'cart_data_books' in request.session:
        for pid, item in request.session['cart_data_books'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])       
            
    context = render_to_string('core/async/cart-list.html', {'cart_data':request.session['cart_data_books'], 
                        'totalcartbooks': len(request.session['cart_data_books']),
                        'cart_total_amount': cart_total_amount})
    
    return JsonResponse({'context': context, 'totalcartbooks': len(request.session['cart_data_books']), })
    
    
def updateCartBook(request):
    product_id = str(request.GET['id'])
    product_qty = str(request.GET['qty'])
    
    if 'cart_data_books' in request.session:
        if product_id in request.session['cart_data_books']:
            cart_data = request.session['cart_data_books']
            cart_data[str(request.GET['id'])]['qty'] = product_qty
            request.session['cart_data_books'] = cart_data
            
    cart_total_amount = 0
    if 'cart_data_books' in request.session:
        for pid, item in request.session['cart_data_books'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])       
            
    context = render_to_string('core/async/cart-list.html', {'cart_data':request.session['cart_data_books'], 
                        'totalcartbooks': len(request.session['cart_data_books']),
                        'cart_total_amount': cart_total_amount})
    
    return JsonResponse({'context': context, 'totalcartbooks': len(request.session['cart_data_books']), })


@login_required
def checkOut(request):
    cart_total_amount = 0
    cart_all_amount = 0
    
    #CHECKING IF SESSION EXISTS
    if 'cart_data_books' in request.session:
        
        #TOTAL AMOUNT FOR PAYPAL PAYMENT
        for pid, item in request.session['cart_data_books'].items():
            cart_all_amount += int(item['qty']) * float(item['price'])  
            
            #CREATING ORDER OBJECTS
            cart_order = CartOrder.objects.create(
                user = request.user,
                price = cart_all_amount,
            )
            
        #TOTAL AMOUNT FOR CART ITEMS
        for pid, item in request.session['cart_data_books'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])    
            
            cart_order_items = CartOrderItem.objects.create(
                cart_order = cart_order,
                invoice_no = 'INVOICE_NO'+ str(cart_order.id),
                item = item['title'],
                image = item['image'],
                quantity = item['qty'],
                price = item['price'],
                total_price = float(item['qty']) * float(item['price']),
            )
    
    host = request.get_host()
    
    paypal_dict = {
        
        #THIS IS AN ALTERNATIVE TO ADDING THE BUSINESS NAME AND HAS TO BE TURNED ON IN SETTINGS
        # 'business': settings.PAYPAL_RECEIVER_EMAIL,
        
        "business": 'babarinde1995@gmail.com',
        'amount': cart_total_amount,
        'item_name': 'order-book-no' + str(cart_order.id),
        'invoice': 'INVOICE_NO'+ str(cart_order.id),
        'currency': 'USD',
        
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('core:paypal-completed')),
        'cancel_return': 'http://{}{}'.format(host,reverse('core:paypal-failed')),
        
        #THIS IS THE ALTERNATIVE TO THE BELOW 3
        # "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        # "return": request.build_absolute_uri(reverse('core:paypal-completed')),
        # "cancel_return": request.build_absolute_uri(reverse('core:paypal-failed')),
        
        
    }
    paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)
    
    # TO GET THE ACTIVE ADDRESS
    try:
        active_address = Address.objects.get(user=request.user, status=True)
    except:
        messages.warning(request, 'Multiple addresses chosen, Please activate just one')
        active_address = None
    
    context = {'cart_data':request.session['cart_data_books'], 
                    'totalcartbooks': len(request.session['cart_data_books']),
                    'cart_total_amount': cart_total_amount,
                    'paypal_payment_button': paypal_payment_button,
                    'active_address': active_address}
        
    return render(request, 'core/checkout.html', context)

    
# @csrf_exempt
@login_required
def paypalCompleted(request):        
    return render(request, 'core/paypal-completed.html', context)


# @csrf_exempt
@login_required
def paypalFailed(request):
    return render(request, 'core/paypal-failed.html')


@login_required
def customerDashboard(request):
    cart_order = CartOrder.objects.filter(user=request.user).order_by('id')
    address = Address.objects.filter(user=request.user)
    profile = Profile.objects.get(user=request.user)
    
    orders = CartOrder.objects.annotate(month=ExtractMonth("order_date")).values('month').annotate(count=Count("id")).values("month", "count")
    month_orders = []
    total_orders =[]
    
    for r in orders:
        month_orders.append(calendar.month_name[r["month"]])
        total_orders.append(r["count"])
        
    if request.method == 'POST':
        
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        
        new_address = Address.objects.create(
            user = request.user,
            address = address,
            mobile = mobile,
        )
        
        messages.success(request, "New address created successfully")
        return redirect(request, 'core:dashboard')
    
    else:
        pass
    
    context = {
        'cart_order': cart_order,
        'address': address,
        'profile': profile,
        'orders': orders,
        'month_orders': month_orders,
        'total_orders': total_orders,
    }
    return render(request, 'core/dashboard.html', context)


def orderDetail(request, id):
    cart_order = CartOrder.objects.get(user=request.user, id=id)
    order_books = CartOrderItem.objects.filter(cart_order=cart_order)
    
    context = {
        'order_books': order_books
    }
    return render(request, 'core/order-detail.html', context)


def defaultAddress(request):
    id = request.GET['id']
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({"boolean": True})


@login_required
def wishlist(request):
    wishlist = Wishlist.objects.all()
    context = {
        'wishlist': wishlist
    }
    return render(request, 'core/wishlist.html', context)


@login_required
def addToWishlist(request):
    book_id = request.GET['id']
    book = Book.objects.get(id=book_id)
    
    context = {}
    
    wishlist_count = Wishlist.objects.filter(book=book, user=request.user).count()
    print(wishlist_count)
    
    if wishlist_count > 0:
        context = {
            'bool': True
        }
    else:
        new_wishlist = Wishlist.objects.create(
            book=book, 
            user=request.user
            )
        context = {
            'bool': True
        }
    
    return JsonResponse(context)


from django.core import serializers


@login_required
def removeFromWishlist(request):
    bk_id = request.GET['id']
    wishlist = Wishlist.objects.filter(user=request.user)
    
    book_d = Wishlist.objects.get(id=bk_id)
    book_delete = book_d.delete()    
    
    context = {
        'bool': True,
        'wishlist': wishlist,
    }
    
    q_json = serializers.serialize('json', wishlist)
    data = render_to_string('core/async/wish-delete.html', context)
    return JsonResponse({'data': data, 'wishlist': q_json})

