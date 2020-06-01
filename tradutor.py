# coding: utf-8
import json
import os
from unidecode import unidecode
from colored import fg, bg, attr
import ctypes

# Define o como o CMD será apresentado
LF_FACESIZE = 32
STD_OUTPUT_HANDLE = -11

class COORD(ctypes.Structure):
    _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

class CONSOLE_FONT_INFOEX(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_ulong),
                ("nFont", ctypes.c_ulong),
                ("dwFontSize", COORD),
                ("FontFamily", ctypes.c_uint),
                ("FontWeight", ctypes.c_uint),
                ("FaceName", ctypes.c_wchar * LF_FACESIZE)]

font = CONSOLE_FONT_INFOEX()
font.cbSize = ctypes.sizeof(CONSOLE_FONT_INFOEX)
font.nFont = 12
font.dwFontSize.X = 11
font.dwFontSize.Y = 18
font.FontFamily = 54
font.FontWeight = 400
font.FaceName = "Castro Console"

handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
ctypes.windll.kernel32.SetCurrentConsoleFontEx(
        handle, ctypes.c_long(False), ctypes.pointer(font))

# Fonte e cores para as letras
base = fg('purple_3')+attr('bold')
cor = fg('yellow')+bg('purple_3')+attr('bold')
reset = attr('reset')+attr('bold')
sucesso = fg('green')+attr('bold')
alerta = fg('yellow')+attr('bold')
erro = fg('yellow')+attr('bold')
text = fg('yellow')+bg('purple_3')+attr('bold')

#Abre o aqrquivo JSON
with open('palavras.json', 'r') as a: palavras = json.load(a)

#Salva e define como o arquivo será identado
def add_json(data):
    with open('palavras.json', 'w') as arq: json.dump(palavras, arq, indent=2)


#Adiciona as palavras no arquivo JSON
def adiciona(palavras: dict, idioma_1: str, idioma_2: str):
   palavras[idioma_1] = idioma_2
   return palavras

#Resposnsável pela tradução
def Por_to_En(palavras: dict, entrada: str): 
    for e in palavras:
        if (palavras[e] == entrada): return e  # retorna a chave  
            
        elif (entrada == e): return palavras[e] # retorna valor

    if (entrada not in palavras[e] and entrada not in palavras): return erro + 'Palavra Inválida / inexistente'


#Quando o usuário digitar frases, elas serão reconhecidas ao colocar espaços. EX: 'color blue is amazing' se colocar virgula ou pontos não será reconhecido.
def texto(palavras: dict, entrada: list):
    lst = []
    for palavra in entrada:
        for k, v in palavras.items():
            if (palavra == k): lst.append(v)

            elif (palavra == v): lst.append(k)

    return ' '.join(lst)


#deleta a palavra e sua tradução
def exclui(deletar_palavra: str):
    save = 0    
    for e in palavras:
        if (palavras[e] == deletar_palavra):
            save = 1    
            break   
            
        elif (deletar_palavra == e):
            save = 1
            break
    if (save == 1):
        palavras.pop(e)
        add_json(e)
    return 'exclusão bem sucedida'


#A partir daqui é o programa rodando.
while (True):
    print(base + '\nPara adicionar mais palavras em outros idiomas digite "ADD". \nPara deletar palavras digite "DEL". \nPara consultar tradução de uma frase com mais de uma palavra, digite "TXT". \nCaso contrário digite a palavra que procura. \nPara consultar todo o conteúdo do tradutor, digite "MOSTRAR". \nPara encerrar o programa, digie "EXIT".\n')
    entrada: str = unidecode(input('Digite o que procura: ').lower().strip(' '))
    os.system('cls')

    #Ao digitar 'add' adicionará palavras ao arquivo JSON
    if (entrada == 'add'):
        idioma_1: str = unidecode(input('Digite a palavra em um idioma: ').lower())
        idioma_2: str = unidecode(input(f'Digite a palavra "{idioma_1}" em outro idioma: ').lower())
        
        #Caso queira adicionar alguma palavra que já exista no JSON, aparecerá esta mensagem
        if (idioma_1 in palavras or idioma_2 in palavras): print(alerta + 'Palavras já existem')

        #Caso as palavras não existam no arquivo JSON, elas serão salvas com sucesso
        elif (idioma_1 not in palavras or idioma_2 not in palavras):
            adiciona(palavras, idioma_1, idioma_2)
            add_json(adiciona)
            print(sucesso + f'Palavras "{idioma_1}" e "{idioma_2}" adicionadas com sucesso')

    #Ao digitar 'txt', irá consultar mais de uma palavra. Só irá conseguir consultar se colocar espaço entre elas. 
    # EX: 'color blue is amazing' 
    # Se colocar algum ponto, virgula, sinais, etc...  como: 'color blue, is amazing!' não irá funcionar
    elif (entrada == 'txt'):
        txt: str = input('Digite o texto: ').lower().split(' ')
        print(text + 'A tradução de', ' '.join(txt), f'é "{texto(palavras,txt)}"' +reset)

    #Caso digite 'del', irá deletar a palavra digitada e sua tradução
    elif (entrada == 'del'):
        deletar_palavra: str = input('Digite a palavra que deseja excluir: ')
        print(sucesso +f'{exclui(deletar_palavra)} da palavra "{deletar_palavra}" e sua tradução')
    
    #Caso digite 'mostrar', aparecerá tudo que está salvo no arquivo JSON
    elif (entrada == 'mostrar'):
        for k, v in palavras.items(): print (alerta + '{0:>10}'.format(k), ':', '{0:>0}'.format(v))
        print('\nAqui são todas as palvras existentes no tradutor' + reset)

    #Caso digite 'exit' o progrma será encerrado
    elif (entrada == 'exit'): 
        print('\nPrograma encerrado')
        break
    
    #Caso digitar alguma palavra que exista no JSON mostrará a tradução dessa palavra
    else: print(cor + f'\nA tradução de "{entrada}" é "{Por_to_En(palavras,entrada)}"'+reset)

