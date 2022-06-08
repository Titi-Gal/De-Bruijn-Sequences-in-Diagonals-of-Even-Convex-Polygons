from math import gcd
from random import choice

def Diagonais(vertices, parcial=False, duplas=1):
    """
    Gera um conjunto com todas as diagonais de um polígono
    Essa função é eficiente, não gera nenhuma possibilidade a mais
    """
    diagonais = set()
    for destino in range(2, vertices - 1):
        diagonais.add(frozenset([0 , destino]))
    for origem in range(1, vertices - 2):
        for destino in range(origem + 2, vertices):
            diagonais.add(frozenset([origem, destino]))
    if parcial:
        for dupla in range(duplas, int(vertices / 2)):
            diagonais.discard({dupla, (dupla + (vertices / 2)) % vertices})
    return diagonais

def CiclosDiagonais(vertices):
    """
    Gera todos ciclos correspondentes as diagonais
    Ex com 6:
    {2: {0: [0, 2, 4, 0], 1: [1, 3, 5, 1]}, 3: {0: [0, 3], 1: [1, 4], 2: [2, 5]}}
    """
    diagonais = {}
    for gerador in range(2, int(vertices / 2) + 1):
        diagonais.setdefault(gerador, {})
        for rotacao in range(gcd(vertices,gerador)):
            ciclo = []
            for indiceciclo in range(0 , int(vertices / gcd(vertices,gerador))):
                ciclo.append((rotacao + (indiceciclo * gerador)) % vertices)
            if len(ciclo) > 2:
                ciclo.append(rotacao)
            diagonais[gerador].setdefault(rotacao, ciclo)
    return diagonais

def VerticesPossibilidades(vertices, parcial=False, duplas=1):
    """
    Gera um grafo mostrando para cada vertices com quais outros vertices ele pode ser ligado para formar uma diagonal
    """
    graph = []
    for vertice in range(vertices):
        possibilities = []
        for diagonal in range(vertice + 2, vertice + 2 + vertices - 3):
            possibilities += [diagonal % vertices]
        graph += [possibilities]

    if parcial:
        assert (vertices % 2) == 0, f'Grafos parciais são para uma quatidade par de vértices, recebido {vertices} vertices' 
        assert duplas < vertices / 2, f'duplas deve ser < vertices / 2 para grafos parciais, vertices: {vertices}, duplas: {duplas}'
        for vertice, possibilidades in enumerate(graph[duplas:]):
            possibilidades.remove((vertice + duplas + (vertices / 2)) % vertices)

    return graph

def CaminhoAleatorio(graph, diagonais, depth, depthcount=0, node=0, path=[0]):
    """
    Aleatoriamente encontra caminhos no grafo que passam por todas as diagonais pelo uma vez
    São possível cíclos de 3 nodes, mas não 2
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
    return CaminhoAleatorio(graph, diagonais, depth, depthcount=depthcount, node=node, path=path)

vertices = 12
parcial = False
duplas = 2
depth = 50
maxfails = 5000000
diagonais = Diagonais(vertices, parcial=parcial, duplas=duplas)
grafo = VerticesPossibilidades(vertices, parcial=parcial, duplas=duplas)

if parcial:
    filename = f'{vertices} vertices, parcial {parcial}, duplas {duplas}.txt'
else:
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
    newpath = CaminhoAleatorio(grafo, diagonais.copy(), depth, path=[0])
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