# -*- coding: utf-8 -*-
"""
PyConES 2016 Almería
"""


def decode_pass(fpass, fpriv):
    """Función de decodificación de ficheros encriptados.

    Args:
        fpass (str): Ruta al fichero encriptado a decodificar.
        fpriv (str): Path a la ``clave privada``.

    Returns:
        str: En función del resultado de la extracción.

    """

    from M2Crypto import RSA

    with open(fpass, 'r') as fichero_salt:
        passwd = fichero_salt.read()

    return RSA.load_key(fpriv).private_decrypt(passwd,
                                               RSA.pkcs1_padding).strip()
