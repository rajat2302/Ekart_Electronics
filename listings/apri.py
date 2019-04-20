from listings.models import Transaction,Product
from mlxtend.frequent_patterns import apriori
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder

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
product = 1
sub_dataset = []
for i in num:
    if product in i:
        sub_dataset.append(i)
    # pip install mlxtend
    # pip install pandas
te = TransactionEncoder()
te_ary = te.fit(sub_dataset).transform(sub_dataset)
df = pd.DataFrame(te_ary, columns=te.columns_)
df1 = df
df1[product] = False
df2 = apriori(df1, min_support=0.6, use_colnames=True)
print(df2)
