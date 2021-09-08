"""
Arquivo principal do programa.
"""
from funcclass import Pessoa, leitura, escrever, recebe_data, resetdb, apagar, hoje, ordenar, listar, CONF, busca
import os
cont = True
menu = ('Agenda de contatos:', 'Selecione uma das opções abaixo:', '1 - Adicionar contato', '2 - Remover contato',
        '3 - Listar todos os contatos', '4 - Buscar um contato', '5 - Aniversariantes do mês', '6 - Sair ')


def sair():
    """
    Executa um questionamento acerca da continuidade ou não do programa.
    :return: True or False
    """
    salir = input('Deseja sair?\nDigite "s" para sim ou "n" para não: ')
    while salir not in CONF:
        salir = input('Opção inválida!\nDigite "s" para sim ou "n" para não: ')
    else:
        if salir.lower() == "s":
            return False
        elif salir.lower() == "n":
            return True


opt = tuple(range(1, 7))
# Menu
while cont:
    os.system('cls')
    print(*menu, sep='\n')
    try:
        sel = int(input('\nSelecione a opção: '))
    except ValueError:
        print('Opção inválida!\nVocê deve digitar obrigatótiamente um número!')
        sel = int(input('\nSelecione a opção: '))

    while sel not in opt:
        sel = int(input('\nOpção inválida!\nSelecione uma opção dentre as listadas acima: '))
    else:
        if sel == 1:
            nome = input('Insira o nome do contato: ')
            email = input('Insira o e-mail do contato: ')
            tel = input('Insira o telefone do contato: ')
            nasc = recebe_data()
            person = Pessoa(nome, email, tel, nasc)
            escrever(person.dados())
            base = ordenar(leitura())
            resetdb()
            for ppl in base:
                escrever(ppl.dados())
            print(f'Dados do contato {person.nome} armazenados com sucesso!')
            cont = sair()
        elif sel == 2:
            nom = input('Insira parte do nome do contato que deseja apagar: ')
            apagar(nom)
            cont = sair()
        elif sel == 3:
            listar(leitura())
            cont = sair()
        elif sel == 4:  # Todo
            nomb = input('Digite o nome (ou parte dele) do contato que deseja localizar: ')
            busca(nomb)
            cont = sair()
        elif sel == 5:
            aniversariantes = []
            meses = (0, 'janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto',
                     'setembro', 'outubro', 'novembro', 'dezembro')
            for ppl in leitura():
                if int(ppl.nascimento.split('/')[1]) == hoje().month:
                    aniversariantes.append(f'{ppl.nome} - {ppl.nascimento}')
            print(f'Os aniversariantes do mês de {meses[hoje().month].title()} são:', *aniversariantes, sep='\n')
            cont = sair()
        elif sel == 6:
            cont = False
