from itertools import permutations as perm

def RepeticoesGrafosCaminhaveis(vertices):
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

def PossiveisRepeticoes(vertices):
    
    for fim in range(1, int(vertices / 2) + 1):
        verticeslistados = [i for i in range(vertices) if i != 0 and i != fim]
        repeticoes = []
        for i, j in enumerate(verticeslistados[:-2]):
            lista = []
            for k in verticeslistados[i+2:]:
                lista.append([j, k])
            if lista:
                repeticoes.append(lista)
        
        PesquisandoPossiveisRepeticoes(repeticoes)

listarepeticoes = []
jaforam = []
def PesquisandoPossiveisRepeticoes(repeticoes):
    global listarepeticoes, jaforam
    if len(listarepeticoes) == 3:
        print(listarepeticoes)
        jaforam.pop(len(jaforam)-1)
        jaforam.pop(len(jaforam)-1)
        listarepeticoes = listarepeticoes[:-1]
        return
    if repeticoes == []:
        
        return
  
    for i in repeticoes[0]:
        for j in i:
            if j in jaforam:
                break
        else:
            listarepeticoes.append(i)
            for j in i:
                jaforam.append(j)
        PesquisandoPossiveisRepeticoes(repeticoes[1:])


RepeticoesGrafosCaminhaveis(6)