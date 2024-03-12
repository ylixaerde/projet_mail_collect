from flask import Flask, render_template, request, redirect, url_for
from flask import session
import csv

app = Flask(__name__)
app.secret_key = b'bafe004cc8de79cc96482b95db2d75473a3aa855b3270350267ccc92bddd46c5'

@app.route('/', methods=['GET'])
@app.route("/index", methods=['GET'])
def index():    
    with open("data.csv", "r", encoding="utf-8") as fichier_csv:
        data = list(csv.DictReader(fichier_csv, delimiter=";"))      
    return render_template('index.html', data=data)


@app.route("/encode_mail", methods=['GET', 'POST'])
def encode_mail():
    if request.method == 'GET':
        return render_template('encode_mail.html')

    elif request.method == 'POST':
        session['first_name'] = request.form['first_name']
        session['last_name'] = request.form['last_name']
        session['email'] = request.form['email']        
        new_id = None

        with open("data.csv", "r", encoding="utf-8", newline="") as fichier_csv:
            data = list(csv.DictReader(fichier_csv, delimiter=";"))
            new_id = int(data[-1]['id']) + 1  

        with open("data.csv", "a", encoding="utf-8", newline="") as fichier_csv:                      
            writer = csv.writer(fichier_csv, delimiter=';')            
            line = [new_id, session['first_name'], session['last_name'], session['email']]
            writer.writerow(line)
        
        return redirect('/submitted')

@app.route('/submitted')
def submitted():
    return render_template('submitted.html',
                           first_name=session['first_name'],
                           last_name=session['last_name'],
                           redirect=url_for('index'),
                           delay=5000,
                           )

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'GET':
        line = []
        with open("data.csv", "r", encoding="utf-8", newline="") as fichier_csv:
            data = list(csv.DictReader(fichier_csv, delimiter=";"))

            # Rechercher une ligne par son ID et modifier son contenu
            for line in data:
                if line['id'] == id:
                    prenom = line['prenom']
                    nom =  line['nom']
                    email = line['email']

        return render_template('edit_mail.html',
                                prenom = prenom,
                                nom = nom,
                                email = email
                                )
     
    elif request.method == 'POST':
        session['first_name'] = request.form['first_name']
        session['last_name'] = request.form['last_name']
        session['email'] = request.form['email']
        data = []

        with open("data.csv", "r", encoding="utf-8", newline="") as fichier_csv:
            data = list(csv.DictReader(fichier_csv, delimiter=";"))

        # Rechercher une ligne par son ID et modifier son contenu
        for line in data:
            if line['id'] == id:
                line['prenom'] = session['first_name']
                line['nom'] = session['last_name']
                line['email'] = session['email']

        # Réécrire le fichier CSV avec les modifications
        with open('data.csv', mode='w', newline='') as file:
            fieldnames = ['id', 'prenom', 'nom', 'email']
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()
            writer.writerows(data)
        
        return redirect('/submitted')
     

@app.route('/delete/<id>', methods=['GET'])
def delete(id):
    data = []

    with open("data.csv", "r", encoding="utf-8", newline="") as fichier_csv:
        data = list(csv.DictReader(fichier_csv, delimiter=";"))

    # Search for the dictionary that contains the line to be deleted
    for line in data:
        if line['id'] == id:
            # Remove the dictionary from the list
            data.remove(line)

    # Write the modified list of dictionaries to the CSV file
    with open('data.csv', mode='w', newline='') as file:
        fieldnames = ['id', 'prenom', 'nom', 'email']
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(data)

    return redirect('/')

if __name__ == '__main__':
	app.run(debug=True)
