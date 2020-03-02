# Adapted from the code found at https://github.com/knightsamar/CS340_starter_flask_app/blob/master/starter_website/webapp.py

from flask import Flask, render_template
from flask import request, redirect
from db_connector.db_connector import connect_to_database, execute_query

#create the web app
webapp = Flask(__name__)
@webapp.route('/hello')
def hello():
    return "Hello World!"

# @webapp.route('/')
# def index():
#     return render_template('index.html')

@webapp.route('/index.html')
def index():
    return render_template('index.html')

# def author_id(a_id):
#     db_connection = connect_to_database()
#     query = "SELECT title FROM books WHERE bookID IN (SELECT bookID FROM authorBooks WHERE authorID = %s)" % a_id
#     books = execute_query(db_connection,query)
#     titles = books.fetchall()
#     for t in titles:
#         print(t)
#     return books
@webapp.route('/author.html', methods=['POST','GET'])
def author():
    print("Fetching author information table")
    db_connection = connect_to_database()
    query = "SELECT * FROM authors"
    result = execute_query(db_connection,query)
    print(result)
    query = "SELECT authorID FROM authors"
    authors  = execute_query(db_connection,query)
    print(authors)
    ids = authors.fetchall()
    for id in ids:
        print(id)
    author_id = request.args.get('id')
    print("author id: ",author_id)
    search_id = request.args.get('search_id')
    print("search id: ",search_id)
    if (author_id and search_id is not None):
        print("Run both!")
        query = "SELECT title FROM books WHERE bookID IN (SELECT bookID FROM authorBooks WHERE authorID = %s)" % author_id
        books = execute_query(db_connection,query)
        titles = books.fetchall()
        for t in titles:
            print(t)
        print("Selecting author with id ",search_id)
        query = "SELECT firstName, lastName FROM authors where authorID=%s" % search_id
        names = execute_query(db_connection,query)
        for n in names:
            print(n)
        state = {'id': author_id, 'search_id': search_id}
        return render_template('author.html',state=state,rows=result,authors_id=authors,
        titles=books,search=names)
    elif (author_id is not None):
        query = "SELECT title FROM books WHERE bookID IN (SELECT bookID FROM authorBooks WHERE authorID = %s)" % author_id
        books = execute_query(db_connection,query)
        titles = books.fetchall()
        for t in titles:
            print(t)
        state = {'id': author_id, 'search_id': search_id}
        return render_template('author.html', state=state,
        rows=result,authors_id=authors,titles=books)
    elif (search_id is not None):
        print("Selecting author with id ",search_id)
        query = "SELECT firstName, lastName FROM authors where authorID=%s" % search_id
        names = execute_query(db_connection,query)
        for n in names:
            print(n)
        state = {'id': author_id, 'search_id': search_id}
        return render_template('author.html', state=state,
        rows=result,authors_id=authors,search=names)
    # if (request.method == 'GET'):
    #     author_id = request.form.get("id",None)
    #     print(author_id)
    state = {'id': author_id, 'search_id': search_id}
    return render_template('author.html', state=state,
    rows=result,authors_id=authors)

@webapp.route('/book.html')
def book():
    print("Fetching book information table")
    db_connection = connect_to_database()
    query = "SELECT * FROM books"
    result = execute_query(db_connection,query)
    print(result)
    query = "SELECT bookID FROM books"
    books = execute_query(db_connection,query)
    print(books)
    ids = books.fetchall()
    for id in ids:
        print(id)
    book_id = request.args.get('book_id')
    print("book id: ",book_id)
    if (book_id is not None):
        print("Selecting author with id ",book_id)
        query = "SELECT title FROM books where bookID=%s" % book_id
        titles = execute_query(db_connection,query)
        for n in titles:
            print(n)

        return render_template('book.html',
        rows=result,book_id=books,search=titles)
    # state = {'id': author_id, 'search_id': search_id}
    return render_template('book.html',rows=result,book_id=books)

@webapp.route('/customer.html')
def customer():
    return render_template('customer.html')

@webapp.route('/order.html')
def order():
    return render_template('order.html')
