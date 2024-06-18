from django.contrib import admin

from finance.models import Category, Transaction, Budget

# Register your models here.
admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(Budget)

