# Copyright 2022 <Votre nom et code permanent>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import random
from flask import request
from flask import Flask, url_for
from flask import redirect
from flask import render_template
from flask import g
from .database import Database
from .validators.Validator import ShouldBeBetween, ValidatorHandler
from .validators.Validator import ShouldNotContainsComma
from .validators.Validator import NumberShouldBeBetween
from .validators.Validator import ShouldBeEmail
from .validators.Validator import Required

app = Flask(__name__, static_url_path="", static_folder="static")


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


# Index page of animals
@app.route('/')
def index():
    # À remplacer par le contenu de votre choix.
    db = Database();
    animals = db.get_animaux()
    random.shuffle(animals)
    if (len(animals) > 5):
        while (len(animals) > 5):
            animals.pop()

    return render_template("index.html", animals=animals, nb_animals=len(animals))

@app.route('/animals/<int:id>')
def show(id):
    db = Database();
    animal = db.get_animal(id)
    return render_template("show.html", animal=animal)

@app.route('/animals/<int:id>/edit')
def edit(id):
    db = Database();
    return db.get_animal(id)

@app.route('/animals/create')
def create():
    return render_template('create.html')


@app.post('/animals/store')
def store():
    nom = request.form.get('nom')
    espece = request.form.get('espece')
    race = request.form.get('race')
    age = request.form.get('age')
    description = request.form.get('description')
    courriel = request.form.get('courriel')
    adresse = request.form.get('adresse')
    cp = request.form.get('cp')
    ville = request.form.get('ville')
    validatorHandler = ValidatorHandler()

    validatorHandler.add('nom', nom, [Required(), ShouldNotContainsComma(), ShouldBeBetween(4, 30), ShouldBeEmail()])
    validatorHandler.add('espece', espece, [Required(), ShouldNotContainsComma()])
    validatorHandler.add('race', race, [Required(), ShouldNotContainsComma()])
    validatorHandler.add('age', age, [Required(), ShouldNotContainsComma()])
    validatorHandler.add('description', description, [Required(), ShouldNotContainsComma()])
    validatorHandler.add('courriel', courriel, [Required(), ShouldNotContainsComma()])
    validatorHandler.add('adresse', adresse, [Required(), ShouldNotContainsComma()])
    validatorHandler.add('cp', cp, [Required(), ShouldNotContainsComma()])
    validatorHandler.add('ville', ville, [Required(), ShouldNotContainsComma()])

    errors = validatorHandler.validate()
    if (len(errors) != 0):
        return render_template('create.html', errors=errors, has_errors=True), 400

    data = {
        'nom': nom,
        'espece': espece,
        'race': race,
        'age': age,
        'description': description,
        'courriel': courriel,
        'adresse': adresse,
        'cp': cp,
        'ville': ville,
    }

    # Database().add_animal(data)
    # return {'sublime': 'ss'}
    return data
    return redirect(
        url_for('show', id=1)
    )
