from flask import Flask, render_template, redirect, request, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import PetForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adoption_list'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ohsoohsosecretkey'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_ECHO'] = True

with app.app_context():
    connect_db(app)
    db.create_all()

@app.route('/')
def homepage():
    pets = Pet.query.order_by(Pet.id).all()
    return render_template('base.html',
                           pets=pets)

@app.route('/add', methods=["GET", "POST"])
def add_pet():
    form = PetForm()
    if form.validate_on_submit():
        name = form.pet_name.data
        species = form.species.data
        photo = form.photo_url.data
        age = form.age.data
        notes = form.notes.data
        with app.app_context():
            maxie = Pet(name=name, species=species, photo_url=photo, age=age, notes=notes)
            db.session.add(maxie)
            db.session.commit()
        return redirect(url_for('homepage'))
    return render_template('index.html',
                           form=form)

@app.route('/pet/<int:pet_id>')
def pet_profile(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    return render_template('petpage.html', 
                           pet=pet)

@app.route('/pet/<int:pet_id>/edit', methods=["GET", "POST"])
def edit_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    form = PetForm(obj=pet)
    if form.validate_on_submit():
        form.populate_obj(pet)
        db.session.commit()
        return redirect(url_for('pet_profile',
                                pet_id=pet.id))
    return render_template('editpet.html', 
                           pet=pet,
                           form=form)

if __name__ == "__main__":
    app.run(debug=True)