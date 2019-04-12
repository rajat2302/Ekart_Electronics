from django.shortcuts import render,get_object_or_404
from .models import Product, Transaction
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
import json
from rest_framework.renderers import JSONRenderer
from django.views.decorators.csrf import csrf_exempt




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
        print(row)
        for ids in row:
            print(ids)
            list_of_ids = ids.split(',')
            print(list_of_ids)
            num.append([int(x) for x in list_of_ids])

    product = listing_id

    sub_dataset = []
    for i in num:
        if product in i:
            sub_dataset.append(i)
    # pip install mlxtend
    # pip install pandas

    import pandas as pd
    from mlxtend.preprocessing import TransactionEncoder

    te = TransactionEncoder()
    te_ary = te.fit(sub_dataset).transform(sub_dataset)
    df = pd.DataFrame(te_ary, columns=te.columns_)

    df1 = df
    df1[product] = False

    list1 = []
    from mlxtend.frequent_patterns import apriori
    import numpy as np

    df2 = apriori(df1, min_support=0.6, use_colnames=True)
    df2 = df2.sort_values(by='support', ascending=False)
    list1 = np.array(df2['itemsets'])
    value, = list1[0]
    product_id = int(value)
    print(product_id)
    suggested_product = Product.objects.get(id=product_id)
    context = {
        'listing': listing,
        'listing_id': listing_id,
        'suggested_product': suggested_product
    }
    print(context)
    return render(request, 'listings/listing.html',context)

def search(request):
    return render(request, 'listings/search.html')

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
            transaction = Transaction(user=User.objects.get(id=1), products=found_product_ids_str, amount=total_amount)
            transaction.save()
            return Response(data={'message': 'Purchase successful'}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'status': 'Invalid products, unable to purchase'}, status=status.HTTP_400_BAD_REQUEST)



def example(request):
    return render(request, 'try/try.html')




