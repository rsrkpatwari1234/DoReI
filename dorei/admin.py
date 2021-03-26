from django.contrib import admin

# Register your models here.

from .models import Location, Book, User, Money, BookDonate

admin.site.register(Location)
admin.site.register(Book)
admin.site.register(User)
admin.site.register(Money)
admin.site.register(BookDonate)

