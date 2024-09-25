import platform
import subprocess
import os

# Fonction pour détecter le système d'exploitation
def detect_os():
    return platform.system()

# Fonction pour détecter l'hyperviseur intégré
def detect_hypervisor():
    os_type = detect_os()
    if os_type == "Linux":
        # Vérifie si KVM est disponible sur Linux
        return "KVM" if os.path.exists("/dev/kvm") else None
    elif os_type == "Windows":
        # Vérifie si Hyper-V est disponible sur Windows
        return "Hyper-V" if subprocess.call("powershell Get-WindowsFeature -Name Hyper-V", shell=True) == 0 else None
    elif os_type == "Darwin":
        # Retourne HVF pour macOS
        return "HVF"
    return None

# Fonction pour détecter les hyperviseurs tiers
def detect_third_party_hypervisors():
    hypervisors = []
    # Vérifie si VirtualBox est installé
    if subprocess.call("vboxmanage --version", shell=True) == 0:
        hypervisors.append("VirtualBox")
    # Vérifie si VMware est installé
    if subprocess.call("vmware -v", shell=True) == 0:
        hypervisors.append("VMware")
    return hypervisors

# Fonction pour créer une machine virtuelle
def create_vm(name, cpu, memory, video_memory, storage, iso, network_mode):
    os_type = detect_os()
    if os_type in ["Linux", "Darwin"]:
        # Commande pour créer une VM avec QEMU/KVM
        # qemu-system-x86_64 : Lance l'émulateur QEMU pour l'architecture x86_64
        # -name {name} : Définit le nom de la machine virtuelle
        # -m {memory} : Alloue la quantité de mémoire vive (RAM) à la VM
        # -smp {cpu} : Spécifie le nombre de processeurs virtuels
        # -vga std : Utilise un adaptateur graphique standard
        # -display gtk,gl=on : Utilise GTK pour l'affichage avec l'accélération graphique activée
        # -hda {storage} : Spécifie le fichier d'image disque dur
        # -cdrom {iso} : Spécifie le fichier d'image ISO pour le lecteur CD-ROM
        # -boot d : Démarre la VM à partir du CD-ROM
        # -netdev user,id=net0 : Configure le mode réseau utilisateur
        # -device e1000,netdev=net0 : Ajoute une carte réseau e1000 connectée au netdev user
        subprocess.call(f"qemu-system-x86_64 -name {name} -m {memory} -smp {cpu} -vga std -display gtk,gl=on -hda {storage} -cdrom {iso} -boot d -netdev user,id=net0 -device e1000,netdev=net0", shell=True)
    else:
        # Lève une exception si la création de VM n'est pas supportée sur la plateforme
        raise NotImplementedError("La création de VM avec QEMU/KVM n'est pas supportée sur cette plateforme.")

# Fonction principale
def main():
    os_type = detect_os() # Détecte le système d'exploitation
    hypervisor = detect_hypervisor() # Détecte l'hyperviseur intégré
    third_party_hypervisors = detect_third_party_hypervisors() # Détecte les hyperviseurs tiers

    # Affiche les informations détectées
    print(f"OS détecté: {os_type}")
    print(f"Hyperviseur intégré: {hypervisor}")
    print(f"Hyperviseurs tiers détectés: {third_party_hypervisors}")

    # Crée une machine virtuelle de test
    create_vm("TestVM", 2, 2048, 128, "storage.img", "iso.img", "user")

# Tests unitaires
def test_detect_os():
    assert detect_os() in ["Windows", "Linux", "Darwin"]

def test_detect_hypervisor():
    hypervisor = detect_hypervisor()
    os_type = detect_os()
    if os_type == "Linux":
        assert hypervisor == "KVM" or hypervisor is None
    elif os_type == "Windows":
        assert hypervisor == "Hyper-V" or hypervisor is None
    elif os_type == "Darwin":
        assert hypervisor == "HVF"

def test_detect_third_party_hypervisors():
    hypervisors = detect_third_party_hypervisors()
    assert isinstance(hypervisors, list)

if __name__ == "__main__":
    main()