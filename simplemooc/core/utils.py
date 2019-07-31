import hashlib
import string
import random


def random_key(size: int = 5):
    """
    Retorna uma palavra formada randomicamente com os caracteres acima, do tamanho informado em size
    :param size: Tamnho da palavra a ser retornada
    :return:
    """
    # todas as letras em maiúsculas + todos os dígitos
    chars = string.ascii_uppercase + string.digits
    return ''.join([random.choice(chars) for i in range(size)])


def generate_hash_key(salt, size: int = 5):
    """
    Gera uma chave aleatória
    :param salt: Palavra chave
    :param size: tamanho do key original antes do hash
    :return: hash
    """
    # Gera uma palavra aleatória
    random_str = random_key(size)
    # Acrescenta o texto personalizado à palavra aleatória
    text = random_str + salt
    # Gera o hash
    return hashlib.sha224(text.encode('utf-8')).hexdigest()
