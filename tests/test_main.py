from src.main import sumar


def test_sumar_correcto():
    assert sumar(2, 3) == 5
    assert sumar(-1, 1) == 0


def test_sumar_incorrecto():
    assert sumar(2, 2) != 5