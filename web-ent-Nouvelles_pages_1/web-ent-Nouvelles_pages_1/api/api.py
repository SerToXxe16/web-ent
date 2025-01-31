import flask
from flask import request, jsonify, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'your_secret_key'

# Définir le chemin de la base de données dans le dossier api/
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'bdd.db')
db = SQLAlchemy(app)

# Définition des modèles de base de données
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    note = db.Column(db.Float, nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    contenu = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

# Créer la base de données
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])
def home():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email, password=password).first()
    
    if user:
        session['user_id'] = user.id
        return redirect(url_for('main'))
    
    return redirect(url_for('home'))

@app.route('/main', methods=['GET'])
def main():
    if 'user_id' in session:
        return render_template("main.html")
    return redirect(url_for('home'))

# Partie admin pour créer des utilisateurs
@app.route('/admin/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        nom = request.form['nom']
        email = request.form['email']
        password = request.form['password']
        
        new_user = User(nom=nom, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('home'))  # Redirige vers la page de connexion après la création
    
    return render_template("create_user.html")

if __name__ == '__main__':
    app.run()