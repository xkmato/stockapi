[![Build Status](https://travis-ci.org/xkmato/stockapi.svg?branch=master)](https://travis-ci.org/xkmato/stockapi)

**Stock API**

```
git clone https://github.com/xkmato/stockapi

cd stockapi

./manage.py test

./manage.py migrate

./manage.py runserver

```

Authentication

Visit `https://localhost:8000/admin/` to create some users

Go to `http://localhost:8000/o/application/` to create an app

Do `curl -X POST -d "grant_type=password&username=<user_name>&password=<password>" -u"<client_id>:<client_secret>" http://localhost:8000/o/token/` to get an access token


To access the api go to:
 
 ```
curl -H "Authorization: Bearer <your_access_token>" http://localhost:8000/stocks/ #List the stocks
curl -H "Authorization: Bearer <your_access_token>" -X POST -d"name=foo&description=bar&launch_date=2019-03-02" http://localhost:8000/stocks/ #Post new stock
```
Checkout the tests to see how to update stock prices

Call command `python manage.py update_stock <stockid> <new_price>` with crontab
 
 