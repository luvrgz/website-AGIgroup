from flask import Flask, url_for, request, render_template, redirect
import sqlite3 as lite
import Group

# ------------------
# application Flask
# ------------------

app = Flask(__name__)

list_group = [Group.client]
dict_group = dict()
for group in list_group:
	dict_group[group.name] = group

# ---------------------------------------
# les différentes pages (fonctions VUES)
# ---------------------------------------


@app.route('/')
def index():
	print(list(dict_group.keys()))
	return render_template('home.html', group_names=list(dict_group.keys()))


@app.route('/<group>')
def group_homepage(group_name=None):
	return dict_group[group_name]

@app.route('/afficher_personnes', methods=['GET'])
def afficher_personnes():
	
	con = lite.connect('exemples.db')
	con.row_factory = lite.Row
	cur = con.cursor()
	cur.execute("SELECT nom, prenom, role FROM personnes")
	lignes = cur.fetchall()
	con.close()
	return render_template('affichage_personnes.html', personnes = lignes)
	
@app.route('/ajouter_personne', methods=['GET', 'POST'])
def ajouter_personne():
	
	if not request.method == 'POST':
		return render_template('formulaire_personne.html', msg = "", nom = "", prenom = "", role = 0)
	else:
		nom = request.form.get('nom', '')
		prenom = request.form.get('prenom','')
		role = request.form.get('role', 0, type=int)
		
		if (nom != "" and prenom != "" and role > 0 and role < 4):
			con = lite.connect('exemples.db')
			con.row_factory = lite.Row
			cur = con.cursor()
			cur.execute("INSERT INTO personnes('nom', 'prenom', 'role') VALUES (?,?,?)", (nom,prenom,role))
			con.commit()
			con.close()
			return redirect(url_for('afficher_personnes'))
		else:
			return render_template('formulaire_personne.html', msg = "Mauvaise saisie !", nom = "", prenom = "", role = 0)


# ---------------------------------------
# pour lancer le serveur web local Flask
# ---------------------------------------

if __name__ == '__main__':
	app.run(debug=True, port=5678)
