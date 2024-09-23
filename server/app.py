
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from collections import OrderedDict

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'data.sqlite') 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Book(db.Model):
    __tablename__ = 'books'
    id:int = db.Column(db.Integer, primary_key=True)
    title:str = db.Column(db.String(100), unique=True)
    author:str = db.Column(db.String(30), unique=True)
    read:bool =db.Column(db.Boolean)


def to_dict(books):
    return OrderedDict(
        id=books.id,
        title=books.title,
        author=books.author,
        read=books.read
    )


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Book=Book)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


def remove_book(book_id):
    Book.query.filter_by(id=book_id).delete()
    db.session.commit()


@app.route('/books', methods=['GET','POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        data = request.get_json()
        book=Book(
            title=data.get('title'),
            author=data.get('author'),
            read=data.get('read')
        )
        db.session.add(book)
        db.session.commit()
    books=Book.query.all()
    response_object['books'] = list(map(to_dict, books))

    return jsonify(response_object)


@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        data = request.get_json()
        remove_book(book_id)
        book=Book(
            title=data.get('title'),
            author=data.get('author'),
            read=data.get('read')
        )
        db.session.add(book)
        db.session.commit()
        response_object['message'] = 'Book updated!'
    if request.method == 'DELETE':
        remove_book(book_id)
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()