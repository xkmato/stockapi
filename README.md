**Stock API**

```
git clone https://github.com/xkmato/stockapi

cd stockapi

./manage.py test

./manage.py migrate

./manage.py runserver

```

To access the api go to:
 
 GET `http://localhost/stock` For list of stocks
 POST `http://localhost/stock` with relevant data to create or update a stock
 
 Call command `python manage.py update_stock <stockid> <new_price>`
 
 