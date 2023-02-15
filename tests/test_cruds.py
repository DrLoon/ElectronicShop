from conftest import client
import schemas


def test_add_product():
    pr = schemas.Product(name='Iphone 14', price=100)
    response = client.post('/api/product', json=pr.dict())
    assert response.status_code == 200
    assert response.json() == pr.dict()

    response = client.post('/api/product', json=pr.dict())
    assert response.status_code == 404
    assert response.json() == {"detail": "Probably, such a product has already been added"}

    assert client.post('/api/product', json={"as": 'asd', 'asd': 0}).status_code == 422
    assert client.post('/api/product', json={"name": 'coco', 'price': -1}).status_code == 422


def test_get_products():
    response = client.get("api/products/?"
                          "name=string&"
                          "sort_by_name=false&"
                          "sort_by_price=false&"
                          "ascending_name=true&"
                          "ascending_price=true")
    assert response.status_code == 200
    assert response.json() == []

    assert client.post('/api/product', json={"name": 'gadget', 'price': 323}).status_code == 200
    response = client.get("api/products/?"
                          "name=gadget&"
                          "sort_by_name=false&"
                          "sort_by_price=false&"
                          "ascending_name=true&"
                          "ascending_price=true")
    assert response.status_code == 200
    assert response.json() == [{"name": "gadget", "price": 323}]
    assert client.get("api/products/?name=gadget").status_code == 200
