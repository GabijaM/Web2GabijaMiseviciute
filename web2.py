from flask import Flask, Response, request, jsonify, abort
import json
import requests

# URL = "http://jokubasb:5000/"

application = Flask(__name__)  

books = [
    {"id" : 1,
    "author" : "J. K. Rowling",
    "title" : "Harry Potter and the Philosopher's stone",
    "year" : 1997,
    "isbn" : 9780590353403,
    "car" : 1
    },
    {"id" : 2,
    "author" : "J. K. Rowling",
    "title" : "Harry Potter and the Chamber of secrets",
    "year" : 1998,
    "isbn" : 9788498387650,
    "car" : 2
    },
    {"id" : 3,
    "author" : "Charles Dickens",
    "title" : "A tale of Two Cities",
    "year" : 1859,
    "isbn" : 9780721407104,
    "car" : 3
    },
    {"id" : 4,
    "author" : "Antoine de Saint-Exupery",
    "title" : "The Little Prince",
    "year" : 1943,
    "isbn" : 9788854172388,
    "car" : 4
    }]

# url = "http://localhost/api/v1/ownedcarsArray/"

# cars = [
#     {
#         "manufacturer": "Subaru",
#         "model": "Impreza",
#         "year": 2005,
#         "surname": "Bird",
#         "name": "Edwin",
#         "number": "606-434-2825",
#         "email": "EdwinRBird@armyspy.com"
#     },
#     {
#         "manufacturer": "Toyota",
#         "model": "Corolla",
#         "year": 2010,
#         "surname": "Patterson",
#         "name": "Sarah",
#         "number": "321-512-3924",
#         "email": "SarahHPatterson@rhyta.com"
#     },
#     {
#         "manufacturer": "Tesla",
#         "model": "Model3",
#         "year": 2016,
#         "surname": "Hayner",
#         "name": "Alisha",
#         "number": "678-237-3632",
#         "email": "AlishaJHayner@armyspy.com"
#     },
#     {
#         "manufacturer": "Dodge",
#         "model": "Challenger",
#         "year": 2018,
#         "surname": "Moorhead",
#         "name": "Amanda",
#         "number": "989-397-1216",
#         "email": "AmandaCMoorhead@teleworm.us"
#     }
# ]

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
        if ("author" in newRecord) and ("title" in newRecord) and ("year" in newRecord) and ("isbn" in newRecord) and ("car" in newRecord):
            add = "{ author: " + newRecord["author"] + ", title: " + newRecord["title"] + ", year: " + str(newRecord["year"]) + ", isbn: " + str(newRecord["isbn"]) + ", car: " + str(newRecord["car"]) + "}"
            newBook = {
                "id" : books[len(books)-1]["id"] + 1,
                "author" : newRecord["author"],
                "title" : newRecord["title"],
                "year" : newRecord["year"],
                "isbn" : newRecord["isbn"],
                "car" : newRecord["car"]
            }
            books.append(newBook)
            return Response((json.dumps({"Success":"Book was added; " + add})), status=201, headers={"location": "/api/bookList/"+str(books[len(books)-1]["id"])}, mimetype="application/json")

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
            if "car" not in newRecord:
                error += "car."
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

        if ("author" not in updateBook) and ("title" not in updateBook) and ("year" not in updateBook) and ("isbn" not in updateBook) and ("car" not in updateBook):
            return Response(json.dumps({"Failure" : "No data is given for update"}),status=400,mimetype="application/json")

        update = "This data have been changed: "

        if "author" in updateBook:
            update += "AUTHOR: [" + book[0]["author"] + "] -> ["
            book[0]["author"] = updateBook["author"]
            update += book[0]["author"] + "]; "
        if "title" in updateBook:
            update += "TITLE: [" + book[0]["title"] + "] -> ["
            book[0]["title"] = updateBook["title"]
            update += book[0]["title"] + "]; "
        if "year" in updateBook:
            update += "YEAR: [" + str(book[0]["year"]) + "] -> ["
            book[0]["year"] = updateBook["year"]
            update += str(book[0]["year"]) + "]; "
        if "isbn" in updateBook:
            update += "ISBN: [" + str(book[0]["isbn"]) + "] -> ["
            book[0]["isbn"] = updateBook["isbn"]
            update += str(book[0]["isbn"]) + "]; "
        if "car" in updateBook:
            update += "CAR: [" + str(book[0]["car"]) + "] -> ["
            book[0]["car"] = updateBook["car"]
            update += str(book[0]["car"]) + "]; "

        return Response(json.dumps({"Success" : update}),status=200,mimetype="application/json")

    elif request.method == "DELETE":
        for bookDEL in books:
            if bookDEL["id"] == bookID:
                books.remove(bookDEL)
                return Response(json.dumps({"Success" : "Book with id "+str(bookID)+" have been deleted"}),status=204,mimetype="application/json")

# @application.route("/api/cars", methods = ["GET", "POST"])
# def apiCars():
#     if request.method == "GET":  
#         req = requests.get(URL + "cars/")
#         return jsonify(req.json())#here

    # elif request.method == "POST":
    #     new_data = request.get_json("force=True")
    #     resp = requests.post(URL+"cars", json = (new_data), )
    #     if str(resp.status_code) == "400" or str(resp.status_code) == "404":
    #         return Response(json.dumps({"Failure" : resp.text}),status=resp.status_code,mimetype="application/json")
    #     else:
    #          return Response(json.dumps({"Success" : resp.text}),status=resp.status_code,mimetype="application/json")

# @application.route("/api/bookList/<int:bookID>/carID", methods = ["GET"])
# def apiCarInfo(bookID):
#     book = [book for book in books if book["id"] == bookID]
#     if len(book) != 1:
#         abort(404)
    
#     if request.method == "GET":
#         req = requests.get(URL+"phones/"+str(book[0]["car"]))
#         return jsonify(req.json())#here


if __name__ == "__main__":
    application.run(host = "0.0.0.0", port = 80, debug = True)