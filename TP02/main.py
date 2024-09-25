import subprocess
import sys
import pytest
from docker_utils import is_docker_installed, install_docker_with_winget
from container_utils import run_container

def afficher_menu():
    # Affiche les options du menu pour l'utilisateur
    print("\nChoisissez un conteneur à télécharger et exécuter :")
    print("1. Conteneur Python")
    print("2. Conteneur MariaDB")
    print("3. Conteneur Debian (avec SSH)")
    print("4. Conteneur Ubuntu (avec SSH)")
    print("5. Quitter")

def main():
    # Vérifie si Docker est installé, propose l'installation si nécessaire
    if not is_docker_installed():
        reponse = input("Docker n'est pas installé. Voulez-vous l'installer avec Winget ? (o/n) : ")
        if reponse.lower() == 'o':
            install_docker_with_winget()
        else:
            print("Installation de Docker annulée.")
            return

    while True:
        # Boucle principale du programme
        afficher_menu()
        choix = input("Entrez votre choix (1-5) : ")

        if choix == '5':
            print("Au revoir !")
            break

        if choix not in ['1', '2', '3', '4']:
            print("Choix invalide. Veuillez réessayer.")
            continue

        # Demande à l'utilisateur s'il souhaite un volume persistent
        volume_persistent = input("Voulez-vous attacher un volume de stockage persistent ? (o/n) : ").lower() == 'o'

        # Exécute le conteneur choisi avec les options appropriées
        if choix in ['1', '2']:
            run_container("python" if choix == '1' else "mariadb", volume_persistent)
        else:
            run_container("debian" if choix == '3' else "ubuntu", volume_persistent, install_ssh=True)

if __name__ == "__main__":
    # Exécuter les tests avant de lancer le programme
    test_result = pytest.main(["-v", "tests"])
    
    # Lancer le programme principal seulement si tous les tests passent
    if test_result == 0:  # 0 indique que tous les tests ont réussi
        main()
    else:
        print("Les tests ont échoué. Veuillez corriger les erreurs avant d'exécuter le programme.")