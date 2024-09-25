import pytest
import subprocess
from docker_utils import is_docker_installed, install_docker_with_winget

def test_is_docker_installed(mocker):
    # Simuler le comportement de subprocess.run
    mock_subprocess = mocker.patch('docker_utils.subprocess.run')
    
    # Test lorsque Docker est installé
    # On simule un code de retour 0, ce qui indique un succès
    mock_subprocess.return_value.returncode = 0
    assert is_docker_installed() == True
    
    # Test lorsque Docker n'est pas installé
    # On simule une erreur FileNotFoundError, ce qui se produit quand la commande docker n'est pas trouvée
    mock_subprocess.side_effect = FileNotFoundError()
    assert is_docker_installed() == False

def test_install_docker_with_winget(mocker):
    # Simuler le comportement de subprocess.run et de la fonction print
    mock_subprocess = mocker.patch('docker_utils.subprocess.run')
    mock_print = mocker.patch('builtins.print')
    
    # Test d'une installation réussie
    install_docker_with_winget()
    # Vérifier que subprocess.run a été appelé avec les bons arguments
    mock_subprocess.assert_called_once_with(["winget", "install", "Docker.DockerDesktop"], check=True)
    # Vérifier que le message de succès a été affiché
    mock_print.assert_called_with("Docker a été installé avec succès.")
    
    # Réinitialiser les mocks pour les tests suivants
    mock_subprocess.reset_mock()
    mock_print.reset_mock()
    
    # Test d'un échec d'installation
    # Simuler une erreur CalledProcessError, qui se produit quand la commande retourne un code d'erreur
    mock_subprocess.side_effect = subprocess.CalledProcessError(1, "winget")
    install_docker_with_winget()
    # Vérifier que le message d'erreur approprié a été affiché
    mock_print.assert_called_with("Erreur lors de l'installation de Docker : Command 'winget' returned non-zero exit status 1.")
    
    # Réinitialiser les mocks pour les tests suivants
    mock_subprocess.reset_mock()
    mock_print.reset_mock()
    
    # Test lorsque Winget n'est pas trouvé
    # Simuler une erreur FileNotFoundError, qui se produit quand la commande winget n'est pas trouvée
    mock_subprocess.side_effect = FileNotFoundError()
    install_docker_with_winget()
    # Vérifier que le message approprié a été affiché
    mock_print.assert_called_with("Winget n'est pas installé ou n'est pas dans le PATH.")
    
    # Réinitialiser les mocks pour les tests suivants
    mock_subprocess.reset_mock()
    mock_print.reset_mock()
    
    # Test d'une erreur inattendue
    # Simuler une exception générique
    mock_subprocess.side_effect = Exception("Unexpected error")
    install_docker_with_winget()
    # Vérifier que le message d'erreur inattendue a été affiché
    mock_print.assert_called_with("Une erreur inattendue s'est produite : Unexpected error")