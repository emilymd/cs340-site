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
    print("Fetching customer information table")
    db_connection = connect_to_database()
    query = "SELECT * FROM customers"
    result = execute_query(db_connection,query)
    print(result)
    query = "SELECT customerID FROM customers"
    customer = execute_query(db_connection,query)
    print(customer)
    ids = customer.fetchall()
    for id in ids:
        print(id)
    customer_id = request.args.get('customer_id')
    print("customer id: ",customer_id)
    if (customer_id is not None):
        print("Selecting customer with id ",customer_id)
        query = "SELECT phoneNumber FROM customers where customerID=%s" % customer_id
        customerInfo = execute_query(db_connection,query)
        for n in customerInfo:
            print(n)

        return render_template('customer.html',
        rows=result,customer_id=customer,customer=customerInfo)
    return render_template('customer.html',rows=result,customer_id=customer)

@webapp.route('/order.html')
def order():
    print("Fetching order information table")
    db_connection = connect_to_database()
    query = "SELECT * FROM orders"
    result = execute_query(db_connection,query)
    print(result)
    query = "SELECT orderID FROM orders"
    order = execute_query(db_connection,query)
    print(order)
    ids = order.fetchall()
    for id in ids:
        print(id)
    order_id = request.args.get('order_id')
    print("order id: ",order_id)
    if (order_id is not None):
        print("Selecting customer with id ",order_id)
        query = "SELECT customerID, orderDate FROM orders where orderID=%s" % order_id
        orderInfo = execute_query(db_connection,query)
        for n in orderInfo:
            print(n)

        return render_template('order.html',
        rows=result,order_id=order,order=orderInfo)
    return render_template('order.html',rows=result,order_id=order)
