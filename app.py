from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Konfigurasi MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.lpk_database
registrants_collection = db.registrants

@app.route('/')
def home():
    programs = [
        {"name": "Web Developer", "image": "https://picsum.photos/200", "description": "Pelatihan untuk menjadi web developer profesional."},
        {"name": "Data Scientist", "image": "https://picsum.photos/200", "description": "Pelatihan untuk menjadi data scientist profesional."},
        {"name": "Android Developer", "image": "https://picsum.photos/200", "description": "Pelatihan untuk menjadi android developer profesional."},
        {"name": "Video Editor", "image": "https://picsum.photos/200", "description": "Pelatihan untuk menjadi video editor profesional."},
        {"name": "Animator", "image": "https://picsum.photos/200", "description": "Pelatihan untuk menjadi animator profesional."},
        {"name": "Content Creator", "image": "https://picsum.photos/200", "description": "Pelatihan untuk menjadi content creator profesional."},
        {"name": "Enterprise Resource Planning", "image": "https://picsum.photos/200", "description": "Pelatihan untuk menjadi enterprise resource planning profesional."},
        {"name": "Desainer Grafis", "image": "https://picsum.photos/200", "description": "Pelatihan untuk menjadi desainer grafis profesional."},
        {"name": "Teknisi Jaringan", "image": "https://picsum.photos/200", "description": "Pelatihan untuk menjadi teknisi jaringan profesional."}
    ]
    return render_template('home.html', programs=programs)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        nik = request.form['nik']
        whatsapp = request.form['whatsapp']
        email = request.form['email']
        program = request.form['program']
        registrant = {
            'name': name,
            'nik': nik,
            'whatsapp': whatsapp,
            'email': email,
            'program': program
        }
        registrants_collection.insert_one(registrant)
        return redirect(url_for('registrants'))
    
    programs = ["Web Developer", "Data Scientist", "Android Developer", "Video Editor", "Animator",
                "Content Creator", "Enterprise Resource Planning", "Desainer Grafis", "Teknisi Jaringan"]
    return render_template('register.html', programs=programs)

@app.route('/registrants')
def registrants():
    registrants = registrants_collection.find()
    return render_template('registrants.html', registrants=registrants)

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    registrant = registrants_collection.find_one({'_id': ObjectId(id)})
    if request.method == 'POST':
        name = request.form['name']
        nik = request.form['nik']
        whatsapp = request.form['whatsapp']
        email = request.form['email']
        program = request.form['program']
        registrants_collection.update_one(
            {'_id': ObjectId(id)},
            {'$set': {
                'name': name,
                'nik': nik,
                'whatsapp': whatsapp,
                'email': email,
                'program': program
            }}
        )
        return redirect(url_for('registrants'))
    
    programs = ["Web Developer", "Data Scientist", "Android Developer", "Video Editor", "Animator",
                "Content Creator", "Enterprise Resource Planning", "Desainer Grafis", "Teknisi Jaringan"]
    return render_template('edit.html', registrant=registrant, programs=programs)

@app.route('/delete/<id>')
def delete(id):
    registrants_collection.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('registrants'))

if __name__ == '__main__':
    app.run(debug=True)
