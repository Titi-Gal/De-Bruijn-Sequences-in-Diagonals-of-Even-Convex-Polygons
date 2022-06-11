from math import gcd
from random import choice

def Diagonais(vertices):
    """
    Gera um conjunto com todas as diagonais de um polígono
    Essa função é eficiente, não gera nenhuma possibilidade a mais
    """
    diagonais = set()
    for fim in range(2, vertices - 1):
        diagonais.add(frozenset([0 , fim]))
    for inicio in range(1, vertices - 2):
        for fim in range(inicio + 2, vertices):
            diagonais.add(frozenset([inicio, fim]))
    return diagonais

def DiagonaisEmCiclos(quantidadeVertices):
    """
    Gera todas as diagonais por ciclos, cada ciclo tem um intervalo diferente
    {2: {0: [0, 2, 4, 0], 1: [1, 3, 5, 1]}, 3: {0: [0, 3], 1: [1, 4], 2: [2, 5]}}
    """
    diagonais = {}
    #são necessarios ciclos de dois até diagonal divido por dois
    for gerador in range(2, int(quantidadeVertices / 2) + 1):
        diagonais.setdefault(gerador, {})
        #cada ciclo vai aparecer mdc de vertices e gerador vezes, cada vez começando de inicio mais um
        for rotacao in range(gcd(quantidadeVertices, gerador)):
            ciclo = []
            #incide de cada numero no ciclo
            for indiceciclo in range(0 , int(quantidadeVertices / gcd(quantidadeVertices, gerador))):
                #operacao para ter o intervalo certo entre os numeros
                ciclo.append((rotacao + (indiceciclo * gerador)) % quantidadeVertices)
            if len(ciclo) > 2:
                #qualquer ciclo maior que dois vai terminar onde comecou
                #tamanho dois voltar para o inicio seria uma repetição da diagonal
                ciclo.append(rotacao)
            diagonais[gerador].setdefault(rotacao, ciclo)
    return diagonais

def DiagonaisRepetidasParaGrafoCaminhavel(vertices):
    """
    gera um dicionario com as diagonais que devem ser repetidas para tornar o grafo das diagonais de um polígono par caminhável
    inicio do caminho é sempre zero e no dicionario existem os fins até metade da quantidade de vértices, o que cobre todas as simetrias
    """
    finsErepeticoes = {}
    listateste = []
    #as diagonais repetidas são um subconjunto das permutações dos vértices menos o de inicio e o de fim
    for fim in range(1, int(vertices / 2) + 1):
        #gera lista com os vertices menos o de inicio e o de fim
        verticeslistados = [i for i in range(vertices) if i != 0 and i != fim]
        #gera permutações dessa lista e guarda somente as que começam no primeiro vertice
        verticesPerm = [i for i in perm(verticeslistados) if i[0] == verticeslistados[0]]

        #as permutações que formam as diagonais repetidas são as em ordem crescente a cada dois e sem sequenciais a cada um
        RepetiçõesInicioFim = []
        for permutacao in verticesPerm:
            DoisEmDois = []
            for i in range(0, len(verticeslistados) - 1, 2):
                #se contém numeros sequencias ou se os primeiros de cada dupla não estão em ordem crescente encerra
                if permutacao[i + 1] <= permutacao[i] + 1 or (i > 1 and permutacao[i - 2] > permutacao[i]):
                    break
                #divide as permutações em listas de dois em dois números
                DoisEmDois.append(permutacao[i: i + 2])
            else:
                #só acrescenta se todos os numeros da permutação atenderem aos critérios
                RepetiçõesInicioFim.append(DoisEmDois)
        #acrescenta a um dicionario, a chave é a diagonal de fim, a de inicio é sempre 0
        finsErepeticoes.update({fim: RepetiçõesInicioFim})
    return finsErepeticoes


def GrafoVerticesEDiagonais(quantidadeVertices):
    """
    Gera um grafo mostrando para cada vertices com quais outros vertices ele pode ser ligado para formar uma diagonal
    """
    grafo = []
    for vertice in range(quantidadeVertices):
        diagonaisDoVertices = []
        for diagonal in range(vertice + 2, vertice + 2 + quantidadeVertices - 3):
            diagonaisDoVertices += [diagonal % quantidadeVertices]
        grafo += [diagonaisDoVertices]
    return grafo

def GrafoCaminhosAleatorios(graph, diagonais, depth, depthcount=0, node=0, path=[0]):
    """
    Aleatoriamente encontra caminhos no grafo que passam por todas as diagonais pelo uma vez
    São possíveis cíclos de 3 nodes, mas não 2
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

vertices = 8
depth = 50
maxfails = 5000000
diagonais = Diagonais(vertices)
grafo = GrafoPoligonos(vertices)
GrafosCaminhaveisPoligonos(vertices, diagonais)


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