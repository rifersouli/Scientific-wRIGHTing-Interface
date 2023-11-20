"""
Programa responsável por aplicar o algoritmo de pareamento (ou matching), no qual a partir
da escolha de uma frase do resumo científico feita pelo usuário, haverá uma comparação com
a resposta anotada, para saber se ele foi assertivo na frase que evoca o objetivo do texto.

@author = Nicholas Zilli
"""

import mariadb

mydb = mariadb.connect(
  host="localhost",
  user="root",
  password="123",
  database="tcc_zilli"
) # Conexão com o banco de dados

# Escolha do resumo em forma de número
RESUMO_ESCOLHIDO = int(input("Selecione um resumo para analisar (1 a 100): "))

def categoria_e_justificativa(resumo):
    """
    Função responsável por apresentar a categoria e justificativa que está o resumo científico.
    A partir de consultas no banco de dados, a função irá retornar em forma de string a categoria,
    sendo um conjunto de duas letras e um número, e a justificativa, que explica essa categoria.
    Categorias:
    OA1 - O objetivo está bem sinalizado e no local esperado
    OA2 - O objetivo está bem sinalizado, mas não no local esperado
    ON1 - Sem objetivo
    ON2 - Objetivo misturado ao problema
    ON3 - Objetivo misturado à metodologia
    @params: resumo (Número do resumo que foi escolhido pelo usuário)
    """

    mycursor = mydb.cursor()

    mycursor.execute("SELECT OBJ_CATEGORIA FROM OBJETIVO WHERE OBJ_ID="+str(resumo))

    myresult = mycursor.fetchone()
    CATEGORIA = ''.join(str(myresult)).replace("('","").replace("',)","")

    mycursor = mydb.cursor()

    mycursor.execute("SELECT OBJ_JUSTIFICATIVA FROM OBJETIVO WHERE OBJ_ID="+str(resumo))

    myresult = mycursor.fetchone()
    JUSTIFICATIVA = ''.join(str(myresult)).replace("('","").replace("',)","")
    return CATEGORIA, JUSTIFICATIVA

def frase_objetivo(vertice):
    """
    Função responsável por armazenar a construção linguística anotada previamente sobre cada resumo
    coletado, no qual contém a frase que evoca o objetivo. Logo essa função irá coletar essa frase
    para ser armazenada na matriz futuramente.

    @params: vertice (Número do vertice que precisa armazenar, relacionado com o número do resumo)
    """

    mycursor = mydb.cursor()
    mycursor.execute("SELECT OBJ_CONSTRUCOES_LINGUISTICAS FROM OBJETIVO WHERE OBJ_ID="+str(vertice))
    myresult = mycursor.fetchone()
    FRASE = ''.join(str(myresult)).replace("('","").replace("',)","")
    return FRASE

def resumo_com_marcacoes(resumo):
    """
    Função responsável por apresentar o resumo armazenado no banco de dados.
    Nele, há marcações para as frases que evocam o objetivo, no qual segue
    a seguinte sintaxe: --{Frase que evoca o objetivo}--
    A função também divide o resumo em frases, usando como delimitador o ".",
    assim podendo apresentar de uma forma mais visual ao usuário.

    @params: resumo (Número do resumo que foi escolhido pelo usuário)
    """

    mycursor = mydb.cursor()

    mycursor.execute("SELECT RES_RESUMO FROM RESUMOS WHERE RES_ID="+str(resumo))

    myresult = mycursor.fetchone()

    RESUMO_SEPARADO = str(myresult).replace("('","").replace("',)","").replace(".",".\n")

    RESUMO_EM_LISTA = RESUMO_SEPARADO.splitlines()

    return RESUMO_EM_LISTA

def frase_usuario_objetivo(resumo):
    """
    Função responsável por apresentar ao usuário o resumo que foi selecionado,
    no qual irá mostrar o título daquele resumo, as frases do resumo dividas
    em linhas, e sem as marcações citadas anteriormente. Além disso, ao
    apresentar as frases, há uma identificação delas por números, assim,
    quando o usuário precisar selecionar a frase que evoca o objetivo,
    ele irá digitar o número correspondente a frase. E assim, a função
    irá salvar a frase selecionada pelo usuário.

    @params: resumo (Número do resumo que foi escolhido pelo usuário)
    """

    mycursor = mydb.cursor()

    mycursor.execute("SELECT RES_TITULO FROM RESUMOS WHERE RES_ID="+str(resumo))

    myresult = mycursor.fetchone()

    RESUMO_TITULO = str(myresult).replace("('","").replace("',)","")

    print(f'\nResumo escolhido: {RESUMO_TITULO}\n')

    mycursor = mydb.cursor()

    mycursor.execute("SELECT RES_RESUMO FROM RESUMOS WHERE RES_ID="+str(resumo))

    myresult = mycursor.fetchone()

    RESUMO_SEPARADO = str(myresult).replace("('","").replace("',)","").replace("--{","").replace("}--","").replace("--[","").replace("]--","").replace(".",".\n")

    RESUMO_EM_LISTA = RESUMO_SEPARADO.splitlines()

    for TAMANHO in range(len(RESUMO_EM_LISTA)):
        print(str(TAMANHO) + ": " + RESUMO_EM_LISTA[TAMANHO])
        print("\n")

    print("\nSeleciona as frases a seguir usando os números apresentados a esquerda da frase.\n")

    SELECIONA_FRASE_OBJETIVO = input("Selecione a frase que evoca o objetivo: ")

    FRASE_USUARIO_OBJETIVO = RESUMO_EM_LISTA[int(SELECIONA_FRASE_OBJETIVO)]
    return FRASE_USUARIO_OBJETIVO

class Grafo(object):
    """
    Classe responsável por gerar o grafo, ou no caso, uma matriz de adjacência esparsa.
    """
    def __init__(self, size):
        """
        Função responsável por criar o grafo do tamanho passado.

        @params: size (tamanho do grafo)
        """
        self.adj_matrix = []
        for i in range(size):
            self.adj_matrix.append([None for i in range(size)])
        self.size = size

    def add_aresta(self, vertice_um, vertice_dois):
        """
        Adiciona as arestas na matriz, seguindo a seguinte lógica:
        - Caso você irá armazenar a frase que evoca o objetivo do
        resumo de número 1, ele estará na posição [0][1] da matriz.
        - Já no caso do resumo 2, ele estará na posição [3][2]
        - Já no caso do resumo 3, ele estará na posição [2][3]
        - Já no caso do resumo 4, ele estará na posição [5][4]
        - Já no caso do resumo 5, ele estará na posição [4][5]

        E assim para o resto dos resumos, com exceção que o último resumo fica
        na posição [99][99].

        @params: vertice_um (Número do primeiro vértice para adicionar a aresta)
        @params: vertice_dois (Número do segundo vértice para adicionar a aresta)
        """
        if vertice_um == vertice_dois:
            print(f'Mesmo vertice {vertice_um} e {vertice_dois}')

        self.adj_matrix[vertice_um][vertice_dois] = frase_objetivo(vertice_dois)
        self.adj_matrix[vertice_dois][vertice_um] = frase_objetivo(vertice_um)
        self.adj_matrix[99][99] = frase_objetivo(100)

    def remove_aresta(self, vertice_um, vertice_dois):
        """
        Remove as arestas da matriz. Por enquanto, não foi usada no programa.

        @params: vertice_um (Número do primeiro vértice para adicionar a aresta)
        @params: vertice_dois (Número do segundo vértice para adicionar a aresta)
        """
        if self.adj_matrix[vertice_um][vertice_dois] == 0:
            print(f'Sem arestas entre {vertice_um} e {vertice_dois}')
            return
        self.adj_matrix[vertice_um][vertice_dois] = 0
        self.adj_matrix[vertice_dois][vertice_um] = 0

    def __len__(self):
        """Retorna o tamanho do grafo. Por enquanto, não usada no programa."""
        return self.size

grafo = Grafo(100)
X = 0
Y = 1

while(X < 100 or Y < 100):
    grafo.add_aresta(X, Y)
    X += 2
    Y += 2

FRASE_USUARIO = frase_usuario_objetivo(RESUMO_ESCOLHIDO)

print("\n")

FRASE_ANOTADA = ""

# Aqui há umas condições para saber a partir do resumo selecionado, onde o programa precisa ir
# para consultar a frase anotada que evoca o objetivo, seguindo o raciocínio apresentado na
# documentação do grafo.

if RESUMO_ESCOLHIDO == 100:
    FRASE_ANOTADA = grafo.adj_matrix[99][99]
elif RESUMO_ESCOLHIDO % 2 != 0:
    FRASE_ANOTADA = grafo.adj_matrix[RESUMO_ESCOLHIDO - 1][RESUMO_ESCOLHIDO]
else:
    FRASE_ANOTADA = grafo.adj_matrix[RESUMO_ESCOLHIDO + 1][RESUMO_ESCOLHIDO]

print(f'Frase anotada: {FRASE_ANOTADA}')

print(f'Frase usuário: {FRASE_USUARIO}')

print("\n")

# Condições responsáveis por realizar o pareamento (ou matching) da frase anotada com a selecionada
# pelo usuário. Caso não haja objetivo no resumo selecionado,
# a frase anotada será uma string em branco, logo independente da frase selecionada pelo usuário,
# não irá parear, logo precisa retornar False. Caso contrário, irá fazer o pareamento normalmente.


if bool(FRASE_ANOTADA and FRASE_ANOTADA.strip()) == False:
    print(f'A frase do usuário combina com a anotada? {False}')
elif FRASE_ANOTADA in grafo.adj_matrix[0][1]:
    print(f'A frase do usuário combina com a anotada? {FRASE_ANOTADA in grafo.adj_matrix[0][1]}')
else:
    print(f'A frase do usuário combina com a anotada? {FRASE_ANOTADA in FRASE_USUARIO}')

RESUMO_MARCADO = resumo_com_marcacoes(RESUMO_ESCOLHIDO)

print("\nResumo com as marcações originais:\n")

for TAMANHO_RESUMO in range(len(RESUMO_MARCADO)):
    print(RESUMO_MARCADO[TAMANHO_RESUMO])

print(f'\nCategoria e Justificativa: {categoria_e_justificativa(RESUMO_ESCOLHIDO)}'.replace(")","").replace("(","").replace("'",""))
