# Virtual Library

## Application:
#### App runs on port 80.
#### To run it, write `docker-compose up`

## App commands:  

### POST
#### To add new book to library
#### To create new record in library, author, title, year and isbn are required. Author and title variables are strings, year and isbn are integers.
#### If you want to create a book, you need to sent `post` request to `http://localhost/api/bookList`
#### The request should look like this:
```
{
"author" : "someone",
"title" : "something",
"year" : year,
"isbn" : isbn,
"part" : partID
}
```
#### This is how record is created:
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
#### An example:
```
{
    "author" : "Michael P. Papazoglou",
    "title" : "Web Services: Principles and Technology",
    "year" : 2007,
    "isbn" : 321155556,
    "part" : 1
}
```
#### If you want to add a book and also a part, you need to sent `post` request to `http://localhost/api/extendedBookList`
#### The request should look like this:
```
{
"author" : "someone",
"title" : "something",
"year" : year,
"isbn" : isbn
"part" : {
        "manufacturer": "new manufacturer",
        "name": "new name",
        "price": "new price",
        "type": "new type"
    }
}
```
#### If you want to add only a part, you need to sent `post` request to `http://localhost/api/parts`
#### The request should look like this:
```
{
"manufacturer": "new manufacturer",
"name": "new name",
"price": "new price",
"type": "new type"
}
```
## Response:
* On successful request, status `201` and new record data are returned
* On failure, status `400` is returned


### GET
#### Actions:
* Get all the books in library
`http://localhost/api/bookList/`
* Get a book from library using id
`http://localhost/api/bookList/<bookID>`
* Get an expanded books from library
`http://localhost/api/extendedBookList`
* Get an expanded book from library using id
`http://localhost/api/extendedBookList<bookID>`
* Get parts list
`http://localhost/api/parts`
* Get books part
`http://localhost/api/bookList/<bookID>/part`
## Response:
* On successful request, status `200` is returned
* On failure, status `404` is returned


### PUT
#### Change values of specific book:
`http://localhost/api/bookList/<bookID>`
#### There are possibility to change any book value. Request need to be json type. 
#### Note: Here you can change only books part ID.
#### If you want to change the isbn of the book, you need to sent `put` request and it sould look like this:
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
#### Change values of specific book and its part at the same time:
`http://localhost/api/extendedBookList/<bookID>`
#### Request need to be json type.
#### If you want to change the isbn of the book, you need to sent `put` request and it sould look like this:
```
{
"author" : "new_name",
"title" : "new_title",
"year" : new_year,
"isbn" : new_isbn,
"part" : {
    "manufacturer": "new manufacturer",
    "name": "new name",
    "price": "new price",
    "type": "new type"
    }
}
```
#### It is possible to use less variables
## Response:
* On successful request, status `200` is returned
* On failure, status `400` is returned


### DELETE
#### To remove book by id:
`http://127.0.0.1/api/bookList/<bookID>`
#### or
`http://127.0.0.1/api/extendedBookList/<bookID>`

## Response:
* On successful request, status `204` is returned and changed data are returned
* On failure, status `404` is returned
