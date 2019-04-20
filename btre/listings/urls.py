from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='listings'),
    path('<int:listing_id>', views.listing, name='listing'),
    path('search', views.search, name='search'),
    path('purchase', views.PurchaseView.as_view(), name='Purchase'),
    path('suggested_products', views.PurchaseView.as_view(), name='Purchase'),
    path('review_system', views.review_system, name='review_system')


]