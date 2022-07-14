from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from blog.models import Post
from main.forms import ContactForm, NewsletterForm

def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():

            contact = form.save(commit=False)
            contact.name = 'Anonymous'
            contact.save()

            messages.add_message(request, messages.SUCCESS, 'Your ticket is submitted successfully.')
        else:
            messages.add_message(request, messages.ERROR, 'Submitting of your ticket failed!')

    form = ContactForm()

    return render(request, 'main/contact.html', { 'form': form })

def newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()

    return HttpResponseRedirect('/')
