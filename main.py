from flask import Flask, url_for, request, render_template, redirect
import sqlite3 as lite
import Group

# ------------------
# application Flask
# ------------------

app = Flask(__name__)

list_group = [Group.client]
dict_group = dict()
for tmp_group in list_group:
	dict_group[tmp_group.name] = tmp_group

print(dict_group)
# ---------------------------------------
# les différentes pages (fonctions VUES)
# ---------------------------------------


@app.route('/')
def index():
	list_group_names = list(dict_group.keys())
	return render_template('home.html', group_names=list_group_names)


@app.route('/homepage')
def group_homepage():
	group_name = request.args.get('group')
	group = dict_group[group_name]
	return render_template('group_homepage.html', group=group.name)


@app.route('/afficher_commandes', methods=['GET'])
def afficher_commandes():
	group_name = request.args.get('group')

	con = lite.connect('exemples.db')
	con.row_factory = lite.Row
	cur = con.cursor()
	cur.execute("SELECT * FROM personnes")
	lignes = cur.fetchall()
	con.close()
	return render_template('afficher_commandes.html', commandes_values=lignes, commande_keys=lignes[0].keys(), group=group_name)


@app.route('/passer_commande', methods=['GET', 'POST'])
def passer_commande():
	group_name = request.args.get('group')

	con = lite.connect('exemples.db')
	con.row_factory = lite.Row
	cur = con.cursor()
	cur.execute("SELECT * FROM personnes")
	lignes = cur.fetchall()
	con.close()

	if not request.method == 'POST':
		return render_template('passer_commande.html', commandes_values=lignes, commande_keys=lignes[0].keys(), group=group_name)
	else:
		nom = request.form.get('nom', '')
		prenom = request.form.get('prenom', '')
		role = request.form.get('role', 0, type=int)

		con = lite.connect('exemples.db')
		con.row_factory = lite.Row
		cur = con.cursor()
		cur.execute("INSERT INTO personnes('nom', 'prenom', 'role') VALUES (?,?,?)", (nom,prenom,role))
		con.commit()
		con.close()
		return redirect(url_for('succes', msg="Okay commande bien passée"))


@app.route('/succes')
def succes():
	group_name = request.args.get('group')
	return render_template('succes.html', msg="", group=group_name)

# ---------------------------------------
# pour lancer le serveur web local Flask
# ---------------------------------------

if __name__ == '__main__':
	app.run(debug=True, port=5678)
