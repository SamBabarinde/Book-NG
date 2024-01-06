from django.shortcuts import render
from .models import ContactUs
from django.http import JsonResponse

def contactpage(request):
    return render(request, 'pages/contact.html')

def ajaxContact(request):
    full_name = request.GET['full_name']
    email = request.GET['email']
    phone = request.GET['phone']
    subject = request.GET['subject']
    message = request.GET['message']
    
    contact = ContactUs.objects.create(
        full_name=full_name,
        email=email,
        phone=phone,
        subject=subject,
        message=message
    )
    
    context = {
        'bool': True,
    }
    
    return JsonResponse({'context':context})