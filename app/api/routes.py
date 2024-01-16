from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Books, books_schema, book_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'naw'}

# @api.route('/data')
# def viewdata():
#     data = get_contact()
#     response = jsonify(data)
#     print(response)
#     return render_template('index.html', data = data)

@api.route('/books', methods = ['POST'])
@token_required
def create_books(current_user_token):
    author_name = request.json['author_name']
    book_title = request.json['book_title']
    book_length = request.json['book_length']
    book_hardcover = request.json['book_hardcover']
    book_paperback = request.json['book_paperback']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    books = Books(author_name, book_title, book_length, book_hardcover, book_paperback, user_token=user_token)

    db.session.add(books)
    db.session.commit()

    response = book_schema.dump(books)
    return jsonify(response)

@api.route('/books', methods = ['GET'])
@token_required
def get_books(current_user_token):
    a_user = current_user_token.token
    books = Books.query.filter_by(user_token = a_user).all()
    response = books_schema.dump(books)
    return jsonify(response)

@api.route('/books/<id>', methods = ['GET'])
@token_required
def get_single_books(current_user_token, id):
    fan = current_user_token.token
    if fan == current_user_token.token:
        books = Books.query.get(id)
        response = book_schema.dump(books)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401

# UPDATE endpoint
@api.route('/books/<id>', methods = ['POST','PUT'])
@token_required
def update_books(current_user_token,id):
    books = Books.query.get(id) 
    books.author_name = request.json['author_name']
    books.book_title = request.json['book_title']
    books.book_length = request.json['book_length']
    books.book_hardcover = request.json['book_hardcover']
    books.book_paperback = request.json['book_paperback']
    contact.user_token = current_user_token.token

    db.session.commit()
    response = book_schema.dump(books)
    return jsonify(response)


# DELETE car ENDPOINT
@api.route('/books/<id>', methods = ['DELETE'])
@token_required
def delete_books(current_user_token, id):
    books = Books.query.get(id)
    db.session.delete(books)
    db.session.commit()
    response = books_schema.dump(books)
    return jsonify(response)