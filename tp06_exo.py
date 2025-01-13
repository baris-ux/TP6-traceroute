import argparse
import subprocess
import re
import platform

def traceroute(cible, progressif, fichier_sortie):

    est_windows = platform.system().lower() == "windows"
    commande = ["tracert", cible] if est_windows else ["traceroute", cible]
    resultats = []

    regex_ip = r"\b(?:\d{1,3}\.){3}\d{1,3}\b|[a-fA-F0-9:]+:+[a-fA-F0-9]+"

    try:
        if progressif:
            processus = subprocess.Popen(commande, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            fichier = open(fichier_sortie, "w") if fichier_sortie else None
            for ligne in iter(processus.stdout.readline, ""):
                correspondance_ip = re.search(regex_ip, ligne)
                if correspondance_ip:
                    adresse_ip = correspondance_ip.group()
                    print(adresse_ip)
                    resultats.append(adresse_ip)
                    if fichier:
                        fichier.write(adresse_ip + "\n")
            processus.wait()
            if fichier:
                fichier.close()
        else:
            processus = subprocess.run(commande, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if processus.returncode != 0:
                print("Erreur lors de l'exécution de tracert/traceroute :", processus.stderr)
                return
            for ligne in processus.stdout.splitlines():
                correspondance_ip = re.search(regex_ip, ligne)
                if correspondance_ip:
                    resultats.append(correspondance_ip.group())

            for ip in resultats:
                print(ip)

            if fichier_sortie:
                with open(fichier_sortie, "w") as fichier:
                    fichier.write("\n".join(resultats))
    except Exception as e:
        print("Erreur : ", str(e))

def principal():
    parseur = argparse.ArgumentParser(description="Script traceroute avec options d'affichage progressif et enregistrement.")
    parseur.add_argument("cible", help="URL ou adresse IP cible pour le traceroute.")
    parseur.add_argument("-p", "--progressif", action="store_true", help="Affiche les résultats au fur et à mesure.")
    parseur.add_argument("-o", "--fichier-sortie", help="Nom du fichier pour enregistrer les résultats.")

    arguments = parseur.parse_args()

    traceroute(arguments.cible, arguments.progressif, arguments.fichier_sortie)

if __name__ == "__main__":
    principal()
