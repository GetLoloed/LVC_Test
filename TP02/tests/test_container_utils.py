import pytest
from container_utils import generate_password, run_container

# Test de la fonction generate_password
def test_generate_password():
    password = generate_password()
    # Vérifie que le mot de passe a la longueur attendue
    assert len(password) == 12
    # Vérifie que le mot de passe contient au moins une lettre minuscule
    assert any(c.islower() for c in password)
    # Vérifie que le mot de passe contient au moins une lettre majuscule
    assert any(c.isupper() for c in password)
    # Vérifie que le mot de passe contient au moins un chiffre
    assert any(c.isdigit() for c in password)
    # Vérifie que le mot de passe contient au moins un caractère spécial
    assert any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password)

# Test paramétré de la fonction run_container
@pytest.mark.parametrize("image_name,use_volume,install_ssh", [
    ("python", False, False),
    ("mariadb", True, False),
    ("debian", False, True),
    ("ubuntu", True, True),
])
def test_run_container(mocker, image_name, use_volume, install_ssh):
    # Mock des fonctions et méthodes utilisées dans run_container
    mock_subprocess = mocker.patch('container_utils.subprocess.run')
    mock_print = mocker.patch('builtins.print')
    mocker.patch('container_utils.generate_password', return_value='test_password')
    mocker.patch('uuid.uuid4', return_value=mocker.Mock(hex='12345678'))
    mocker.patch('random.randint', return_value=50000)

    # Appel de la fonction à tester
    result = run_container(image_name, use_volume, install_ssh)

    # Vérification des noms générés
    expected_container_name = f"{image_name}-12345678"
    expected_volume_name = f"{expected_container_name}-volume" if use_volume else None

    # Vérification de la création du volume si nécessaire
    if use_volume:
        assert mock_subprocess.call_args_list[0] == mocker.call(["docker", "volume", "create", expected_volume_name], check=True)

    # Construction de la commande docker run attendue
    run_cmd = ["docker", "run", "-d", "--name", expected_container_name]
    if use_volume:
        run_cmd.extend(["-v", f"{expected_volume_name}:/data"])
    if install_ssh:
        run_cmd.extend(["-p", "50000:22"])
        run_cmd.append(image_name)
        run_cmd.extend(["/bin/bash", "-c", mocker.ANY])
    else:
        run_cmd.append(image_name)

    # Vérification de l'appel à docker run
    assert mock_subprocess.call_args_list[-1] == mocker.call(run_cmd, check=True)

    # Vérification des messages affichés
    assert mock_print.call_args_list[0] == mocker.call(f"Conteneur {image_name} lancé avec succès.")
    if use_volume:
        assert mock_print.call_args_list[1] == mocker.call(f"Volume persistent attaché : {expected_volume_name}")
    if install_ssh:
        assert mock_print.call_args_list[-5] == mocker.call("SSH installé et démarré dans le conteneur.")
        assert mock_print.call_args_list[-4] == mocker.call(f"Pour vous connecter en SSH, utilisez la commande suivante :")
        assert mock_print.call_args_list[-3] == mocker.call(f"ssh root@localhost -p 50000")
        assert mock_print.call_args_list[-2] == mocker.call(f"Le mot de passe pour l'utilisateur root est : test_password")
        assert mock_print.call_args_list[-1] == mocker.call("ATTENTION : Notez bien ce mot de passe, il ne sera plus affiché par la suite.")

    # Vérification du résultat retourné par run_container
    expected_result = (expected_container_name, 50000 if install_ssh else None, 'test_password' if install_ssh else None)
    assert result == expected_result