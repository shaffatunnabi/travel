from django.contrib import admin
from .models import Person, Book

# Register the Person model to the admin site
admin.site.register(Person)
admin.site.register(Book)
