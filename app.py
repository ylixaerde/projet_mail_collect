from flask import Flask, render_template, request, redirect, url_for
from flask import session
import logging
import csv
from email_validator import validate_email, EmailNotValidError

app = Flask(__name__)
logger = logging.getLogger(__name__)
app.secret_key = b'bafe004cc8de79cc96482b95db2d75473a3aa855b3270350267ccc92bddd46c5'

# verifie la validité de l'email
def verif_email(email):
	try:
	# validate and get info
		v = validate_email(email)
		# replace with normalized form
		print("True")
	except EmailNotValidError as e:
		# email is not valid, exception message is human-readable
		print(str(e))

@app.route('/', methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
    result = []
    with open("data.csv", "r", encoding="utf-8") as fichier_csv:
        data = csv.reader(fichier_csv, delimiter=';')
        keys = ['prenom', 'nom', 'email']        
        for row in data:
            d = {}
            for i in range(len(keys)):
                d[keys[i]] = row[i]
            result.append(d)       
    return render_template('index.html', list_mail=result)
    
@app.route("/encode_mail", methods=['GET', 'POST'])
def encode_mail():
    if request.method == 'GET':
        return render_template('encode_mail.html')

    elif request.method == 'POST':
        session['first_name'] = request.form['first_name']
        session['last_name'] = request.form['last_name']
        session['email'] = request.form['email']

        # Do something with the form data (e.g. store it in a database)
        line = [session['first_name'], session['last_name'], session['email']]

        with open("data.csv", "a", encoding="utf-8", newline="") as fichier_csv:
            writer = csv.writer(fichier_csv, delimiter=';')
            writer.writerow(line)
        
        return redirect('/submitted')

    else:
        return "Method Not Allowed"

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
