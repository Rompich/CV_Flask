from flask import Flask, render_template, request, redirect, jsonify, json
import sqlite3
from urllib.request import urlopen
from dotenv import load_dotenv
import os
def get_db_connection():
    conn = sqlite3.connect('database.db')
    return conn
   
app = Flask(__name__) #creating flask app name

load_dotenv()

TOKEN = os.getenv('ALWAYSDATA_TOKEN')

if TOKEN is None:
    raise ValueError("Le token n'est pas défini dans les variables d'environnement !")

@app.route('/')
def home():
    return render_template("resume_1.html")

@app.route('/resume_1')
def resume_1():
    return render_template("resume_1.html")

@app.route('/resume_2')
def resume_2():
    return render_template("resume_2.html")

@app.route('/resume_template')
def resume_template():
    return render_template("resume_template.html")
    
@app.route('/messages')
def message():
    return render_template("message.html")
    
# Création d'une nouvelle route pour la lecture de la BDD
@app.route("/consultation/")
def ReadBDD():
    conn = get_db_connection()  # Utilisation de la fonction définie pour la connexion
    cursor = conn.cursor()
    cursor.execute('SELECT email, message FROM client;')
    data = cursor.fetchall()
    conn.close()
    # Rendre le template HTML et transmettre les données
    return render_template('read_data.html', data=data)
    
@app.route('/choix/<int:post_id>')
def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM client WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    
@app.route('/messages', methods=['GET','POST'])
def ajouter_message():
    if request.method == 'POST':
        
        submitted_token = request.form['token']
        # Vérification du token
        if submitted_token != TOKEN:
            return "Token incorrect. Accès non autorisé."

        email = request.form['email']
        message = request.form['message']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO client (email, message, token) VALUES (?, ?, ?)', (email, message, token))
        conn.commit()
        
        return redirect('/consultation')
        
    return render_template('message.html')

 
if(__name__ == "__main__"):
    app.run()
