from django.shortcuts import render,redirect,get_object_or_404
from .models import Product, Transaction,Review
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
import json
from rest_framework.renderers import JSONRenderer
from django.views.decorators.csrf import csrf_exempt
from mlxtend.frequent_patterns import apriori
import numpy as np
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from listings.choices import price_choices,type_choices,brand_choices
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.pipeline import Pipeline



def index(request):
    listings = Product.objects.order_by('-list_date').filter(is_available=True)

    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    context = {
        'listings': paged_listings
    }
    return render(request, 'listings/listings.html',context)

def listing(request, listing_id):
    listing = get_object_or_404(Product, pk=listing_id)
    transaction = Transaction.objects.values_list('products')
    transaction_ids = [list(x) for x in transaction]
    num = []
    for row in transaction_ids:
        for ids in row:
            list_of_ids = ids.split(',')
            num.append([int(x) for x in list_of_ids])
    product = listing_id

    sub_dataset = []
    for i in num:
        if product in i:
            sub_dataset.append(i)
    te = TransactionEncoder()
    te_ary = te.fit(sub_dataset).transform(sub_dataset)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    df1 = df
    df1[product] = False
    df2 = apriori(df1, min_support=0.6, use_colnames=True)
    df2 = df2.sort_values(by='support', ascending=False)
    list1 = np.array(df2['itemsets'])
    suggested_product = None
    if list1 and len(list1) > 0:
        value, = list1[0]
        product_id = int(value)
        suggested_product = Product.objects.get(id=product_id)
    context = {
        'listing': listing,
        'listing_id':listing_id,
        'user': request.user,
        'suggested_product': suggested_product
    }
    print(context)
    return render(request, 'listings/listing.html',context)

def search(request):
    queryset_list = Product.objects.order_by('-list_date')
    # Keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)
    # City
    if 'ram' in request.GET:
        ram = request.GET['ram']
        if ram:
            queryset_list = queryset_list.filter(ram__iexact=ram)

    # State
    if 'type' in request.GET:
        type = request.GET['type']
        if type:
            queryset_list = queryset_list.filter(type__iexact=type)

    # Bedrooms
    if 'brand' in request.GET:
        brand = request.GET['brand']
        if brand:
            queryset_list = queryset_list.filter(brand__iexact=brand)

    # Price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price)

    context = {
        'listings': queryset_list,
        'price_choices': price_choices,
        'brand_choices': brand_choices,
        'type_choices': type_choices,
        'values': request.GET
    }
    return render(request, 'listings/search.html',context)

def validate_products(products):
    found_product_ids = []
    missing_product_ids = []
    total_amount = 0
    if products:
        product_ids = products.split(',')
        for product_id in product_ids:
            print(product_id)
            product = Product.objects.filter(id=product_id)[0:1]
            if len(product) > 0:
                found_product_ids.append(product[0].id)
                total_amount = round(total_amount + product[0].price, 2)
            else:
                missing_product_ids.append(product_id)

    return found_product_ids, missing_product_ids, total_amount

class PurchaseView(APIView):

    renderer_classes = (JSONRenderer,)

    def get(self, request):
        purchase = Transaction.objects.all()
        data = []
        for p in purchase:
            data.append({'id': p.id, 'amount': str(p.amount), 'products': p.products})
        return Response({"purchase": data})

    def post(self, request):
        products = request.data.get('products')
        found_product_ids, missing_product_ids, total_amount = validate_products(products)
        if len(found_product_ids) > 0:
            found_product_ids_str = ','.join([str(x) for x in found_product_ids])
            transaction = Transaction(user=User.objects.get(id=request.user.id), products=found_product_ids_str, amount=total_amount)
            transaction.save()
            return Response(data={'message': 'Purchase successful'}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'status': 'Invalid products, unable to purchase'}, status=status.HTTP_400_BAD_REQUEST)


class SuggestedProductView(APIView):

    renderer_classes = (JSONRenderer,)

    def get(self, request):
        product_id = request.data.get("product_id")
        # check product exists or not
        # if not then give error
        # run algo and return list of suggested products as json
        return Response(data={'suggested_product': {'id': id, 'name': name, 'price': price}}, status=status.HTTP_201_CREATED)

def review_system(request):
    review_statement = request.POST['review']
    csvfile = r'C:\Users\rajat\PycharmProjects\Ekart_Electronics\btre\listings\sentiments_with_review.csv'
    saved_review = pd.read_csv(csvfile, encoding='latin-1')
    x = saved_review['review'].values
    y = saved_review['sentiment'].values
    naive_model = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', MultinomialNB())])
    naive_model.fit(x, y)
    sentiment = naive_model.predict([review_statement])
    print(sentiment[0])
    reviews = Review(user=User.objects.get(id=request.user.id),review_statement=review_statement,review_sentiment=sentiment[0])
    reviews.save()
    return redirect('listings')