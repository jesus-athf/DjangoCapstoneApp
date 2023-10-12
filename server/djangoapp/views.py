from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import CarDealer, CarModel, CarModel
# from .restapis import related methods
from .restapis import get_dealers_from_cf, get_request, get_dealer_by_id, get_dealers_by_state, get_dealer_reviews_from_cf, analyze_review_sentiments, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout (request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://michischaetz-3000.theiadocker-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        dealerships = get_dealers_from_cf(url)
        context["dealership_list"] = dealerships
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        context = {}
        dealer_url = 'https://michischaetz-3000.theiadocker-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get'
        dealer = get_dealer_by_id(dealer_url, dealer_id=dealer_id)
        context["dealer"] = dealer
    
        review_url = "https://michischaetz-5000.theiadocker-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews"
        reviews = get_dealer_reviews_from_cf(review_url, dealer_id=dealer_id)

        # Analyze sentiment for each review
        for review in reviews:
            sentiment = analyze_review_sentiments(review)
            review.sentiment = sentiment  # Update the sentiment attribute of the review
        
        print(reviews)
        context["reviews"] = reviews
        context["dealer_id"] = dealer_id
        
        return render(request, 'djangoapp/dealer_details.html', context)
#
# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {}
    dealer_url = 'https://michischaetz-3000.theiadocker-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get'
    dealer = get_dealer_by_id(dealer_url, dealer_id=dealer_id)
    context["dealer"] = dealer
    if request.method == 'GET':
        # Get cars for the dealer
        cars = CarModel.objects.all()
        print(cars)
        context["cars"] = cars
        
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        if request.user.is_authenticated:
            username = request.user.username
            print(request.POST)
            payload = dict()
            payload["time"] = datetime.utcnow().isoformat()
            payload["name"] = username
            payload["dealership"] = request.POST["dealership"]
            payload["review"] = request.POST["review"]
            payload["purchase"] = False
            if "purchasecheck" in request.POST:
                if request.POST["purchasecheck"] == 'on':
                    payload["purchase"] = True
            payload["purchase_date"] = request.POST["purchase_date"]
            payload["car_make"] = request.POST["car_make"]
            payload["car_model"] = request.POST["car_model"]
            payload["car_year"] = request.POST["car_year"]

            new_payload = {}
            new_payload["review"] = payload
            review_post_url = 'https://michischaetz-5000.theiadocker-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/post_review'
            post_request(review_post_url, new_payload,dealer_id=dealer_id)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
