import pytest
from main import main, afficher_menu

def test_afficher_menu(capsys):
    # Test de la fonction afficher_menu
    afficher_menu()
    captured = capsys.readouterr()
    # Vérification que tous les éléments du menu sont présents dans la sortie
    assert "Choisissez un conteneur à télécharger et exécuter :" in captured.out
    assert "1. Conteneur Python" in captured.out
    assert "2. Conteneur MariaDB" in captured.out
    assert "3. Conteneur Debian (avec SSH)" in captured.out
    assert "4. Conteneur Ubuntu (avec SSH)" in captured.out
    assert "5. Quitter" in captured.out

@pytest.mark.parametrize("docker_installed,install_choice,container_choice", [
    (False, 'n', '5'),
    (True, '', '5'),
    (True, '', '1'),
    (True, '', '2'),
    (True, '', '3'),
    (True, '', '4'),
])
def test_main(mocker, docker_installed, install_choice, container_choice):
    # Simulation de l'état d'installation de Docker
    mocker.patch('main.is_docker_installed', return_value=docker_installed)
    # Création de mocks pour les fonctions d'installation et d'exécution de conteneur
    mock_install = mocker.patch('main.install_docker_with_winget')
    mock_run_container = mocker.patch('main.run_container')
    
    # Préparation des entrées simulées de l'utilisateur
    mock_inputs = [install_choice, container_choice]
    if container_choice != '5':
        mock_inputs.append('n')  # Choix de volume (non)
    mock_inputs.extend(['5', '5'])  # Pour sortir de la boucle et du programme
    
    # Simulation des entrées utilisateur
    mocker.patch('builtins.input', side_effect=mock_inputs)
    
    # Exécution de la fonction principale
    main()
    
    # Vérification de l'appel à l'installation de Docker si nécessaire
    if not docker_installed and install_choice.lower() == 'o':
        mock_install.assert_called_once()
    elif docker_installed or install_choice.lower() != 'o':
        mock_install.assert_not_called()
    
    # Vérification de l'exécution du conteneur si un choix valide a été fait
    if container_choice in ['1', '2', '3', '4']:
        mock_run_container.assert_called_once()
    else:
        mock_run_container.assert_not_called()