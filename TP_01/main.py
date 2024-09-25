import os
import os_detector
import vm_creation
import pytest
import sys
import subprocess

# Fonction pour afficher les informations système
def afficher_info_systeme():
    print("Informations sur le système :")
    system_info = os_detector.obtenir_sys_info()
    for key, value in system_info.items():
        print(f"{key}: {value}")

    type_systeme = system_info['System Type']
    if type_systeme == 'Windows':
        hardware_info = os_detector.get_windows_hardware_info()
    elif type_systeme == 'Linux':
        hardware_info = os_detector.get_linux_hardware_info()
    else:
        print(f"Type de système non supporté pour les informations matérielles : {type_systeme}")
        return

    print("\nInformations matérielles :")
    for key, value in hardware_info.items():
        print(f"{key}: {value}")

# Fonction pour afficher les informations sur l'hyperviseur
def afficher_info_hyperviseur():
    print("\nInformations sur l'hyperviseur :")
    os_type = vm_creation.detect_os()
    hypervisor = vm_creation.detect_hypervisor()
    third_party_hypervisors = vm_creation.detect_third_party_hypervisors()

    print(f"Système d'exploitation détecté : {os_type}")
    print(f"Hyperviseur intégré : {hypervisor}")
    print(f"Hyperviseurs tiers détectés : {', '.join(third_party_hypervisors) if third_party_hypervisors else 'Aucun'}")

# Fonction pour créer une machine virtuelle
def creer_vm():
    print("\nCréation d'une machine virtuelle :")
    nom_vm = "TestVM"
    cpu = 2
    memoire = 2048
    memoire_video = 128
    
    # Définir le chemin de stockage dans le même dossier que le script main.py
    stockage = os.path.join(os.path.dirname(__file__), "storage.img")
    iso = os.path.join(os.path.dirname(__file__), "debian.iso")  # Chemin vers l'image ISO
    mode_reseau = "user"

    # Créer le fichier d'image si il n'existe pas
    if not os.path.exists(stockage):
        print(f"Création de l'image disque : {stockage}")
        subprocess.run(["qemu-img", "create", "-f", "qcow2", stockage, "10G"])  # Crée une image de 10 Go

    try:
        vm_creation.create_vm(nom_vm, cpu, memoire, memoire_video, stockage, iso, mode_reseau)
        print("Machine virtuelle créée avec succès !")
    except NotImplementedError as e:
        print(f"Erreur lors de la création de la VM : {e}")

# Fonction pour exécuter les tests
def run_tests():
    print("Exécution des tests...")
    test_result = pytest.main(["-v", "test_os_detector.py", "test_vm_creation.py"])
    if test_result == 0:
        print("Tous les tests ont réussi.")
        return True
    else:
        print("Certains tests ont échoué.")
        return False

# Fonction principale
def main():
    if run_tests():
        print("\nExécution du programme principal :")
        afficher_info_systeme()
        afficher_info_hyperviseur()
        creer_vm()
    else:
        print("Le programme s'arrête en raison d'échecs de tests.")
        sys.exit(1)

if __name__ == "__main__":
    main()