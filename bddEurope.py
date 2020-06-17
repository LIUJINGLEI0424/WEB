"""
Programme de création d'une base de données à partir de fichiers Json


Nous avons récupéré la base de donnée fournie ne contenant que le nom la position et la capitale du pays.
Nous avons donc créé une deuxième table contenant les informations sur le pays.
Dans le programme du serveur, il suffit de faire une jointure entre ces deux tables pour récupérer toutes les informations nécessaires.
"""

import sqlite3
import os
import json

conn = sqlite3.connect("Europe.sqlite")
c = conn.cursor()

sql = "DELETE FROM `datas`"
c.execute(sql)
conn.commit()

os.chdir("europe")

for paysJson in os.listdir():

	with open(paysJson,'r') as fichier:

		pays = json.loads(fichier.read())

		wp = pays["common_name"]	# RAS
		surface = pays["area_km2"]	# conv , en .
		try:
			pop = pays["population_estimate"]	# trouver le nombre et conv , en .
			
			j = -1
			iInit = 0
			for i in range(len(pop)):

				if pop[i] in ["0","1","2","3","4","5","6","7","8","9","."]:
					if j == -1:
						j = i
						iInit = i
					else:
						j += 1
			pop = int(pop[iInit:j].replace(",",""))

		except:
			pop = "undefined"


		monnaie = pays["currency"]	# []
		i = monnaie.find("[[")
		j = monnaie.find("]]")
		monnaie = monnaie[i+2:j]
		print(monnaie)

		try:
			pib = pays["GDP_nominal"]	# RAS
		except:
			pib = "undefined"

		drapeau = pays["image_flag"] # RAS
	
		surface = float(surface.replace(",",""))

		sql = 'INSERT INTO datas VALUES (?, ?, ?, ?, ?, ?)'

		c.execute(sql,(wp,surface,pop,monnaie,pib,drapeau))
		conn.commit()

		