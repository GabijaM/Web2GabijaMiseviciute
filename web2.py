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
    "part" : 3
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
    "part" : 2
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

@application.route("/api/books", methods = ["GET"])
def getBookList():

    booksToReturn = []

    args = request.args
    expand = args.get('expand')
        
    if (expand == "part"):
        for book in books:
            booksWithPart = book.copy()
            try:
                get = requests.get(URL + "api/parts/" + str(book["part"]))
                getPart = {
                    "manufacturer" : get.json()[0]["manufacturer"],
                    "name" : get.json()[0]["name"],
                    "type" : get.json()[0]["type"],
                    "price" : get.json()[0]["price"]
                }
                booksWithPart["part"] = getPart

            except requests.exceptions.RequestException as ex:
                print(ex)
            booksToReturn.append(booksWithPart)
        return Response(json.dumps(booksToReturn),status=200,mimetype="application/json")

    else:
        return Response(json.dumps(books),status=200,mimetype="application/json")

@application.route("/api/books", methods = ["POST"])
def postBookList():
    newRecord = request.get_json("force: True")      
    
    if ("expand" in request.args):
        if ("author" in newRecord) and ("title" in newRecord) and ("year" in newRecord) and ("isbn" in newRecord) and ("part" in newRecord):
            if type(newRecord["part"]) == type(0):
                return Response(json.dumps({"Failure" : "Request expects json type part"}),status=400,mimetype="application/json")
            if ("manufacturer" in newRecord["part"]) and ("name" in newRecord["part"]) and ("price" in newRecord["part"]) and ("type" in newRecord["part"]):
                postPart = {
                    "manufacturer" : newRecord["part"]["manufacturer"],
                    "name" : newRecord["part"]["name"],
                    "price" : newRecord["part"]["price"],
                    "type" : newRecord["part"]["type"]
                }
                try:
                    post = requests.post(URL + "api/parts", json = postPart)
                    getPart = requests.get(URL + "/api/parts")
                    returnPart = {
                        "id" : getPart.json()[len(getPart.json())-1]["id"],
                        "manufacturer" : getPart.json()[len(getPart.json())-1]["manufacturer"],
                        "name" : getPart.json()[len(getPart.json())-1]["name"],
                        "price" : getPart.json()[len(getPart.json())-1]["price"],
                        "type" : getPart.json()[len(getPart.json())-1]["type"]
                    }
                except requests.exceptions.RequestException as ex:
                    return Response(json.dumps({"Failure" : "Can not connect to the server"}),status="503",mimetype="application/json")

                if(str(post.status_code) == "400" or str(post.status_code) == "404"):
                    return Response(json.dumps({"Failure" : "error code: " +str(post.status_code)}),status=post.status_code,mimetype="application/json")

                else:
                    newBook = {
                        "id" : books[len(books)-1]["id"] + 1,
                        "author" : newRecord["author"],
                        "title" : newRecord["title"],
                        "year" : newRecord["year"],
                        "isbn" : newRecord["isbn"],
                        "part" : getPart.json()[len(getPart.json())-1]["id"]
                    }

                    returnBook = newBook.copy()
                    returnBook["part"] = returnPart

                    books.append(newBook)
                    bookID = returnBook["id"]
                    return Response((json.dumps({"Success":"Book was added; "})+json.dumps(returnBook)), status=201, headers={"location": "/api/extendedBookList/"+str(bookID)},mimetype="application/json")
            
            else:
                error = "This data has not been given: "
                if "manufacturer" not in newRecord["part"]:
                    error += "manufacturer; "
                if "name" not in newRecord["part"]:
                    error += "name; "
                if "price" not in newRecord["part"]:
                    error += "price; "
                if "type" not in newRecord["part"]:
                    error += "type."
                return Response(json.dumps({"Failure" : error}),status=400,mimetype="application/json")
        
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

    else:
        if ("author" in newRecord) and ("title" in newRecord) and ("year" in newRecord) and ("isbn" in newRecord) and ("part" in newRecord):
            if type(newRecord["part"]) == type(0):
                newBook = {
                    "id" : books[len(books)-1]["id"] + 1,
                    "author" : newRecord["author"],
                    "title" : newRecord["title"],
                    "year" : newRecord["year"],
                    "isbn" : newRecord["isbn"],
                    "part" : newRecord["part"]
                }
                books.append(newBook)

                return Response((json.dumps({"Success":"Book was added; "})+json.dumps(newBook)), status=201, headers={"location": "/api/bookList/"+str(books[len(books)-1]["id"])}, mimetype="application/json")
            error = "Request expects part id"
            return Response(json.dumps({"Failure" : error}),status=400,mimetype="application/json")

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

# ---------------------------------------------------------------------------------------------------------------------------------------

@application.route("/api/books/<int:bookID>", methods = ["GET"])
def getBookByID(bookID):

    book = [book for book in books if book["id"] == bookID]

    if len(book) != 1:
        abort(404)

    args = request.args
    expand = args.get('expand')
        
    if (expand == "part"):
        returnBook = {
            "author" : book[0]["author"],
            "title" : book[0]["title"],
            "year" : book[0]["year"],
            "isbn" : book[0]["isbn"],
            "part" : book[0]["part"]
        }
        try:
            get = requests.get(URL + "api/parts/" + str(book[0]["part"]))
            getPart = {
            "manufacturer" : get.json()[0]["manufacturer"],
            "name" : get.json()[0]["name"],
            "type" : get.json()[0]["type"],
            "price" : get.json()[0]["price"]
            }
            returnBook["part"] = getPart
        except requests.exceptions.RequestException as ex:
            print(ex)

        return Response(json.dumps(returnBook), status=200,mimetype="application/json")

    else:
        returnBook = {
            "author" : book[0]["author"],
            "title" : book[0]["title"],
            "year" : book[0]["year"],
            "isbn" : book[0]["isbn"],
            "part" : book[0]["part"]
        }
        return Response((json.dumps(returnBook)), status=200,mimetype="application/json")

@application.route("/api/books/<int:bookID>", methods = ["PUT"])
def putBookByID(bookID):
    book = [book for book in books if book["id"] == bookID]

    if len(book) != 1:
        abort(404)

    updateBook = request.get_json("force: True")

    if ("author" not in updateBook) and ("title" not in updateBook) and ("year" not in updateBook) and ("isbn" not in updateBook) and ("part" not in updateBook):
        return Response(json.dumps({"Failure" : "No data is given for update"}),status=400,mimetype="application/json")

    update = "This data have been changed: "

    if ("expand" in request.args):
        if type(updateBook["part"]) == type(0):
            return Response(json.dumps({"Failure" : "Request expects json type part"}),status=400,mimetype="application/json")

        if ("manufacturer" not in updateBook["part"]) and ("name" not in updateBook["part"]) and ("price" not in updateBook["part"]) and ("type" not in updateBook["part"]):
            return Response(json.dumps({"Failure" : "No data is given for book part"}),status=400,mimetype="application/json")

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

            returnBook = {
                "author" : book[0]["author"],
                "title" : book[0]["title"],
                "year" : book[0]["year"],
                "isbn" : book[0]["isbn"],
                "part" :  book[0]["part"]
            }
            try:
                put = requests.put(URL + "api/parts/" + str(book[0]["part"]), json = updateBook["part"])
                update += "part; "
                get = requests.get(URL + "api/parts/" + str(book[0]["part"]))
                getPart = {
                    "manufacturer" : get.json()[0]["manufacturer"],
                    "name" : get.json()[0]["name"],
                    "type" : get.json()[0]["type"],
                    "price" : get.json()[0]["price"]
                }
                returnBook["part"] = getPart
            except requests.exceptions.RequestException as ex:
                update += "(part could not be changed because of connection error)"
            
        return Response(json.dumps({"Success" : str(update)})+json.dumps(returnBook),status="200",mimetype="application/json")

    else:
        if type(updateBook["part"]) == type(0):
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

            returnBook = {
                "author" : book[0]["author"],
                "title" : book[0]["title"],
                "year" : book[0]["year"],
                "isbn" : book[0]["isbn"],
                "part" : book[0]["part"]
            }

            return Response(json.dumps({"Success" : update})+json.dumps(returnBook),status="200",mimetype="application/json")

        error = "Request expects part id"
        return Response(json.dumps({"Failure" : error}),status=400,mimetype="application/json")

@application.route("/api/books/<int:bookID>", methods = ["DELETE"])
def deleteBookByID(bookID):

    for bookDEL in books:
        if bookDEL["id"] == bookID:
            books.remove(bookDEL)
            return Response(json.dumps({"Success" : "Book with id "+str(bookID)+" have been deleted"}),status=200,mimetype="application/json")

# ---------------------------------------------------------------------------------------------------------------------------------------
    
@application.route("/api/books/<int:bookID>/part", methods = ["GET"])
def getBooksPartByID(bookID):
    book = [book for book in books if book["id"] == bookID]

    if len(book) == 0:
        abort(404)
    
    get = requests.get(URL + "/api/parts/" + str(book[0]["part"]))
    part = {
        "manufacturer" : get.json()[0]["manufacturer"],
        "name" : get.json()[0]["name"],
        "type" : get.json()[0]["type"],
        "price" : get.json()[0]["price"]
    }
    return Response(json.dumps(part),status="200",mimetype="application/json")

if __name__ == "__main__":
    application.run(host = "0.0.0.0", port = 80, debug = True)