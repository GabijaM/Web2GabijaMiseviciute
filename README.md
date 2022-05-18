# Virtual Library

## Application:
#### App runs on port 80.
#### To run it, write `docker-compose up`

## App commands:  

### POST
#### To add new book to library
#### To create new record in library, author, title, year, isbn and compiuter part are required. Author and title variables are strings, year and isbn are integers, part could be id or full json. Part contains manufacturer, name, price ant type, all of these are string type.
#### If you want to create a book, you need to sent `post` request to `http://127.0.0.1/api/books`
#### If you want to add book in a simple way, the request should look like this with added parameter `list`:
```
{
"author" : "someone",
"title" : "something",
"year" : year,
"isbn" : isbn,
"part" : partID
}
```
#### If you want to add book in a expanded way, the request should look like this with added parameter `expand_list`:
```
{
"author" : "someone",
"title" : "something",
"year" : year,
"isbn" : isbn,
"part" : {
    "manufacturer" : "manufacturer",
    "name" : "name",
    "price" : price,
    "type" : type
    }
}
```
### This is how record is created:
```
{
"id" : last_library_book_id + 1
"author" : "someone",
"title" : "something",
"year" : year,
"isbn" : isbn,
"part" : partID
}
```
#### OR
#### if the post request is with expanded part, the part is added to another server using `post` request to it. To book only added part id:
```
{
...
"part" : partID
}
```
#### AND `post` to http://web2:5000/api/parts with:
```
{
"manufacturer" : "manufacturer",
"name" : "name",
"price" : price,
"type" : type
}
```
#### NOTE: doing `post` request, all fields are requared.
#### An example with parameter `expand_list`:
```
{
    "author" : "Michael P. Papazoglou",
    "title" : "Web Services: Principles and Technology",
    "year" : 2007,
    "isbn" : 321155556,
    "part" : {
        "manufacturer": "ASRock",
        "name": "AB350 PRO4",
        "type": "Motherboard",
        "price": "74.69"
        }
}
```
#### An example with parameter `list`:
```
{
    "author" : "Michael P. Papazoglou",
    "title" : "Web Services: Principles and Technology",
    "year" : 2007,
    "isbn" : 321155556,
    "part" : 2
}
```

## Response:
* On successful request, status `201` and new record data are returned
* On failure, status `400` is returned


## GET
### Actions using `get` request:
* Get all the books in library, use parameter `list`:  
`http://127.0.0.1/api/books` 
* Get all the books in library with their expanded part, use parameter `expand_list`:  
`http://127.0.0.1/api/books` 
* Get a book from library using id, use parameter `list`:  
`http://127.0.0.1/api/books/<bookID>`
* Get book from library with expanded part use parameter `expand_list`:  
`http://127.0.0.1/api/books/<bookID>`
* Get book part using book id:  
`http://127.0.0.1/api/books/<bookID>/part`

## Response:
* On successful request, status `200` is returned
* On failure, status `404` is returned


## PUT
### Change values of specific book using `put` request:
`http://127.0.0.1/api/books/<bookID>`
#### There are possibility to change any book value. Request need to be json type. 
#### If you want to change the isbn of the book using `list` or `expand_list` parameter, request sould look like this:
```
{"isbn" : new_isbn}
```
#### At the same you can modify multiple values:
```
{
"name" : "new name"
...
"isbn" : new_isbn,
}
```
### Change values of specific book and its part at the same time:
#### Request need to be json type.
#### If you want to change the `isbn` of the book and `parts values` , request sould look like this:
#### NOTE: in this example way, it is needed to select parameter `expand_list`
```
{
"isbn" : new_isbn,
"part" : {
    "manufacturer": "new manufacturer",
    "name": "new name",
    "price": "new price",
    "type": "new type"
    }
}
```
#### If you want to change the `name` of the book and `part id` , request sould look like this:
#### NOTE: in this example way, it is needed to select parameter `list`
```
{
"name" : "new name",
"part" : new id
}
```
## Response:
* On successful request, status `200` is returned
* On failure, status `400` is returned

### DELETE
#### To remove book by id:
`http://127.0.0.1/api/books/<bookID>`

## Response:
* On successful request, status `200` is returned and changed data are returned
* On failure, status `404` is returned
