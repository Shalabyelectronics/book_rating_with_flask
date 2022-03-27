from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.secret_key = "6f8c6cd39dabc7a5b32be6fdd8c8377d"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
"""We use 3 slashes that mean it is a relative path and four slashes that mean absolute path"""
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

'''
The books table should contain 4 fields: id, title, author and rating. The fields should have the
same limitations as before e.g. INTEGER/FLOAT/VARCHAR/UNIQUE/NOT NULL etc.
'''


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Books(title : {self.title}, Author : {self.author}," \
               f"Rating : {self.rating}/10 )"


@app.route('/')
def home():
    all_books = [book for book in db.session.query(Books).all()]
    return render_template('index.html', all_books=all_books)


@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        book_data = Books(title=request.form.get('Book Name').title(),
                          author=request.form.get('Book Author').title(),
                          rating=request.form.get('Rating'))
        db.session.add(book_data)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('add.html')


@app.route("/edite_rating/<book_id>", methods=["GET", "POST"])
def edite_rating(book_id):
    if request.method == "GET":
        book_selected = db.session.query(Books).filter_by(id=book_id).first()
        return render_template("edite_rating.html", book=book_selected)
    else:
        change_rate = db.session.query(Books).filter_by(id=book_id).first()
        change_rate.rating = request.form.get("new rate")
        db.session.commit()
        return redirect(url_for('home'))


@app.route("/delete/<book_id>")
def delete_book(book_id):
    book = db.session.query(Books).filter_by(id=book_id).first()
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
