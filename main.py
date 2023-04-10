from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap4
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired, URL
import requests
import os

# Initialise Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap4(app)

# Configure database with SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie-database.db'
db = SQLAlchemy(app)


class MovieForm(FlaskForm):
    title = StringField("Movie title", validators=[DataRequired()])
    submit = SubmitField("Submit")


class EditForm(FlaskForm):
    rating = FloatField("Rating", validators=[DataRequired()])
    # ranking = IntegerField("Ranking", validators=[DataRequired()])
    review = StringField("Review", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Define models
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Integer, unique=True, nullable=False)
    year = db.Column(db.Integer, unique=False, nullable=False)
    description = db.Column(db.String(250), unique=False, nullable=False)
    rating = db.Column(db.Float, unique=False, nullable=False)
    ranking = db.Column(db.Integer, unique=False, nullable=False)
    review = db.Column(db.String(250), unique=False, nullable=False)
    img_url = db.Column(db.String(250), unique=False, nullable=False)

    def __repr__(self):
        return f'<Movie {self.title}>'


# Create database
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    movies = db.session.query(Movie).all()
    return render_template("index.html", movies=movies)


@app.route("/edit", methods=["GET", "POST"])
def edit():
    id_number = request.args.get("id")
    form = EditForm()
    if form.validate_on_submit():
        movie_to_update = Movie.query.get(id_number)
        movie_to_update.rating = request.form["rating"]
        # movie_to_update.ranking = request.form["ranking"]
        movie_to_update.review = request.form["review"]
        db.session.commit()

        return redirect(url_for("home"))

    movie_to_edit = Movie.query.filter_by(id=id_number).first()
    return render_template("edit.html", movie=movie_to_edit, form=form)


@app.route("/delete")
def delete():
    id_number = request.args.get("id")
    movie_to_delete = Movie.query.get(id_number)
    db.session.delete(movie_to_delete)
    db.session.commit()

    return redirect(url_for("home"))


@app.route("/add", methods=["GET", "POST"])
def add():
    form = MovieForm()

    if form.validate_on_submit():
        search_title = request.form["title"].lower()

        api_key = os.environ["API_KEY"]
        bearer_token = os.environ["BEARER_TOKEN"]
        tmdb_endpoint = "https://api.themoviedb.org/3/search/movie"

        query = {
            "api_key": api_key,
            "query": search_title,
        }

        headers = {
            'Authorization': f'Bearer {bearer_token}',
            'Content-Type': 'application/json;charset=utf-8',
        }

        response = requests.get(tmdb_endpoint, params=query, headers=headers)
        response.raise_for_status()

        movie_data = response.json()["results"]

        # Present user with list of potential matching movies.
        return render_template("select.html", movies=movie_data)

    return render_template("add.html", form=form)


@app.route("/select", methods=["GET", "POST"])
def select():
    # Get movie title
    title = request.args.get("title")

    # Get release year
    release_date = request.args.get("release_date")
    year = release_date[:4]

    # Get movie description
    description = request.args.get("description")

    # Get movie poster
    base_url = "https://image.tmdb.org/t/p/"
    file_size = "original"
    poster_path = request.args.get("img_url")

    img_url = base_url + file_size + poster_path

    # Add the data to the database
    movie_to_add = Movie(title=title,
                         year=year,
                         description=description,
                         rating=0,
                         ranking=0,
                         review="",
                         img_url=img_url)

    db.session.add(movie_to_add)
    db.session.commit()

    last_added_movie = Movie.query.filter_by(title=title).first()
    id_number = last_added_movie.id

    # After adding new movie to database, redirect to edit page for the newly added movie.
    # This will allow the user to fill the currently empty rating and review fields.

    return redirect(url_for("edit", id=id_number))



if __name__ == '__main__':
    app.run(debug=True)
