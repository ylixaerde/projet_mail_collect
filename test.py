error_list = []
error_column = {}
error_column["state"] = False
error_column["message"] = "Les colonnes du fichier ne correspondent pas aux colonnes attendues."
error_list.append(error_column)

# print (error_list])
for cle,valeur in error_list[0].items():
    print (cle.capitalize(), valeur)