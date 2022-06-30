from math import gcd
from random import choice
from time import perf_counter

class EvenConvexPolygon:
    def __init__(self, NumberOfVertices):
        if NumberOfVertices % 2 != 0:
            raise Exception("Number of vertices must be even")
        self.NumberOfVertices = NumberOfVertices
        self.Diagonals = self.__Diagonals()
        self.DiagonalsInCycles = self.__DiagonalsInCycles()
        self.DiagonalsGraph = self.__DiagonalsGraph()
        self.DiagonalsRepeated = self.__DiagonalsRepeated()

    def __Diagonals(self):
        """Gera um conjunto com todas as diagonais de um polígono.

        Essa função é eficiente, não gera nenhuma possibilidade a mais
        """
        diagonals = []
        for fim in range(2, self.NumberOfVertices - 1):
            diagonals.append([0 , fim])
        for inicio in range(1, self.NumberOfVertices - 2):
            for fim in range(inicio + 2, self.NumberOfVertices):
                diagonals.append([inicio, fim])
        return diagonals

    def __DiagonalsInCycles(self):
        """Gera todas as diagonais por ciclos, cada ciclo tem um intervalo diferente;

        Ex: {2: {0: [0, 2, 4, 0], 1: [1, 3, 5, 1]}, 3: {0: [0, 3], 1: [1, 4], 2: [2, 5]}}
        """
        diagonais = {}
        #são necessarios ciclos de dois até diagonal divido por dois
        for gerador in range(2, int(self.NumberOfVertices / 2) + 1):
            diagonais.setdefault(gerador, [])
            #cada ciclo vai aparecer mdc de vertices e gerador vezes, cada vez começando de inicio mais um
            for rotacao in range(gcd(self.NumberOfVertices, gerador)):
                ciclo = []
                #incide de cada numero no ciclo
                for indiceciclo in range(0 , int(self.NumberOfVertices / gcd(self.NumberOfVertices, gerador))):
                    #operacao para ter o intervalo certo entre os numeros
                    ciclo.append((rotacao + (indiceciclo * gerador)) % self.NumberOfVertices)
                if len(ciclo) > 2:
                    #qualquer ciclo maior que dois vai terminar onde comecou
                    #tamanho dois voltar para o inicio seria uma repetição da diagonal
                    ciclo.append(rotacao)
                diagonais[gerador].append(ciclo)
        return diagonais

    def __DiagonalsGraph(self):
        """Gera um grafo mostrando para cada vertices com quais outros vertices ele pode ser ligado para formar uma diagonal."""
        grafo = []
        for vertice in range(self.NumberOfVertices):
            diagonaisDoVertices = []
            for diagonal in range(vertice + 2, vertice + 2 + self.NumberOfVertices - 3):
                diagonaisDoVertices += [diagonal % self.NumberOfVertices]
            grafo += [diagonaisDoVertices]
        return grafo
    
    def __DiagonalsRepeated(self):
        """Gera todas as possibilidades de repetir diagonais em grafos pares para que tenham caminhos eulerianos.

        Os grafos pares precisam de (n-2)/2 diagonais repetidas para terem caminhos eulerianos 
        Assume inicio no vertice 0 e muda o fim até n/2 para cada fim gera os grafos com as diagonais repetidas
        """

        def EncontraRepeticoes(verticeslistados, MontandoDiagonaisRepetidas, DiagonaisRepetidas):
            """Encontra recursivamente as repetições nas listas sem os vértices já utilizados.
            """
            for vertice in verticeslistados[1:]: #para cada vertices do segundo em diante
                if verticeslistados[0] + 1 != vertice: #se não for adjacente com o primeiro
                    MontandoDiagonaisRepetidas.append((verticeslistados[0], vertice)) #acrescenta na lista montando
                    #repassa a lista sem os dois vertices para a funcao
                    EncontraRepeticoes([i for i in verticeslistados if i != verticeslistados[0] and i != vertice], MontandoDiagonaisRepetidas, DiagonaisRepetidas)
                    #se lista montando tiver (tamanho n -2) / 2
                    if len(MontandoDiagonaisRepetidas) == (self.NumberOfVertices - 2) / 2:
                        #acrescenta nas diagonais repetidas prontas
                        DiagonaisRepetidas.append(MontandoDiagonaisRepetidas.copy())
                    #retira da lista montando a última possibilidade adicionada
                    MontandoDiagonaisRepetidas.pop()
            return DiagonaisRepetidas

        finsErepeticoes = {} #dicionario onde serão guardados todas as repetições para cada final
        for fim in range(1, int(self.NumberOfVertices / 2) + 1): #final até metade da quantidade de vértices
            #gera uma lista com os vertices restantes e passa para encontrar repeticoes
            DiagonaisRepetidas = EncontraRepeticoes([i for i in range(self.NumberOfVertices) if i != 0 and i != fim], [], [])
            #quarda no dicionario
            finsErepeticoes.update({fim: DiagonaisRepetidas})
        return finsErepeticoes

def GrafoCaminhosAleatorios(graph, diagonais, depth, depthcount=0, node=0, path=[0]):
    """Aleatoriamente encontra caminhos no grafo que passam por todas as diagonais pelo uma vez.

    São possíveis cíclos de 3 nodesnos caminhos, mas não 2 (a função não volta diretamente para o vértice de trás).
    """
    #se não existir mais nenhuma diagonal desconhecida retorna
    if diagonais == set():
        return path
    #se o limite superior de nodes for alcando e o caminho não for achado retorna
    if depthcount == depth:
        return 1

    #escolhe um proximo node aleatoriamente
    node = choice(graph[node])
    while [node] == path[-2:-1]:
        #se o node for igual ao anterior procura outro
        node = path[-1]
        node = choice(graph[node])

    #acrescenta o novo node no caminho e retira a diagonal da lista de todas as diagonais
    path.append(node)
    diagonais.discard(frozenset(path[-2:]))

    #avança para o proximo node e procura a partir dele
    depthcount += 1
    return GrafoCaminhosAleatorios(graph, diagonais, depth, depthcount=depthcount, node=node, path=path)

convexPolygon = EvenConvexPolygon(8)

#________________________________________________________________________________________________

"""
Diagonais  = {0:[]}
DiagomaisEmCiclo =  {2:{0:[], 1:[]},3:{...}}
DiagonaisGrafo = [[][][]]

Diagonais_ComRepeticoes = {fim: [], fim: []}
DiagonaisEmCiclo_ComRepeticoes = ?
DiagonaisGrafo_ComRepeticoes = [[][][]]
"""

"""
vertices = 1
depth = 50
maxfails = 5000000
diagonais = Diagonais(vertices)
grafo = GrafoVerticesEDiagonais(vertices)

comrepeticoes4_time = perf_counter()
comrepeticoes4 = DiagonaisRepetidasGrafosPares(vertices)
comrepeticoes4_time = perf_counter() - comrepeticoes4_time

filename = f'{vertices} vertices.txt'
pathsfound = []

try:
    with open(filename, 'r') as f:
        lines = f.readlines()
    depth = int(lines[0].rsplit(':')[1].strip())
    for line in lines[2:]:
        line = line.rsplit('.', 1)[1].strip()
        path = []
        for num in line.split(','):
            num = num.strip()
            if num.isdigit():
                path.append(int(num))
        pathsfound.append(path)
    del lines, line, num
except FileNotFoundError:
    pass

fails = 0
while fails < maxfails:
    newpath = GrafoCaminhosAleatorios(grafo, diagonais.copy(), depth, path=[0])
    if newpath != 1 and newpath not in pathsfound:
        path = newpath
        depth = len(path) - 1
        pathsfound.append(path)
    else:
        fails += 1

if len(pathsfound) != 0:
    with open(filename, 'w') as f:
        f.write(f'menor tamanho: {depth}' + '\n\n')
        s = ''
        for count, path in enumerate(pathsfound):
            s =f'{count + 1}. '
            for num in path:
                s += f'{num}, '
            f.write(s.rstrip(', ') + '\n')
            s = ''
"""