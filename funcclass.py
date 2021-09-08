from datetime import date as data
from csv import DictWriter, DictReader
"""
Arquivo principal contendo classes, constantes e funções
"""

DB_PATH = 'A:\\agenda\\db.csv'  # Caminho absoluto do banco de dados CSV.

CAMPOS = ('nome', 'e-mail', 'telefone', 'nasc')  # Tupla contendo os nomes dos campos a serem armazenados no CSV.

CONF = ('s', 'n', 'S', 'N')  # Opções de confirmação para uso como referência.


class Pessoa:
    """
    Classe base do cadastro de pessoas.

    dados: Nome, E-Mail, Telefone e Data de Nascimento.

    Calcula a idade do sujeito e permite alteraçao posterior de dados.
    """
    def __init__(self, nome: str, email: str, telefone: str, nascimento: list):
        self.__nome: str = nome.title()
        self.__email: str = email.lower()
        self.__telefone: str = telefone
        self.__nascimento: data = data(day=nascimento[0], month=nascimento[1], year=nascimento[2])
        if data.today() < self.__nascimento.replace(year=data.today().year):
            self.__idade: int = data.today().year - self.__nascimento.year - 1
        else:
            self.__idade: int = data.today().year - self.__nascimento.year

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome.title()

    @property
    def telefone(self):
        return self.__telefone

    @telefone.setter
    def telefone(self, tel: str):
        self.__telefone = tel

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, novo_email: str):
        self.__email = novo_email

    @property
    def idade(self):
        return self.__idade

    @property
    def nascimento(self):
        return f'{self.__nascimento.day}/{self.__nascimento.month}/{self.__nascimento.year}'

    def dados(self):
        dados = {"nome": str(self.__nome), "e-mail": str(self.__email), "telefone": str(self.__telefone),
                 "nasc": f'{self.__nascimento.day}/{self.__nascimento.month}/{self.__nascimento.year}'}
        return dados


def escrever(entrada: dict):
    """
    Escreve uma entrada no banco de dados.
    :param entrada:  uma lista de Strings contendo os dados a serem escritos.
    :return: None
    """
    with open(DB_PATH, 'a', newline='') as database:
        escreve = DictWriter(database, fieldnames=CAMPOS)
        escreve.writerow(entrada)


def resetdb():
    """
    Apaga o banco de dados antes de reescrevê-lo escrevendo os campos iniciais.
    :return: Sem retorno.
    """
    with open(DB_PATH, 'w', newline='') as database:
        base = DictWriter(database, fieldnames=CAMPOS)
        base.writeheader()


def leitura():
    """
    Monta o banco de dados em uma lista de objetos da classe Pessoa.
    :return: Retorna uma lista de objetos da classe Pessoa.
    """
    with open(DB_PATH, 'r') as database:
        pessoas = \
            [Pessoa(str(pessoa['nome']), str(pessoa['e-mail']), str(pessoa['telefone']),
                    [int(dado) for dado in pessoa['nasc'].split('/')]) for pessoa in DictReader(database)]
    return pessoas


def apagar(nome_part: str):
    """
    Apaga um contato na lista do banco de dados e o reescreve sem o mesmo.
    :param nome_part: String contendo um trecho do nome do contato a ser apagado.
    :return: sem retorno além da confirmação da deleção do contato.
    """
    base = leitura()
    for ppl in base:
        if nome_part.lower() in ppl.nome.lower():
            print(f'{ppl.nome} foi encontrado.', 'Deseja apagar o contato?', sep='\n')
            ent = input('Digite "s" para sim ou "n" para não: ')
            while ent not in CONF:
                ent = input('Digite "s" para sim ou "n" para não: ')
            else:
                if ent.lower() == 's':
                    base.remove(ppl)
                    print('Contato removido com sucesso.')

    resetdb()

    for ppl in base:
        escrever(ppl.dados())


def hoje():
    return data.today()


def ordenar(base: list):
    s_base = sorted(base, key=lambda a: a.nome.lower())
    return s_base


def listar(base: list):
    """
    Lista toda a base de contatos de maneira formatada.
    :param base: banco de dados a ser informado
    :return: Lista completa impressa formatada de contatos
    """
    form_str = []
    for pessoa in base:
        form_str.append(f'Nome: {pessoa.nome.split()[0]} {pessoa.nome.split()[-1]} - E-Mail: {pessoa.email} -'
                        f' Telefone: {pessoa.telefone} - Idade: {pessoa.idade} - Nascimento: {pessoa.nascimento}')
    return print(*form_str, sep='\n')


def recebe_data():
    """
    Monta a data de nascimento do contato.
    :return: retorna uma lista formatada com a data.
    """
    k = ('dia', 'mês', 'ano')
    anos = tuple(range(1900, int(hoje().year) + 1))
    meses = tuple(range(1, 13))
    dias = tuple(range(1, 32))
    date = []
    for i in range(3):
        ent = int(input(f'Insira o {k[i]} da data de nascimento: '))
        if i == 0:
            while ent not in dias:
                ent = int(input(f'Valor inválido!\nInsira o {k[i]} da data de nascimento: '))
            else:
                date.append(ent)
        elif i == 1:
            while ent not in meses:
                ent = int(input(f'Valor inválido!\nInsira o {k[i]} da data de nascimento: '))
            else:
                date.append(ent)
        elif i == 2:
            while ent not in anos:
                ent = int(input(f'Valor inválido!\nInsira o {k[i]} da data de nascimento: '))
            else:
                date.append(ent)
    return date


def busca(nome: str):
    resul = []
    for pessoa in leitura():
        if nome.lower() in pessoa.nome.lower():
            resul.append(f'{pessoa.nome.split()[0]} {pessoa.nome.split()[-1]} - TEL: {pessoa.telefone} -'
                         f' E-mail: {pessoa.email} - Nasc.: {pessoa.nascimento} - Idade: {pessoa.idade}')
    return print(*resul, sep='\n')
