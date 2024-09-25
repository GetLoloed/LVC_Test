import pytest
import os_detector

def test_obtenir_sys_info(mocker):
    # Simulez le retour de platform.uname()
    mock_uname = mocker.Mock()
    mock_uname.system = 'Linux'
    mock_uname.node = 'test_node'
    mock_uname.release = '5.4.0-42-generic'
    mock_uname.version = '#46-Ubuntu SMP Fri Jul 10 00:24:02 UTC 2020'
    mock_uname.machine = 'x86_64'
    mock_uname.processor = 'x86_64'
    
    mocker.patch('platform.uname', return_value=mock_uname)

    expected_result = {
        'System Type': 'Linux',
        'Node Name': 'test_node',
        'Release': '5.4.0-42-generic',
        'Version': '#46-Ubuntu SMP Fri Jul 10 00:24:02 UTC 2020',
        'Machine': 'x86_64',
        'Processor': 'x86_64'
    }

    result = os_detector.obtenir_sys_info()
    assert result == expected_result  # Vérifie si le résultat est égal à l'attendu

def test_get_windows_hardware_info(mocker):
    # Simulez le retour de platform.system() et subprocess.check_output
    mocker.patch('platform.system', return_value='Windows')

    mocker.patch('os_detector.subprocess.check_output', side_effect=[
        "Name\nIntel(R) Core(TM) i7-8565U CPU @ 1.80GHz\n".encode(),
        "Capacity\n17179869184\n".encode()  # 16 Go
    ])

    expected_result = {
        'CPU': 'Intel(R) Core(TM) i7-8565U CPU @ 1.80GHz',
        'Total Memory (GB)': 16.0
    }

    result = os_detector.get_windows_hardware_info()
    assert result == expected_result

def test_get_linux_hardware_info(mocker):
    # Simulez le retour de platform.system() et subprocess.check_output
    mocker.patch('platform.system', return_value='Linux')

    mocker.patch('os_detector.subprocess.check_output', side_effect=[
        "Model name: Intel(R) Core(TM) i7-8565U CPU @ 1.80GHz\n".encode(),
        "MemTotal: 16777216 kB\n".encode()  # 16 Go
    ])

    expected_result = {
        'CPU': 'Intel(R) Core(TM) i7-8565U CPU @ 1.80GHz',
        'Total Memory (GB)': 16.0
    }

    result = os_detector.get_linux_hardware_info()
    assert result == expected_result

def test_get_hardware_info(mocker):
    # Simulez les appels aux fonctions pour obtenir les informations système
    mocker.patch('os_detector.obtenir_sys_info', return_value={'System Type': 'Linux'})
    mocker.patch('os_detector.get_linux_hardware_info', return_value={'CPU': 'Intel', 'Total Memory (GB)': 16})

    system_info = os_detector.obtenir_sys_info()
    type_systeme = system_info['System Type']
    
    if type_systeme == 'Windows':
        hardware_info = os_detector.get_windows_hardware_info()
    elif type_systeme == 'Linux':
        hardware_info = os_detector.get_linux_hardware_info()
    else:
        pytest.skip(f"Test non applicable pour le système : {type_systeme}")

    assert isinstance(hardware_info, dict)
    assert 'CPU' in hardware_info
    assert 'Total Memory (GB)' in hardware_info