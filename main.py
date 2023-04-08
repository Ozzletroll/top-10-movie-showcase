from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap4
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests


# Initialise Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap4(app)

# Configure database with SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie-database.db'
db = SQLAlchemy(app)


# Define models
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Integer, unique=True, nullable=False)
    year = db.Column(db.Integer, unique=False, nullable=False)
    description = db.Column(db.String(250), unique=False, nullable=False)
    rating = db.Column(db.Integer, unique=False, nullable=False)
    ranking = db.Column(db.Integer, unique=False, nullable=False)
    review = db.Column(db.String(250), unique=False, nullable=False)
    img_url = db.Column(db.String(250), unique=False, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'


# Create database
with app.app_context():
    db.create_all()

    # Add example movie
    # example_movie = Movie(title="Lawrence of Arabia",
    #                       year="1962",
    #                       description="The story of T.E. Lawrence, the English officer who successfully united and "
    #                                   "led the diverse, often warring, Arab tribes during World War I in order to "
    #                                   "fight the Turks.",
    #                       rating="9",
    #                       ranking="10",
    #                       review="Vast, awe-inspiring, beautiful with ever-changing hues, exhausting and barren "
    #                              "of humanity.",
    #                       img_url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Lawrence_of_arabia_ver3_xxlg."
    #                               "jpg/800px-Lawrence_of_arabia_ver3_xxlg.jpg")
    #
    # db.session.add(example_movie)
    # db.session.commit()


@app.route("/")
def home():
    movies = db.session.query(Movie).all()
    return render_template("index.html", movies=movies)


if __name__ == '__main__':
    app.run(debug=True)
