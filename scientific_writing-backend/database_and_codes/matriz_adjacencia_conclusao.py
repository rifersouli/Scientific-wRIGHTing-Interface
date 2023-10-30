"""
Programa responsável por aplicar o algoritmo de pareamento (ou matching), no qual a partir
da escolha de uma frase do resumo científico feita pelo usuário, haverá uma comparação com
a resposta anotada, para saber se ele foi assertivo na frase que evoca a conclusão do texto.

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
    CA1 - A conslusão está bem sinalizada e no local esperado
    CA2 - A conslusão está bem sinalizada, mas não no local esperado
    CN1 - Sem conclusão
    CN2 - Conclusão misturada à metodologia
    CN3 - Conclusão misturada aos resultados
    @params: resumo (Número do resumo que foi escolhido pelo usuário)
    """

    mycursor = mydb.cursor()

    mycursor.execute("SELECT CON_CATEGORIA FROM CONCLUSAO WHERE CON_ID="+str(resumo))

    myresult = mycursor.fetchone()
    CATEGORIA = ''.join(str(myresult)).replace("('","").replace("',)","")

    mycursor = mydb.cursor()

    mycursor.execute("SELECT CON_JUSTIFICATIVA FROM CONCLUSAO WHERE CON_ID="+str(resumo))

    myresult = mycursor.fetchone()
    JUSTIFICATIVA = ''.join(str(myresult)).replace("('","").replace("',)","")
    return CATEGORIA, JUSTIFICATIVA

def frase_conclusao(vertice):
    """
    Função responsável por armazenar a construção linguística anotada previamente sobre cada resumo
    coletado, no qual contém a frase que evoca a conclusão. Logo essa função irá coletar essa frase
    para ser armazenada na matriz futuramente.

    @params: vertice (Número do vertice que precisa armazenar, relacionado com o número do resumo)
    """

    mycursor = mydb.cursor()
    mycursor.execute("SELECT CON_CONSTRUCOES_LINGUISTICAS FROM CONCLUSAO WHERE CON_ID="+str(vertice))
    myresult = mycursor.fetchone()
    FRASE = ''.join(str(myresult)).replace("('","").replace("',)","")
    return FRASE

def resumo_com_marcacoes(resumo):
    """
    Função responsável por apresentar o resumo armazenado no banco de dados.
    Nele, há marcações para as frases que evocam a conclusão, no qual segue
    a seguinte sintaxe: --[Frase que evoca a conclusão]--
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

def frase_usuario_conclusao(resumo):
    """
    Função responsável por apresentar ao usuário o resumo que foi selecionado,
    no qual irá mostrar o título daquele resumo, as frases do resumo dividas
    em linhas, e sem as marcações citadas anteriormente. Além disso, ao
    apresentar as frases, há uma identificação delas por números, assim,
    quando o usuário precisar selecionar a frase que evoca a conclusão,
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

    SELECIONA_FRASE_CONCLUSAO = input("Selecione a frase que evoca a conclusão: ")

    FRASE_USUARIO_CONCLUSAO = RESUMO_EM_LISTA[int(SELECIONA_FRASE_CONCLUSAO)]
    return FRASE_USUARIO_CONCLUSAO

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
        - Caso você irá armazenar a frase que evoca a conclusão do
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
            print(f'Mesmo vértice {vertice_um} e {vertice_dois}')

        self.adj_matrix[vertice_um][vertice_dois] = frase_conclusao(vertice_dois)
        self.adj_matrix[vertice_dois][vertice_um] = frase_conclusao(vertice_um)
        self.adj_matrix[99][99] = frase_conclusao(100)

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

print(grafo.adj_matrix[5][4])

FRASE_USUARIO = frase_usuario_conclusao(RESUMO_ESCOLHIDO)

print("\n")

FRASE_ANOTADA = ""

# Aqui há umas condições para saber a partir do resumo selecionado, onde o programa precisa ir
# para consultar a frase anotada que evoca a conclusão, seguindo o raciocínio apresentado na
# documentação do grafo.

if RESUMO_ESCOLHIDO == 100:
    FRASE_ANOTADA = grafo.adj_matrix[99][99]
elif RESUMO_ESCOLHIDO % 2 != 0:
    FRASE_ANOTADA = " " + grafo.adj_matrix[RESUMO_ESCOLHIDO - 1][RESUMO_ESCOLHIDO]
else:
    FRASE_ANOTADA = " " + grafo.adj_matrix[RESUMO_ESCOLHIDO + 1][RESUMO_ESCOLHIDO]

print(f'Frase anotada: {FRASE_ANOTADA}')

print(f'Frase usuário: {FRASE_USUARIO}')

print("\n")

# Condições responsáveis por realizar o pareamento (ou matching) da frase anotada com a selecionada
# pelo usuário. Caso não haja conclusão no resumo selecionado,
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
