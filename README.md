# Book Rating With_flask
This practice will teach us how to use object oriented mapping to connect your sqlite3 database with our flask web application by using Flask Alchemy to practicing CRUD , Create, Read, Update, Delete , Data from our database.
![day-63-project](https://user-images.githubusercontent.com/57592040/160295073-a1bd343d-4e4c-4d36-ac3c-5f4049a0a141.gif)

## Step 1
As every starting steps we need to install flask alchemy by using pip 
```python
pip install -U Flask-SQLAlchemy
```
And we need to import the particular class from flask_sqlalchemy and it is SQLAlcemy.
then we need to add a configration to our flask app to locate our sqlite3 database by adding this line of code.
```python
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
```
And We use 3 slashes that mean it is a relative path and four slashes that mean absolute path.
We can also add another configration that will hide sqlAlchemy warning by this line of code. It's really not effecting your web application on any way.
```python
app.config['SQLALCHEMY_TRACK_MODIFICATIONS"] = False
```
Finally for this step we need to create an instance from SQLAlchemy class by adding our flask app as argument.
```python
db = SQLAlchemy(app)
```
## step 2
In this stage we are going to create our database table and we can do that by using `Model` class which can be used to declare models:
for this project we are going to create a Books table that includes four columns as below:
1. id and it will be an Integer promary key.
2. title and it will be a unique string .
3. author and it will be a string.
4. rating and it will be a float number.

```python
class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
    # To view the object data when print it.
        return f"Books(title : {self.title}, Author : {self.author}, Rating : {self.rating}/10 )"
           
```
After creating our Books Model we need to create our data base and start testing it before implementing it to our app and this will be on step 3.
## Step 3
Now our work will be on the python interactive console so you need to redirect to your project path or use a bulit-in pycharm console.
In the interactive console we need to import first our database instance by this line of code :
```python 
from main import db
```
If you did not get any error so you are on the right path else you need to check tour flask alchemy setup.
Then we need to create our Books database table by using this line of code:
```python
db.create_all()
```
And you will see your database file will be created and place on the selected path.
Now we can add data to our table by import the Model from our app script file and create an objects that referring to each row of data in our Books table.
I recommend you to do some experiment before implementing any code to your flask web app so you will be fully understanding of how you can deal with it later.
```python 
from main import Books
first_book = Books(title="Automate the Boring Stuff with python", author="Al Sweigart", rating=10.0)
```
So now you create first row on Books table and we did not add the id because it will be generated automatically. 
But this changes can't be added until you added and commit it as well by this line of code:
```python
db.session.add(first_book)
db.session.commit()
```
Now you added it successfully and to confirm that this row was added you can use query to display all row on the Books table by this line of code:
```python
db.session.query(Books).all()
```
Or you can search for specific book by any of its attributes by this line of code:
```python
book_id = 1
db.session.query(Books).filter_by(id=book_id).first()
# Just change the parameter inside the filter_by method to any attributes withen Books Model.
```
Lets say you want to update or edite any cell in your database here we need to locate the book first then update what we want, and to do so we can fellow the code bellow:
```python
book_to_edit = db.session.query(Books).filter_by(id=book_id).first()
book_to_edit.title = "Invent Your Own Computer Games with Python"
# So here we update the title from > Automate the Boring Stuff with python TO  Invent Your Own Computer Games with Python
db.session.commit()
# No need to use add method here because you already create the row and you just update it as well
```
Finally if we want to delete any row in our database we can do so by this line of code:
```python
book = db.session.query(Books).filter_by(id=book_id).first()
db.session.delete(book)
db.session.commit()
```
Before going to the Step 4 I want to add a useful tool and it is Sqlite3 Shell you can read and download it [HERE](https://www.sqlite.org/download.html).
## Step 4
First we need to display all books that we stored in our database to our home page and to do so we need to load all rows when our home page and we can do so by this line of code inside our home route function:
```python
@app.route('/')
def home():
    all_books = [book for book in db.session.query(Books).all()]
    # Here we load all rows and save it in our all_books array to pass it to our home page and unpack it.
    return render_template('index.html', all_books=all_books)
```
Then we Update our home page > index.html to loop throw all_books array and unpack the each book data as the Jinja code below:
```html
{% for book_data in all_books %}
    <ul>
        <li>Book Name : {{ book_data.title }}</li>
        <li>Book Author : {{ book_data.author }}</li>
        <li>Book Rating : {{ book_data.rating }}/10</li>
        <li>
            <a href="{{ url_for('edite_rating', book_id=book_data.id) }}"><button>Edite Rating</button></a>
            <a href="{{ url_for('delete_book', book_id=book_data.id) }}"><button>Delete</button></a>
        </li>
    </ul>
    <hr>
    {% else %}
    <p>Library is empty.</p>
    <hr>
    {% endfor %}
```
On this step we are done from display our Books table data next step will be about adding new book data to our database.
## Step 5
Ok We are doing well so far, now we need to add new book data to our database and to do so we need to create our form first and it will be like this:
```html
<form action="{{url_for('add')}}" method="post"><!--We will redirect data to our add route function with post -->
        <label>Book Name</label>
        <input type="text" name="Book Name">
        <label>Book Author</label>
        <input type="text" name="Book Author">
        <label>Rating</label>
        <input type="text" name="Rating">
        <button type="submit">Add Book</button>
</form>
```
then we will create our add route function like this:
```python
@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "POST": # When the user submit the form data by POST Request to send data to server.
    # here we wil create a book_data instance from Books Model then added and commit it as well
        book_data = Books(title=request.form.get('Book Name').title(),
                          author=request.form.get('Book Author').title(),
                          rating=request.form.get('Rating'))
        db.session.add(book_data)
        db.session.commit()
    # Finally we will redirect to our home page route
        return redirect(url_for('home'))
    
    # We will load the home page if the user did not submit the form.
    return render_template('add.html')
```
Until this step we did the job for adding new book to our database next step we will explain how to edite our book rating and deleting book as well
## Step 6
To edite our book rating lets start adding edite rating to our home page by adding edite rating link tage as button 
```html
<a href="{{ url_for('edite_rating', book_id=book_data.id) }}"><button>Edite Rating</button></a>
```
As you see the edite_rating route will take one parameter book_id th use it later to get that book from our database and edite thier rating. To do so we need to create our edite rating route function like below.
```python
@app.route("/edite_rating/<book_id>", methods=["GET", "POST"])
def edite_rating(book_id):
    if request.method == "GET": # When we Get the page from the server we will load the specified book data.
        book_selected = db.session.query(Books).filter_by(id=book_id).first()
        # And we will pass this book data when rendering our page.
        return render_template("edite_rating.html", book=book_selected)
    else:
    # If the user post the form data to the server here we edited the rating and commit it as well.
        change_rate = db.session.query(Books).filter_by(id=book_id).first()
        change_rate.rating = request.form.get("new rate")
        db.session.commit()
        # Finally we redirect the user to the home page
        return redirect(url_for('home'))
```
So Our edite_rating web page will look like this:
```html
<ul>
    <li><h1>Book : {{ book.title }} | Author : {{ book.author }} | Rating : {{ book.rating }}</h1></li>
    <li>
<form action="{{url_for('edite_rating', book_id=book.id)}}" method="post">
    <h2>Change Rating to : </h2>
    <input type="number" step="0.01" name="new rate">
    <button type="submit">Edite it</button>
</form>
    </li>
</ul>
```
So Now we finised from editing the book rating and the next will be how to delete the book from our database.
again we will add another link to our home page to delete the book like this :
```html
<a href="{{ url_for('delete_book', book_id=book_data.id) }}"><button>Delete</button></a>
```
