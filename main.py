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
        print(response.json())

        return redirect(url_for("home"))

    return render_template("add.html", form=form)

# movie = Movie(title=request.form["title"],
#               year=request.form["year"],
#               description=request.form["description"],
#               rating=request.form["rating"],
#               ranking=request.form["ranking"],
#               review=request.form["review"],
#               img_url=request.form["image_url"]
#               )


if __name__ == '__main__':
    app.run(debug=True)
