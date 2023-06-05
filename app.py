from flask import Flask, render_template, request, redirect, url_for
from flask import session
import csv

app = Flask(__name__)
app.secret_key = b'bafe004cc8de79cc96482b95db2d75473a3aa855b3270350267ccc92bddd46c5'

@app.route('/', methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
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
            new_id = len(data) + 1  

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

@app.route('/edit')
def edit():
     return render_template('edit.html,')

@app.route('/delete')
def delete():
     return render_template('delete.html,')

if __name__ == '__main__':
	app.run(debug=True)
