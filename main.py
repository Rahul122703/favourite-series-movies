
from flask import Flask,render_template,request,redirect,url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import mapped_column,Mapped,DeclarativeBase
from sqlalchemy import Float,Integer,String
from flask_wtf import FlaskForm
from wtforms import StringField,FloatField,SubmitField,URLField
from wtforms.validators import DataRequired, URL

class MyForm(FlaskForm):
    rating = FloatField(label="Your Rating out of 10".title(), validators=[DataRequired()],render_kw={"style": "width: 300px;"})
    review = StringField(label = "your review".title(), validators=[DataRequired()],render_kw={"style": "width: 300px;"})
    doneButton = SubmitField(label = "Done")
    
class AddMovie(FlaskForm):
    title = StringField(label="Movie name", validators=[DataRequired()],render_kw={"style": "width: 300px;"})
    year = StringField(label="Enter year", validators=[DataRequired()],render_kw={"style": "width: 300px;"})
    description = StringField(label="Description", validators=[DataRequired()],render_kw={"style": "width: 600px;"})
    rating = FloatField(label="Rating", validators=[DataRequired()],render_kw={"style": "width: 300px;"})
    review = StringField(label="Review", validators=[DataRequired()],render_kw={"style": "width: 300px;"})
    img_url = URLField(label="Movie poster pic url", validators=[DataRequired(),URL(message="Pease enter a valid URL")],render_kw={"style": "width: 300px;"})
    add_button = SubmitField(label = "Add Movie")

app = Flask(__name__)
app.secret_key = "rahulsharma"
app.config['SQLALCHEMY_DATABASE_URI'] = r"sqlite:///G:\My Drive\WORK\MINE\Python\100 days python bootcamp\Day 64\instance\movies.db"
bootstrap = Bootstrap5(app)


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

with app.app_context():
    db.create_all()

class Movie(db.Model):
    id : Mapped[int]  = mapped_column(Integer, primary_key = True) 
    title : Mapped[str]  = mapped_column(String(50), unique = True, nullable = False)
    year : Mapped[int]  = mapped_column(Integer, nullable = False)
    description : Mapped[str]  = mapped_column(String(500), nullable = False)
    rating : Mapped[float]  = mapped_column(Float, nullable = True) 
    review: Mapped[str]  = mapped_column(String(500), nullable=True)
    img_url: Mapped[str]  = mapped_column(String(500), nullable=False)
    
@app.route('/')
def home():
    result = db.session.execute(db.select(Movie).order_by(Movie.rating))
    all_movies = result.scalars().all() 
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()
    return render_template("index.html", movies=all_movies)

@app.route('/edit/<string:movieTitle>', methods=['POST','GET'])
def edit_info(movieTitle): ###EDIT INFORMATION
    form_instance = MyForm()
    if form_instance.validate_on_submit():
        movie_data = db.session.execute(db.select(Movie).where(Movie.title == movieTitle)).scalar()
        movie_data.rating = form_instance.rating.data
        movie_data.review = form_instance.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', new_movie_form = form_instance, movie_title = movieTitle)

@app.route('/delete/<string:movieTitle>')
def delete_movie(movieTitle): ######DELETE
    del_movie = db.session.execute(db.select(Movie).where(Movie.title == movieTitle)).scalar()
    db.session.delete(del_movie)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/add',methods=['POST','GET'])
def add_movie():
    movie_form = AddMovie()
    if movie_form.validate_on_submit():
        new_movie = Movie(
        title = movie_form.title.data,
        year = int(movie_form.year.data),
        description = movie_form.description.data,
        rating = float(movie_form.rating.data),
        review = movie_form.review.data,
        img_url = movie_form.img_url.data)
        db.session.add(new_movie)
        db.session.commit()
        print("this part is running")
        return redirect(url_for('home'))
    return render_template('add.html', movie_form = movie_form)

if __name__ == "__main__":
    app.run(debug=True)

