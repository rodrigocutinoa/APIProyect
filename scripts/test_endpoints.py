import httpx

base = 'http://127.0.0.1:8000'

with httpx.Client(base_url=base, timeout=10.0) as client:
    print('GET /items')
    response = client.get('/items')
    print(response.status_code, response.text)

    print('POST /items')
    response = client.post('/items', json={'name': 'test-item', 'description': 'desc', 'metadata': {'foo': 'bar'}})
    print(response.status_code, response.text)
    item = response.json()
    item_id = item['_id']

    print('GET /items/{item_id}')
    response = client.get(f'/items/{item_id}')
    print(response.status_code, response.text)

    print('PUT /items/{item_id}')
    response = client.put(f'/items/{item_id}', json={'description': 'updated'})
    print(response.status_code, response.text)

    print('GET /items after update')
    response = client.get('/items')
    print(response.status_code, response.text)

    print('DELETE /items/{item_id}')
    response = client.delete(f'/items/{item_id}')
    print(response.status_code, response.text)

    print('GET /items after delete')
    response = client.get('/items')
    print(response.status_code, response.text)

    print('GET nonexistent item')
    response = client.get('/items/000000000000000000000000')
    print(response.status_code, response.text)
