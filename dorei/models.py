from django.db import models

# Create your models here.

from django.urls import reverse # Used to generate URLs by reversing the URL patterns

class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)

    def __str__(self):
        """String for representing the Model object."""
        return self.title

class User(models.Model):
    user_id = models.IntegerField(db_column='user_id', primary_key=True)  
    first_name = models.TextField(db_column='first_name', max_length=10)
    middle_name = models.TextField(db_column='middle_name', max_length=10, blank=True, null=True)
    last_name = models.TextField(db_column='last_name', max_length=10, blank=True, null=True)
    email_address = models.EmailField(db_column='email_address', max_length=40)  
    house_number = models.CharField(db_column='house_number', max_length=10, blank=True, null=True) 
    street_number = models.CharField(db_column='street_number', max_length=10, blank=True, null=True)  
    street_name = models.TextField(db_column='street_name', max_length=50)   
    city = models.TextField(db_column='city', max_length=50)  
    state = models.TextField(db_column='state', max_length=50)  
    postal_code = models.DecimalField(db_column='postal_code', max_digits=6, decimal_places=0) 
    password = models.CharField(db_column='password', max_length=256) 

    def __str__(self):
        """String for representing the Model object."""
        return self.email_address

