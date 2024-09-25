import pytest
from unittest.mock import patch, Mock
import vm_creation
import subprocess

def test_detect_os(mocker):
    # Simule le retour de platform.system()
    mocker.patch('platform.system', return_value='Linux')
    os_type = vm_creation.detect_os()
    assert os_type in ["Windows", "Linux", "Darwin"]

def test_detect_hypervisor(mocker):
    # Simule le retour de platform.system() et l'existence de /dev/kvm
    mocker.patch('platform.system', return_value='Linux')
    mocker.patch('os.path.exists', return_value=True)  # Simule que /dev/kvm existe
    hypervisor = vm_creation.detect_hypervisor()
    assert hypervisor == "KVM"

def test_detect_third_party_hypervisors(mocker):
    # Simule les résultats de subprocess.call pour détecter les hyperviseurs tiers
    mocker.patch('subprocess.call', side_effect=[0, 1])  # Simule que VirtualBox est installé et VMware non
    hypervisors = vm_creation.detect_third_party_hypervisors()
    assert hypervisors == ["VirtualBox"]

def test_create_vm(mocker):
    # Simule les appels nécessaires pour créer une VM
    mocker.patch('vm_creation.detect_os', return_value='Linux')
    mocker.patch('vm_creation.detect_hypervisor', return_value='KVM')
    mocker.patch('subprocess.call', return_value=0)  # Simule un appel réussi à qemu-system-x86_64

    # Appel de la fonction create_vm
    result = vm_creation.create_vm("TestVM", 2, 2048, 128, "storage.img", "debian.iso", "user")
    
    # Vérifiez que la fonction subprocess.call a été appelée avec les bons arguments
    subprocess.call.assert_called_once_with(
        "qemu-system-x86_64 -name TestVM -m 2048 -smp 2 -vga std -display gtk,gl=on -hda storage.img -cdrom debian.iso -boot d -netdev user,id=net0 -device e1000,netdev=net0",
        shell=True
    )
    
    # Vérifiez que le résultat est None (ou ajustez selon votre fonction)
    assert result is None  # Si create_vm ne retourne rien, vérifiez que c'est None

def test_create_vm_permission_error(mocker):
    # Simulez la détection de l'OS et de l'hyperviseur
    mocker.patch('vm_creation.detect_os', return_value='Linux')
    mocker.patch('vm_creation.detect_hypervisor', return_value='KVM')

    # Simulez un appel à subprocess.call qui échoue
    mocker.patch('subprocess.call', side_effect=PermissionError("Accès refusé : privilèges élevés requis"))

    # Vérifiez que l'appel à create_vm lève une exception
    with pytest.raises(PermissionError, match="Accès refusé : privilèges élevés requis"):
        vm_creation.create_vm("TestVM", 2, 2048, 128, "storage.img", "debian.iso", "user")


