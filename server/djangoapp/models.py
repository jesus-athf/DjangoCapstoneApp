from django.db import models
from django.utils.timezone import now

# Create your models here.

class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

# <HINT> Create a Car Model 

class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    id = models.IntegerField(default=1,primary_key=True)
    name = models.CharField(max_length=100)
    
    CAR_TYPES = [
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
    ]
    car_type = models.CharField(max_length=10, choices=CAR_TYPES)
    
    year = models.DateField()
    
    # Add other fields as needed

    def __str__(self):
        return f"{self.year} {self.make.name} {self.name}"


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, dealer_id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.dealer_id = dealer_id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip
    def __str__(self):
        return "Dealer name: " + self.full_name 
    
class DealerReview:

    def __init__(self, 
                 dealership, 
                 name, 
                 purchase, 
                 review):
        # Dealership
        self.dealership = dealership
        # Name
        self.name = name
        # Purchase
        self.purchase = purchase
        # Review
        self.review = review
        # Purchase Date
        self.purchase_date = '99/99/9999'
        # Car Make
        self.car_make = 'N/A'
        # Car Model
        self.car_model = 'N/A'
        # Car Year
        self.car_year = 9999
        # Sentiment
        self.sentiment = ''
        # ID
        self.id = 0      

    def __str__(self):
        return "Review: " + self.review 