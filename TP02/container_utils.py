import subprocess
import uuid
import random
import string
import os
import shlex

def generate_password(length=12):
    """
    Génère un mot de passe aléatoire avec des lettres, chiffres et caractères spéciaux.
    Assure qu'au moins un chiffre est présent à la fin.
    """
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length-1))
    password += random.choice(string.digits)  # Ajoute un chiffre à la fin
    return ''.join(random.sample(password, len(password)))  # Mélange le mot de passe

def run_container(image_name, use_volume=False, install_ssh=False):
    """
    Lance un conteneur Docker avec des options pour le volume et SSH.
    
    Args:
    - image_name: Nom de l'image Docker à utiliser
    - use_volume: Booléen pour attacher un volume persistant
    - install_ssh: Booléen pour installer et configurer SSH dans le conteneur
    
    Returns:
    - Tuple contenant le nom du conteneur, le port SSH (si applicable), et le mot de passe root (si applicable)
    """
    # Génération d'un nom unique pour le conteneur en utilisant le nom de l'image et un identifiant unique
    container_name = f"{image_name}-{uuid.uuid4().hex[:8]}"
    
    # Création d'un nom de volume si l'option use_volume est activée
    volume_name = f"{container_name}-volume" if use_volume else None
    
    # Sélection d'un port aléatoire pour SSH dans la plage des ports dynamiques/privés
    ssh_port = random.randint(49152, 65535)
    
    # Génération d'un mot de passe root si l'installation SSH est demandée
    root_password = generate_password() if install_ssh else None

    # Création du volume Docker si l'option use_volume est activée
    if use_volume:
        subprocess.run(["docker", "volume", "create", volume_name], check=True)

    # Préparation de la commande Docker pour lancer le conteneur
    cmd = ["docker", "run", "-d", "--name", container_name]

    # Ajout de l'option de volume si demandé
    if use_volume:
        cmd.extend(["-v", f"{volume_name}:/data"])

    # Configuration pour l'installation et le démarrage de SSH si demandé
    if install_ssh:
        cmd.extend(["-p", f"{ssh_port}:22"])
        cmd.append(image_name)
        # Script bash pour configurer SSH dans le conteneur
        
        cmd.extend(["/bin/bash", "-c", f"""
            apt-get update && 
            apt-get install -y openssh-server && 
            echo 'root:{root_password}' | chpasswd && 
            sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && 
            service ssh start && 
            tail -f /dev/null
        """])
    else:
        # Si SSH n'est pas demandé, on lance simplement l'image
        cmd.append(image_name)

    try:
        # Exécution de la commande Docker
        subprocess.run(cmd, check=True)
        
        # Affichage des informations sur le conteneur lancé
        print(f"Conteneur {image_name} lancé avec succès.")
        if use_volume:
            print(f"Volume persistent attaché : {volume_name}")
        if install_ssh:
            print("SSH installé et démarré dans le conteneur.")
            print(f"Pour vous connecter en SSH, utilisez la commande suivante :")
            print(f"ssh root@localhost -p {ssh_port}")
            print(f"Le mot de passe pour l'utilisateur root est : {root_password}")
            print("ATTENTION : Notez bien ce mot de passe, il ne sera plus affiché par la suite.")
    except subprocess.CalledProcessError as e:
        # Gestion des erreurs lors du lancement du conteneur
        print(f"Erreur lors du lancement du conteneur : {e}")

    # Retour des informations sur le conteneur lancé
    return container_name, ssh_port if install_ssh else None, root_password if install_ssh else None