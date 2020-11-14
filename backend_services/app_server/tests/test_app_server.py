from backend_services.app_server import __version__


def test_version():
    assert __version__ == "0.1.0"
