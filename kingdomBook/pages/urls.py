from django.urls import path
from . import views

app_name = "pages"


urlpatterns = [
    path("contact/", views.contactpage, name="contact"),
    path("ajax-contact-form/", views.ajaxContact, name="ajax-contact"),
]
