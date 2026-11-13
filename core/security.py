from passlib.context import CryptContext

CRIPTO = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_senha(senha: str, senha_hash: str) -> bool:
    """
    função para verificar se a senha fornecida corresponde ao hash armazenado no banco de dados.
    :param senha: A senha fornecida pelo usuário.
    :param senha_hash: O hash da senha armazenado no banco de dados.
    :return: True se a senha for correta, False caso contrário.
    """
    return CRIPTO.verify(senha, senha_hash)

def gerar_hash_senha(senha: str) -> str:
    """
    função para gerar um hash seguro da senha fornecida.
    :param senha: A senha fornecida pelo usuário.
    :return: O hash da senha.
    """
    return CRIPTO.hash(senha)