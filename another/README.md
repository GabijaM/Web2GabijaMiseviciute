# PC Parts List

## Launching app
App runs on port 5000
``` docker-compose up ```

## Usage

### GET

**Get all parts**

```http://localhost:5000/api/parts ```

**Get specific part by id**

```http://localhost:5000/api/parts/<id> ```

**Response**
- On success - returns part/parts and status `200`
- On failure - status `404`

### POST

**Posting new part**

```localhost:5000/api/parts?manufacturer=X&name=Y&type=Z&price=D```

It will create new part:
    {'id': max_id+1,
     'manufacturer': X,
     'name': Y,
     'type': Z,
     'price': D
    }

**Response**
- On success - Address to new part ant status `201`
- On failure - status `400`

### DELETE

**Removing part by part id**

```http://localhost:5000/api/parts/<id> ```

**Response**
- On success - status `204`
- On failure - status `404`

### PUT

**Changing values of specific part**

***Changing part name***

```http://localhost:5000/api/parts/<id>?name=new_name ```

***Changing part manufacturer***

```http://localhost:5000/api/parts/<id>?manufacturer=new_manufacturer ```

***Changing part type***

```http://localhost:5000/api/parts/<id>?type=new_type ```

***Changing part price***

```http://localhost:5000/api/parts/<id>?price=new_price ```

**Response**
- On success - status `201`
- On failure - status `400`