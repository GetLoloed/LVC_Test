import subprocess

# Fonction pour vérifier si Docker est installé
def is_docker_installed():
    try:
        # Exécute la commande 'docker --version' pour vérifier l'installation
        subprocess.run(["docker", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True  # Docker est installé
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False  # Docker n'est pas installé ou la commande a échoué

# Fonction pour installer Docker avec Winget
def install_docker_with_winget():
    try:
        # Utilise Winget pour installer Docker Desktop
        subprocess.run(["winget", "install", "Docker.DockerDesktop"], check=True)
        print("Docker a été installé avec succès.")
    except subprocess.CalledProcessError as e:
        # Gère les erreurs spécifiques à l'installation
        print(f"Erreur lors de l'installation de Docker : {e}")
    except FileNotFoundError:
        # Gère le cas où Winget n'est pas trouvé
        print("Winget n'est pas installé ou n'est pas dans le PATH.")
    except Exception as e:
        # Gère toutes les autres erreurs inattendues
        print(f"Une erreur inattendue s'est produite : {e}")