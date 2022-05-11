from flask import Flask, Response, request, jsonify, abort
import json
import requests

URL = "http://web2:5000/"

application = Flask(__name__)  

books = [
    {"id" : 1,
    "author" : "J. K. Rowling",
    "title" : "Harry Potter and the Philosopher's stone",
    "year" : 1997,
    "isbn" : 9780590353403,
    "part" : 0
    },
    {"id" : 2,
    "author" : "J. K. Rowling",
    "title" : "Harry Potter and the Chamber of secrets",
    "year" : 1998,
    "isbn" : 9788498387650,
    "part" : 2
    },
    {"id" : 3,
    "author" : "Charles Dickens",
    "title" : "A tale of Two Cities",
    "year" : 1859,
    "isbn" : 9780721407104,
    "part" : 1
    },
    {"id" : 4,
    "author" : "Antoine de Saint-Exupery",
    "title" : "The Little Prince",
    "year" : 1943,
    "isbn" : 9788854172388,
    "part" : 1
    }]

@application.route("/")
def homePage():
    return "<h1>Welcome to virtual library!</h1><a href='http://127.0.0.1:80/api/bookList'>To see all books</a>"

@application.route("/api/bookList", methods = ["GET", "POST"])
def bookList():
    if request.method == "GET":
        if "author" in request.args:
            booksToReturn = []
            for book in books:
                booksToReturn.append({"id" : book["id"], "author" : book["author"]})
            return jsonify(booksToReturn)
        elif "title" in request.args:
            booksToReturn = []
            for book in books:
                booksToReturn.append({"id" : book["id"], "title" : book["title"]})
            return jsonify(booksToReturn)
        return jsonify(books)

    elif request.method == "POST":
        newRecord = request.get_json("force: True")
        if ("author" in newRecord) and ("title" in newRecord) and ("year" in newRecord) and ("isbn" in newRecord) and ("part" in newRecord):
            newBook = {
                "id" : books[len(books)-1]["id"] + 1,
                "author" : newRecord["author"],
                "title" : newRecord["title"],
                "year" : newRecord["year"],
                "isbn" : newRecord["isbn"],
                "part" : newRecord["part"]
            }
            books.append(newBook)
            return Response((json.dumps({"Success":"Book was added; "})+json.dumps(newRecord)), status=201, headers={"location": "/api/bookList/"+str(books[len(books)-1]["id"])}, mimetype="application/json")

        else:
            error = "This data has not been given: "
            if "author" not in newRecord:
                error += "author; "
            if "title" not in newRecord:
                error += "title; "
            if "year" not in newRecord:
                error += "year; "
            if "isbn" not in newRecord:
                error += "isbn;"
            if "part" not in newRecord:
                error += "part."
            return Response(json.dumps({"Failure" : error}),status=400,mimetype="application/json")

@application.route("/api/bookList/<int:bookID>", methods = ["GET", "PUT","DELETE"])
def bookListID(bookID):

    book = [book for book in books if book["id"] == bookID]
    if len(book) != 1:
        abort(404)

    if request.method == "GET":
        return jsonify(book)

    elif request.method == "PUT":
        updateBook = request.get_json("force: True")

        if ("author" not in updateBook) and ("title" not in updateBook) and ("year" not in updateBook) and ("isbn" not in updateBook) and ("part" not in updateBook):
            return Response(json.dumps({"Failure" : "No data is given for update"}),status=400,mimetype="application/json")

        update = "This data have been changed: "
        previousBook = book

        if "author" in updateBook:
            book[0]["author"] = updateBook["author"]
            update += "author; "
        if "title" in updateBook:
            book[0]["title"] = updateBook["title"]
            update += "title; "
        if "year" in updateBook:
            book[0]["year"] = updateBook["year"]
            update += "year; "
        if "isbn" in updateBook:
            book[0]["isbn"] = updateBook["isbn"]
            update += "isbn; "
        if "part" in updateBook:
            book[0]["part"] = updateBook["part"]

        return Response(json.dumps({"Success" : update})+json.dumps(book),status="200",mimetype="application/json")

    elif request.method == "DELETE":
        for bookDEL in books:
            if bookDEL["id"] == bookID:
                books.remove(bookDEL)
                return Response(json.dumps({"Success" : "Book with id "+str(bookID)+" have been deleted"}),status=204,mimetype="application/json")

# ============================

@application.route("/api/extendedBookList", methods = ["GET", "POST"])
def extendedBookList():
    if request.method == "GET":
        booksToReturn = []
        for book in books:
            booksWithPart = book.copy()
            try:
                get = requests.get(URL + "api/parts/" + str(book["part"]))
                booksWithPart["part"] = get.json()
            except requests.exceptions.RequestException as ex:
                print(ex)
            booksToReturn.append(booksWithPart)
        return jsonify(booksToReturn)

    if request.method == "POST":
        newRecord = request.get_json("force=True")

        if ("author" in newRecord) and ("title" in newRecord) and ("year" in newRecord) and ("isbn" in newRecord) and ("part" in newRecord):
            try:
                post = requests.post(URL + "api/parts", json = newRecord["part"])
                getID = requests.get(URL + "/api/parts")
                id = getID.json()[len(getID.json())-1]["id"]
            except requests.exceptions.RequestException as ex:
                return Response(json.dumps({"Failure" : "Can not connect to the server"}),status="503",mimetype="application/json")

            if(str(post.status_code) == "400" or str(post.status_code) == "404"):
                return Response(json.dumps({"Failure" : "error code: " + str(post.status_code)}),status=post.status_code,mimetype="application/json")

            else:
                newBook = {
                    "id" : books[len(books)-1]["id"] + 1,
                    "author" : newRecord["author"],
                    "title" : newRecord["title"],
                    "year" : newRecord["year"],
                    "isbn" : newRecord["isbn"],
                    "part" : id
                }
                books.append(newBook)
                bookID = books[len(books)-1]["id"]
                return Response((json.dumps({"Success":"Book was added; "})+json.dumps(newRecord)), status=201, headers={"location": "/api/extendedBookList/"+str(bookID)},mimetype="application/json")
        else:
            error = "This data has not been given: "
            if "author" not in newRecord:
                error += "author; "
            if "title" not in newRecord:
                error += "title; "
            if "year" not in newRecord:
                error += "year; "
            if "isbn" not in newRecord:
                error += "isbn;"
            if "part" not in newRecord:
                error += "part."
            return Response(json.dumps({"Failure" : error}),status=400,mimetype="application/json")
            

@application.route("/api/extendedBookList/<int:bookID>", methods = ["GET", "PUT", "DELETE"])
def extendedBookListID(bookID):

    book = [book for book in books if book["id"] == bookID]

    if len(book) == 0:
        abort(404)

    if request.method == "GET":
        bookWithPart = book.copy()
        try:
            get = requests.get(URL + "api/parts/" + str(book[0]["part"]))
            bookWithPart[0]["part"] = get.json()
        except requests.exceptions.RequestException as ex:
            print(ex)
        return jsonify(bookWithPart)

    elif request.method == "PUT":
        updateBook = request.get_json("force=True") 
        bookWithPart = book.copy()

        if ("author" not in updateBook) and ("title" not in updateBook) and ("year" not in updateBook) and ("isbn" not in updateBook) and ("part" not in updateBook):
            return Response(json.dumps({"Failure" : "No data is given for update"}),status=400,mimetype="application/json")

        update = "This data have been changed: " 

        if "author" in updateBook:
            book[0]["author"] = updateBook["author"]
            # update += "author; "
        if "title" in updateBook:
            book[0]["title"] = updateBook["title"]
            # update += "title; "
        if "year" in updateBook:
            book[0]["year"] = updateBook["year"]
            # update += "year; "
        if "isbn" in updateBook:
            book[0]["isbn"] = updateBook["isbn"]
            # update += "isbn; "
        if "part" in updateBook:
            try:
                index = book[0]["part"]
                put = requests.put(URL + "api/parts/" + str(index), json = updateBook["part"])
                # update += "part; "
                update = URL + "api/parts/" + str(index)
            except requests.exceptions.RequestException as ex:
                update += "(part could not be changed because of connection error)"

            # try:
            #     get = requests.get(URL + "api/parts/" + str(index))
            #     bookWithPart[0]["part"] = get.json()
            # except requests.exceptions.RequestException as ex:
            #     print(ex)

        return Response(json.dumps({"Success" : str(update)})+json.dumps(book),status="200",mimetype="application/json")

    elif request.method == "DELETE":
        for book in books:
            if book["id"] == bookID:
                books.remove(book)
                return Response(json.dumps({"Success" : "Deleted"}),status=204, mimetype="application/json")

#======================================

@application.route("/api/parts", methods = ["GET", "POST"])
def partsList():
    if request.method == "GET":
        getParts = requests.get(URL + "/api/parts")
        return jsonify(getParts.json())

    elif request.method == "POST":
        newRecord = request.get_json("force=True")
        response = requests.post(URL+"/api/parts",json = (newRecord), )
        getID = requests.get(URL + "/api/parts")
        id = getID.json()[len(getID.json())-1]["id"]
        if str(response.status_code) == "400" or str(response.status_code) == "404":
            return Response(json.dumps({"Failure" : "error code: " + str(response.status_code) + response.text}),status=response.status_code,mimetype="application/json")
        else:
            return Response((json.dumps({"Success":"Book was added; "})+json.dumps(newRecord)), status=201, headers={"location": "/api/parts/"+str(id)},mimetype="application/json")

@application.route("/api/bookList/<int:bookID>/part", methods = ["GET"])
def bookListIDPart(bookID):
    book = [book for book in books if book["id"] == bookID]

    if len(book) == 0:
        abort(404)

    if request.method == "GET":
        parts = requests.get(URL + "/api/parts/" + str(book[0]["part"]))
        return jsonify(parts.json()) 

#======================================

if __name__ == "__main__":
    application.run(host = "0.0.0.0", port = 80, debug = True)