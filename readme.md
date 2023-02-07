# Микросервис для электронного магазина

Чтобы запустить:
1) docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres
2) pip install -r requirements.txt
3) python main.py

Тестовый сценарий:
1) `$ curl -X 'POST' 'http://127.0.0.1:8000/add_product' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"name": "IPhone 14", "price": 800}'` 
Добавляет товар с названием и ценой

2) `$ curl -X 'GET' 'http://127.0.0.1:8000/products/?name=IPhone%2014&price=800&sort_by_name=true&sort_by_price=true&ascending_name=true&ascending_price=false' -H 'accept: application/json'` 
Возвращает товары с фильтрацией и сортировкой по названию и цене по возрастанию или по убыванию

3) `curl -X 'GET' 'http://127.0.0.1:8000/product_names/?name=IPhone&price=800&sort_by_name=true&sort_by_price=true&ascending_name=true&ascending_price=false' -H 'accept: application/json'`
Возвращает только названия товаров с фильтрацией и сортировкой по названию и цене по возрастанию или по убыванию

4) `curl -X 'POST' 'http://127.0.0.1:8000/add_product_to_cart?product_name=IPhone%2014' -H 'accept: application/json' -d ''`
Добавляет товар в корзину

5) `curl -X 'POST' 'http://127.0.0.1:8000/change_cart_product_amount?product_name=IPhone%2014&new_amount=42' -H 'accept: application/json' -d ''`
Меняет количество товара в корзине, удаляет товар из корзины, если передать 0
