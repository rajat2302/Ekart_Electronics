from django.contrib import admin
from .models import Product, Transaction,Review
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_available', 'price', 'list_date', 'brand')
    list_display_links = ('id', 'name')
    list_filter = ('brand',)
    list_editable = ('is_available',)
    search_fields = ('name', 'description', 'type', 'stype', 'ram', 'storage', 'price')
    list_per_page = 25

class TransactionAdmin(admin.ModelAdmin):
    pass

class ReviewAdmin(admin.ModelAdmin):
    pass


admin.site.register(Product, ProductAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Review, ReviewAdmin)