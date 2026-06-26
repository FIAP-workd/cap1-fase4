# ===================================================================
# SEÇÃO 0 — CABEÇALHO E IMPORTS
# ===================================================================
"""
SIGIC - Sistema Inteligente de Gerenciamento da Infraestrutura da Colônia
Base Marciana Aurora Siger

Este arquivo autossuficiente implementa a gestão de uma base marciana fictícia
utilizando conceitos de grafos, algoritmos de busca, modelagem matemática de
perda de energia e indicadores de sustentabilidade.
"""

import math
import copy


# ===================================================================
# SEÇÃO 1 — DADOS DOS MÓDULOS
# ===================================================================
# Dicionário principal dos módulos da base, indexado por ID numérico.
MODULOS: dict[int, dict] = {
    1: {
        "nome": "Habitação",
        "tipo": "sobrevivencia",
        "consumo_energetico": 150,   # kWh
        "prioridade": 1,             # 1 = mais crítico
        "capacidade_armazenamento": 300,  # kWh
        "necessidade_comunicacao": 7,     # 0 a 10
        "status": "ativo",
        "x": 10.0,
        "y": 20.0,
    },
    2: {
        "nome": "Centro de Controle",
        "tipo": "gerenciamento",
        "consumo_energetico": 200,
        "prioridade": 1,
        "capacidade_armazenamento": 100,
        "necessidade_comunicacao": 10,
        "status": "ativo",
        "x": 30.0,
        "y": 40.0,
    },
    3: {
        "nome": "Armazenamento de Energia",
        "tipo": "energia",
        "consumo_energetico": 50,
        "prioridade": 2,
        "capacidade_armazenamento": 2000,
        "necessidade_comunicacao": 5,
        "status": "ativo",
        "x": 60.0,
        "y": 35.0,
    },
    4: {
        "nome": "Agricultura",
        "tipo": "sustentabilidade",
        "consumo_energetico": 180,
        "prioridade": 3,
        "capacidade_armazenamento": 400,
        "necessidade_comunicacao": 4,
        "status": "ativo",
        "x": 80.0,
        "y": 70.0,
    },
    5: {
        "nome": "Laboratório Científico",
        "tipo": "pesquisa",
        "consumo_energetico": 250,
        "prioridade": 4,
        "capacidade_armazenamento": 200,
        "necessidade_comunicacao": 8,
        "status": "ativo",
        "x": 120.0,
        "y": 90.0,
    },
    6: {
        "nome": "Comunicação",
        "tipo": "comunicacao",
        "consumo_energetico": 120,
        "prioridade": 2,
        "capacidade_armazenamento": 80,
        "necessidade_comunicacao": 10,
        "status": "ativo",
        "x": 50.0,
        "y": 10.0,
    },
    7: {
        "nome": "Suporte Médico",
        "tipo": "saude",
        "consumo_energetico": 100,
        "prioridade": 1,
        "capacidade_armazenamento": 150,
        "necessidade_comunicacao": 6,
        "status": "ativo",
        "x": 100.0,
        "y": 30.0,
    },
    8: {
        "nome": "Produção de Oxigênio",
        "tipo": "suporte_vital",
        "consumo_energetico": 90,
        "prioridade": 1,
        "capacidade_armazenamento": 500,
        "necessidade_comunicacao": 5,
        "status": "ativo",
        "x": 130.0,
        "y": 15.0,
    },
}

# Tupla imutável com informações básicas de cada módulo para referência rápida.
INFO_MODULOS: tuple[tuple[int, str, str, int], ...] = (
    (1, "Habitação", "sobrevivencia", 1),
    (2, "Centro de Controle", "gerenciamento", 1),
    (3, "Armazenamento de Energia", "energia", 2),
    (4, "Agricultura", "sustentabilidade", 3),
    (5, "Laboratório Científico", "pesquisa", 4),
    (6, "Comunicação", "comunicacao", 2),
    (7, "Suporte Médico", "saude", 1),
    (8, "Produção de Oxigênio", "suporte_vital", 1),
)


# ===================================================================
# SEÇÃO 2 — DADOS DAS CONEXÕES
# ===================================================================
# Conexões físicas entre os módulos: (origem, destino, distância em metros).
# Grafo conexo: todos os módulos são alcançáveis a partir de qualquer outro.
CONEXOES: list[tuple[int, int, float]] = [
    (1, 2, 50.0),
    (1, 6, 20.0),
    (2, 3, 30.0),
    (2, 4, 80.0),
    (3, 6, 30.0),
    (4, 5, 60.0),
    (5, 7, 40.0),
    (6, 7, 40.0),
    (6, 8, 25.0),
    (7, 8, 35.0),
]

# Constantes para modelagem de perda de energia ao longo dos cabos.
ALPHA: float = 0.005       # Coeficiente de perda do material (1/m)
P0: float = 100.0            # Potência inicial em kWh

# Valor representando infinito para algoritmos de grafos.
INF = float("inf")


# ===================================================================
# SEÇÃO 3 — FUNÇÕES DA REDE (GRAFO)
# ===================================================================

def inicializar_rede() -> tuple[list[list[float]], dict[int, list[tuple[int, float]]]]:
    """
    Constrói a representação do grafo da base marciana.

    Retorna:
        - matriz_adj: matriz NxN de adjacência com pesos (INF quando não conectado).
        - lista_adj: dicionário com listas de tuplas (vizinho, peso) para cada módulo.
    """
    total = len(MODULOS)
    ids = sorted(MODULOS.keys())
    # Inicializa a matriz com INF e 0 na diagonal.
    matriz_adj = [[0.0 if i == j else INF for j in range(total)] for i in range(total)]
    lista_adj: dict[int, list[tuple[int, float]]] = {id_mod: [] for id_mod in ids}

    # Preenche com as conexões fornecidas (grafo não direcionado).
    for origem, destino, distancia in CONEXOES:
        i = ids.index(origem)
        j = ids.index(destino)
        matriz_adj[i][j] = distancia
        matriz_adj[j][i] = distancia
        lista_adj[origem].append((destino, distancia))
        lista_adj[destino].append((origem, distancia))

    # Ordena vizinhos para exibição determinística.
    for id_mod in lista_adj:
        lista_adj[id_mod].sort(key=lambda x: x[0])

    return matriz_adj, lista_adj


def exibir_matriz(matriz: list[list[float]], usar_modulos: bool = True) -> None:
    """
    Exibe a matriz de adjacência formatada, opcionalmente com nomes dos módulos.
    """
    ids = sorted(MODULOS.keys())
    n = len(ids)
    # Calcula largura máxima para alinhamento.
    max_nome = max(len(MODULOS[mid]["nome"]) for mid in ids)
    largura = max(max_nome, 10)

    # Cabeçalho com IDs e nomes.
    if usar_modulos:
        print(" " * (largura + 3), end="")
        for mid in ids:
            print(f"{MODULOS[mid]['nome'][:largura]:^{largura}} ", end="")
        print()
        print(" " * (largura + 3), end="")
        for mid in ids:
            print(f"{'(ID ' + str(mid) + ')':^{largura}} ", end="")
        print()

    # Linhas da matriz.
    for i, mid in enumerate(ids):
        if usar_modulos:
            label = f"{MODULOS[mid]['nome'][:largura]}({mid})"
            print(f"{label:<{largura + 3}}", end="")
        else:
            print(f"{mid:>{largura + 3}}", end="")
        for j in range(n):
            valor = matriz[i][j]
            if valor == INF:
                celula = " ∞ "
            elif i == j:
                celula = " 0 "
            else:
                celula = f"{valor:>6.2f}"
            print(f"{celula:^{largura}} ", end="")
        print()


def exibir_lista_adj(lista_adj: dict[int, list[tuple[int, float]]]) -> None:
    """
    Exibe a lista de adjacência de forma legível.
    """
    for id_mod in sorted(lista_adj.keys()):
        nome = MODULOS[id_mod]["nome"]
        vizinhos = lista_adj[id_mod]
        if vizinhos:
            lista_str = ", ".join([f"({v}, {p:.1f}m)" for v, p in vizinhos])
        else:
            lista_str = "sem conexões"
        print(f"  {id_mod:>2} - {nome:<30} → [{lista_str}]")


def consultar_modulo(id_ou_nome: int | str) -> dict | None:
    """
    Consulta um módulo por ID numérico ou por nome (parcial/minúsculo).
    Retorna o dicionário do módulo ou None.
    """
    if isinstance(id_ou_nome, int) and id_ou_nome in MODULOS:
        return MODULOS[id_ou_nome]

    if isinstance(id_ou_nome, str):
        termo = id_ou_nome.lower()
        for mid, dados in MODULOS.items():
            if termo in dados["nome"].lower():
                return dados
    return None


def listar_modulos() -> float:
    """
    Lista todos os módulos em uma tabela formatada e retorna o consumo total.
    """
    print(f"{'ID':>4} | {'Nome':<30} | {'Status':<10} | {'Consumo (kWh)':>14} | {'Prioridade':>10}")
    print("-" * 80)
    consumo_total = 0.0
    for mid in sorted(MODULOS.keys()):
        dados = MODULOS[mid]
        print(
            f"{mid:>4} | {dados['nome']:<30} | {dados['status']:<10} | "
            f"{dados['consumo_energetico']:>14.1f} | {dados['prioridade']:>10}"
        )
        consumo_total += dados["consumo_energetico"]
    print("-" * 80)
    print(f"{'Consumo total da base:':>58} {consumo_total:>14.1f} kWh")
    return consumo_total


# ===================================================================
# SEÇÃO 4 — ALGORITMOS DE REDES
# ===================================================================

def bfs(origem_id: int, lista_adj: dict[int, list[tuple[int, float]]]) -> tuple[list[int], dict[int, int], dict[int, list[int]]]:
    """
    Realiza busca em largura (BFS) a partir de origem_id.

    Retorna:
        - visitados: lista de IDs na ordem de visita.
        - distancias: dicionário id -> distância em número de saltos.
        - niveis: dicionário distância -> lista de IDs naquele nível.
    """
    fila: list[int] = [origem_id]
    visitados: list[int] = []
    distancias: dict[int, int] = {origem_id: 0}
    niveis: dict[int, list[int]] = {0: [origem_id]}

    while fila:
        atual = fila.pop(0)
        if atual in visitados:
            continue
        visitados.append(atual)
        for vizinho, _ in lista_adj.get(atual, []):
            if vizinho not in distancias:
                distancias[vizinho] = distancias[atual] + 1
                fila.append(vizinho)
                niveis.setdefault(distancias[vizinho], []).append(vizinho)

    return visitados, distancias, niveis


def dfs(origem_id: int, lista_adj: dict[int, list[tuple[int, float]]]) -> list[int]:
    """
    Realiza busca em profundidade (DFS) a partir de origem_id.
    Retorna a lista de IDs na ordem de visita.
    """
    pilha: list[int] = [origem_id]
    visitados: list[int] = []

    while pilha:
        atual = pilha.pop()
        if atual in visitados:
            continue
        visitados.append(atual)
        for vizinho, _ in reversed(lista_adj.get(atual, [])):
            if vizinho not in visitados:
                pilha.append(vizinho)

    return visitados


def dijkstra(origem_id: int, destino_id: int, lista_adj: dict[int, list[tuple[int, float]]]) -> tuple[list[int] | None, float]:
    """
    Executa o algoritmo de Dijkstra para encontrar o menor caminho entre dois módulos.

    Retorna:
        - caminho: lista de IDs do caminho (incluindo origem e destino) ou None.
        - custo_total: distância total do caminho (INF se não houver caminho).
    """
    ids = sorted(MODULOS.keys())
    distancias: dict[int, float] = {mid: INF for mid in ids}
    anteriores: dict[int, int | None] = {mid: None for mid in ids}
    nao_visitados: set[int] = set(ids)

    distancias[origem_id] = 0.0

    while nao_visitados:
        # Seleciona o nó não visitado com menor distância atual.
        atual = min(nao_visitados, key=lambda x: distancias[x])
        if distancias[atual] == INF:
            break
        nao_visitados.remove(atual)

        for vizinho, peso in lista_adj.get(atual, []):
            if vizinho in nao_visitados:
                nova_dist = distancias[atual] + peso
                if nova_dist < distancias[vizinho]:
                    distancias[vizinho] = nova_dist
                    anteriores[vizinho] = atual

    if distancias[destino_id] == INF:
        return None, INF

    # Reconstrói o caminho.
    caminho: list[int] = []
    passo: int | None = destino_id
    while passo is not None:
        caminho.append(passo)
        passo = anteriores[passo]
    caminho.reverse()
    return caminho, distancias[destino_id]


def detectar_pontes(lista_adj: dict[int, list[tuple[int, float]]], total_modulos: int) -> list[tuple[int, int]]:
    """
    Detecta pontes no grafo usando o algoritmo de Tarjan.

    Uma ponte é uma aresta cuja remoção aumenta o número de componentes conexos.
    """
    ids = sorted(MODULOS.keys())
    adj: dict[int, list[int]] = {mid: [v for v, _ in lista_adj.get(mid, [])] for mid in ids}

    descoberta: dict[int, int] = {}
    low: dict[int, int] = {}
    visitado: set[int] = set()
    pontes: list[tuple[int, int]] = []
    tempo = 0

    def tarjan(u: int, pai: int | None) -> None:
        nonlocal tempo
        tempo += 1
        descoberta[u] = tempo
        low[u] = tempo
        visitado.add(u)

        for v in adj[u]:
            if v == pai:
                continue
            if v not in visitado:
                tarjan(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > descoberta[u]:
                    # Garante ordenação para evitar duplicatas.
                    pontes.append(tuple(sorted((u, v))))  # type: ignore
            else:
                low[u] = min(low[u], descoberta[v])

    for mid in ids:
        if mid not in visitado:
            tarjan(mid, None)

    pontes.sort()
    return pontes


# ===================================================================
# SEÇÃO 5 — SIMULAÇÕES
# ===================================================================

def simular_falha_modulo(id_modulo: int, matriz_adj: list[list[float]], lista_adj: dict[int, list[tuple[int, float]]]) -> dict:
    """
    Simula a falha de um módulo: desativa conexões, verifica conectividade e
    recalcula rotas alternativas para módulos críticos (prioridade 1).

    Todos os dados são restaurados ao final.
    """
    if id_modulo not in MODULOS:
        return {"erro": f"Módulo {id_modulo} não existe."}

    # Backup profundo dos dados originais.
    matriz_original = copy.deepcopy(matriz_adj)
    lista_original = copy.deepcopy(lista_adj)
    status_original = MODULOS[id_modulo]["status"]

    nome = MODULOS[id_modulo]["nome"]
    MODULOS[id_modulo]["status"] = "alerta"

    ids = sorted(MODULOS.keys())
    idx = ids.index(id_modulo)

    # Remove conexões incidentes ao módulo falho.
    for vizinho, _ in lista_adj.get(id_modulo, [])[:]:  # cópia para iterar seguro
        j = ids.index(vizinho)
        matriz_adj[idx][j] = INF
        matriz_adj[j][idx] = INF
        lista_adj[vizinho] = [(v, p) for v, p in lista_adj[vizinho] if v != id_modulo]
    lista_adj[id_modulo] = []

    print(f"\n\033[1m\033[33m[FALHA SIMULADA]\033[0m Módulo {id_modulo} ({nome}) está em ALERTA.")
    print("Conexões incidentes foram removidas temporariamente.\n")

    # Testa conectividade com BFS a partir de um módulo ativo qualquer.
    origem_teste = ids[0] if ids[0] != id_modulo else ids[1]
    visitados, distancias, niveis = bfs(origem_teste, lista_adj)
    atingidos = set(visitados)
    isolados = [mid for mid in ids if mid != id_modulo and mid not in atingidos]

    print(f"Conectividade após falha (BFS a partir de {MODULOS[origem_teste]['nome']}):")
    print(f"  Módulos alcançados: {len(visitados)} de {len(ids) - 1} (excluindo o falho)")
    if isolados:
        print(f"  ⚠️ Módulos isolados: {isolados}")
    else:
        print("  ✅ Todos os demais módulos permanecem conectados.")

    # Recalcula Dijkstra para módulos críticos (prioridade 1).
    criticos = [mid for mid in ids if MODULOS[mid]["prioridade"] == 1 and mid != id_modulo]
    print(f"\nRotas alternativas para módulos críticos a partir de {MODULOS[origem_teste]['nome']}:")
    rotas: list[tuple[int, list[int] | None, float]] = []
    for destino in criticos:
        caminho, custo = dijkstra(origem_teste, destino, lista_adj)
        rotas.append((destino, caminho, custo))
        if caminho:
            nomes_caminho = " → ".join([MODULOS[m]["nome"] for m in caminho])
            print(f"  {MODULOS[origem_teste]['nome']} → {MODULOS[destino]['nome']}: {nomes_caminho} | Custo: {custo:.2f}m")
        else:
            print(f"  {MODULOS[origem_teste]['nome']} → {MODULOS[destino]['nome']}: ❌ SEM ROTA")

    # Restaura os dados originais.
    matriz_adj[:] = matriz_original
    lista_adj.clear()
    lista_adj.update(lista_original)
    MODULOS[id_modulo]["status"] = status_original

    print("\n\033[1m\033[33m[RESTAURAÇÃO]\033[0m Todos os dados da rede foram restaurados.")

    return {
        "modulo_falho": id_modulo,
        "modulos_isolados": isolados,
        "rotas_para_criticos": rotas,
    }


def simular_falha_conexao(origem: int, destino: int, matriz_adj: list[list[float]], lista_adj: dict[int, list[tuple[int, float]]]) -> dict:
    """
    Simula a falha de uma conexão específica, recalcula a rota alternativa
    e compara com o custo original.
    """
    if origem not in MODULOS or destino not in MODULOS:
        return {"erro": "IDs de origem/destino inválidos."}

    ids = sorted(MODULOS.keys())
    i = ids.index(origem)
    j = ids.index(destino)

    # Backup.
    matriz_original = copy.deepcopy(matriz_adj)
    lista_original = copy.deepcopy(lista_adj)

    peso_original = matriz_adj[i][j]
    if peso_original == INF:
        return {"erro": f"Não existe conexão direta entre {origem} e {destino}."}

    # Rota original.
    caminho_original, custo_original = dijkstra(origem, destino, lista_adj)

    # Remove a aresta.
    matriz_adj[i][j] = INF
    matriz_adj[j][i] = INF
    lista_adj[origem] = [(v, p) for v, p in lista_adj[origem] if v != destino]
    lista_adj[destino] = [(v, p) for v, p in lista_adj[destino] if v != origem]

    print(f"\n\033[1m\033[33m[FALHA DE CONEXÃO]\033[0m Entre {MODULOS[origem]['nome']} e {MODULOS[destino]['nome']}.")
    print(f"Distância original da conexão: {peso_original:.2f}m\n")

    caminho_alternativo, custo_alternativo = dijkstra(origem, destino, lista_adj)

    if caminho_original:
        nomes_original = " → ".join([MODULOS[m]["nome"] for m in caminho_original])
        print(f"Rota original: {nomes_original} | Custo: {custo_original:.2f}m")
    else:
        print("Rota original: não disponível")

    if caminho_alternativo:
        nomes_alternativo = " → ".join([MODULOS[m]["nome"] for m in caminho_alternativo])
        print(f"Rota alternativa: {nomes_alternativo} | Custo: {custo_alternativo:.2f}m")
        impacto = ((custo_alternativo - custo_original) / custo_original) * 100 if custo_original > 0 else 0.0
        print(f"Impacto percentual no custo: {impacto:+.2f}%")
    else:
        print("Rota alternativa: ❌ NÃO EXISTE — grafo desconectado!")
        custo_alternativo = INF
        impacto = INF

    # Restaura.
    matriz_adj[:] = matriz_original
    lista_adj.clear()
    lista_adj.update(lista_original)

    print("\n\033[1m\033[33m[RESTAURAÇÃO]\033[0m Conexão restaurada.")

    return {
        "origem": origem,
        "destino": destino,
        "custo_original": custo_original,
        "custo_alternativo": custo_alternativo,
        "impacto_percentual": impacto,
    }


def simular_sobrecarga(id_modulo: int, matriz_adj: list[list[float]], lista_adj: dict[int, list[tuple[int, float]]]) -> dict:
    """
    Simula o aumento de 50% no consumo de um módulo e avalia a sobrecarga da rede.
    """
    if id_modulo not in MODULOS:
        return {"erro": f"Módulo {id_modulo} não existe."}

    consumo_original = MODULOS[id_modulo]["consumo_energetico"]
    consumo_simulado = consumo_original * 1.5

    consumo_total_original = sum(MODULOS[m]["consumo_energetico"] for m in MODULOS)
    capacidade_total = sum(MODULOS[m]["capacidade_armazenamento"] for m in MODULOS)

    consumo_total_simulado = consumo_total_original - consumo_original + consumo_simulado

    print(f"\n\033[1m\033[33m[SOBRECARGA SIMULADA]\033[0m Módulo {id_modulo} ({MODULOS[id_modulo]['nome']})")
    print(f"Consumo original: {consumo_original:.1f} kWh")
    print(f"Consumo após aumento de 50%: {consumo_simulado:.1f} kWh")
    print(f"\nConsumo total da base: {consumo_total_original:.1f} → {consumo_total_simulado:.1f} kWh")
    print(f"Capacidade total de armazenamento: {capacidade_total:.1f} kWh")

    taxa_original = (consumo_total_original / capacidade_total) * 100
    taxa_simulada = (consumo_total_simulado / capacidade_total) * 100
    print(f"Taxa de utilização: {taxa_original:.2f}% → {taxa_simulada:.2f}%")

    if taxa_simulada > 100:
        print("⚠️ ESTADO CRÍTICO: consumo ultrapassa a capacidade total de armazenamento!")
    elif taxa_simulada > 80:
        print("⚠️ ALERTA: rede próxima da sobrecarga.")
    else:
        print("✅ Rede dentro da capacidade de armazenamento.")

    return {
        "modulo": id_modulo,
        "consumo_original": consumo_original,
        "consumo_simulado": consumo_simulado,
        "consumo_total_original": consumo_total_original,
        "consumo_total_simulado": consumo_total_simulado,
        "taxa_utilizacao": taxa_simulada,
    }


# ===================================================================
# SEÇÃO 6 — MODELAGEM MATEMÁTICA
# ===================================================================

def modelagem_perda_energetica(conexoes: list[tuple[int, int, float]]) -> dict:
    """
    Modela a perda de energia ao longo das conexões da base.

    Fórmula: P(l) = P0 * exp(-alpha * l)
    Onde:
        P0 = potência inicial (kWh)
        alpha = coeficiente de perda do material (1/m)
        l = distância da conexão (m)
        P(l) = potência final após a perda
    """
    print("\n\033[1mModelagem Matemática de Perda de Energia\033[0m")
    print("Fórmula: P(l) = P0 * e^(-alpha * l)")
    print(f"  P0    = {P0} kWh    (potência inicial)")
    print(f"  alpha = {ALPHA} 1/m  (coeficiente de perda do material)")
    print("  l     = distância da conexão em metros")
    print("  P(l)  = potência final após perda ao longo do cabo\n")

    # Tabela compacta para não quebrar no terminal durante a apresentação.
    print(f"{'Conexão':<10} | {'Dist.(m)':>8} | {'Perda %':>8} | {'Final kWh':>10}")
    print("-" * 47)
    perda_total = 0.0
    resultados = []
    legendas = []
    for origem, destino, distancia in conexoes:
        nome_origem = MODULOS[origem]["nome"]
        nome_destino = MODULOS[destino]["nome"]
        potencia_final = P0 * math.exp(-ALPHA * distancia)
        perda_percentual = ((P0 - potencia_final) / P0) * 100
        perda_total += perda_percentual
        resultados.append((origem, destino, distancia, perda_percentual, potencia_final))
        legendas.append((origem, destino, nome_origem, nome_destino))
        print(
            f"{origem:>2} -> {destino:<4} | {distancia:>8.2f} | "
            f"{perda_percentual:>8.2f} | {potencia_final:>10.4f}"
        )

    print("-" * 47)
    print(f"Perda total acumulada na rede: {perda_total:.2f}%")

    print("\nLegenda das conexões:")
    for origem, destino, nome_origem, nome_destino in legendas:
        print(f"  {origem} -> {destino}: {nome_origem} -> {nome_destino}")

    print("\nAnálise qualitativa:")
    print("  A função P(l) = P0 * e^(-alpha * l) é uma exponencial decrescente.")
    print("  Quanto maior a distância, maior a perda de energia.")
    print("  Quando l → ∞, P(l) tende assintoticamente a 0, indicando que")
    print("  conexões muito longas desperdiçam energia.\n")

    # Simulação de otimização: reduzir alpha para 0.003.
    alpha_otimizado = 0.003
    print(f"Otimização: reduzindo alpha de {ALPHA} para {alpha_otimizado}:")
    perda_otimizada_total = 0.0
    for origem, destino, distancia in conexoes:
        pot_final_otim = P0 * math.exp(-alpha_otimizado * distancia)
        perda_otim = ((P0 - pot_final_otim) / P0) * 100
        perda_otimizada_total += perda_otim
    ganho = perda_total - perda_otimizada_total
    print(f"  Perda total atual:    {perda_total:.2f}%")
    print(f"  Perda total otimizada: {perda_otimizada_total:.2f}%")
    print(f"  Ganho estimado:       {ganho:.2f}%")
    print("  Ponto ótimo: minimizar a distância total da rede e usar materiais")
    print("  condutores com menor coeficiente de perda.\n")

    return {
        "perda_total": perda_total,
        "perda_otimizada_total": perda_otimizada_total,
        "ganho": ganho,
        "resultados": resultados,
    }


# ===================================================================
# SEÇÃO 7 — SUSTENTABILIDADE E GOVERNANÇA
# ===================================================================

def relatorio_sustentabilidade(modulos: dict[int, dict], matriz_adj: list[list[float]], lista_adj: dict[int, list[tuple[int, float]]], conexoes: list[tuple[int, int, float]]) -> dict:
    """
    Gera um relatório completo de sustentabilidade e governança tecnológica da base.
    """
    consumo_total = sum(m["consumo_energetico"] for m in modulos.values())
    capacidade_total = sum(m["capacidade_armazenamento"] for m in modulos.values())
    modulos_criticos = [m for m in modulos if modulos[m]["prioridade"] == 1]

    # Eficiência média com base na modelagem de perda.
    perda_total = sum(
        ((P0 - P0 * math.exp(-ALPHA * dist)) / P0) * 100
        for _, _, dist in conexoes
    )
    eficiencia_media = max(0.0, 100.0 - (perda_total / len(conexoes)))

    # Rota mais longa e mais curta entre todos os pares (Dijkstra).
    ids = sorted(modulos.keys())
    rota_mais_curta: tuple[list[int], float] = ([], INF)
    rota_mais_longa: tuple[list[int], float] = ([], 0.0)
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            caminho, custo = dijkstra(ids[i], ids[j], lista_adj)
            if caminho is not None:
                if custo < rota_mais_curta[1]:
                    rota_mais_curta = (caminho, custo)
                if custo > rota_mais_longa[1]:
                    rota_mais_longa = (caminho, custo)

    print("\n" + "=" * 70)
    print("          📊 RELATÓRIO DE SUSTENTABILIDADE — AURORA SIGER")
    print("=" * 70)

    print("\n📊 CONSUMO ENERGÉTICO")
    print(f"  Consumo total da base:     {consumo_total:.2f} kWh")
    print(f"  Capacidade total:          {capacidade_total:.2f} kWh")
    print(f"  Taxa de utilização:        {(consumo_total / capacidade_total) * 100:.2f}%")

    print("\n🎯 EFICIÊNCIA DA REDE")
    print(f"  Eficiência média estimada: {eficiencia_media:.2f}%")
    print(f"  Perda média por conexão:   {perda_total / len(conexoes):.2f}%")

    print("\n⚠️ PONTOS CRÍTICOS")
    print(f"  Módulos de prioridade 1: {len(modulos_criticos)}")
    for mid in modulos_criticos:
        print(f"    - {modulos[mid]['nome']} (ID {mid})")
    pontes = detectar_pontes(lista_adj, len(modulos))
    if pontes:
        print(f"  Pontes detectadas na rede: {len(pontes)}")
        for u, v in pontes:
            print(f"    - {modulos[u]['nome']} ↔ {modulos[v]['nome']}")
    else:
        print("  ✅ Nenhuma ponte detectada — rede robusta.")

    if rota_mais_curta[0]:
        nomes_curta = " → ".join([modulos[m]["nome"] for m in rota_mais_curta[0]])
        print(f"\n  Rota mais curta: {nomes_curta} ({rota_mais_curta[1]:.2f}m)")
    if rota_mais_longa[0]:
        nomes_longa = " → ".join([modulos[m]["nome"] for m in rota_mais_longa[0]])
        print(f"  Rota mais longa: {nomes_longa} ({rota_mais_longa[1]:.2f}m)")

    print("\n💡 PROPOSTAS DE MELHORIA")
    print("  1. Reduzir distâncias entre módulos críticos para minimizar perdas.")
    print("  2. Utilizar materiais supercondutores ou de baixa resistência em Marte.")
    print("  3. Adicionar redundância de conexões em torno das pontes detectadas.")
    print("  4. Implementar gerenciamento dinâmico de carga baseado em prioridades.")

    print("\n🏛️ GOVERNANÇA TECNOLÓGICA")
    print("  - Todos os módulos críticos devem possuir rotas alternativas.")
    print("  - Decisões de desligamento seguem a prioridade 1 > 2 > 3 > 4 > 5.")
    print("  - Alterações na topologia da rede exigem aprovação do Centro de Controle.")
    print("  - Dados de consumo e eficiência devem ser auditados periodicamente.")

    print("=" * 70 + "\n")

    return {
        "consumo_total": consumo_total,
        "capacidade_total": capacidade_total,
        "eficiencia_media": eficiencia_media,
        "modulos_criticos": modulos_criticos,
        "pontes": pontes,
        "rota_mais_curta": rota_mais_curta,
        "rota_mais_longa": rota_mais_longa,
    }


# ===================================================================
# SEÇÃO 8 — FUNÇÕES DE INTERFACE (MENU)
# ===================================================================

def limpar_tela() -> None:
    """
    Simula a limpeza da tela com algumas quebras de linha.
    """
    print("\n" * 2)


def exibir_menu() -> None:
    """
    Exibe o menu principal do sistema SIGIC.
    """
    print("\n\033[1m=== SIGIC — SISTEMA INTELIGENTE DE GERENCIAMENTO DA INFRAESTRUTURA DA COLÔNIA ===\033[0m")
    print("\033[33mBase Marciana Aurora Siger\033[0m\n")
    print("  1 - Listar módulos da base")
    print("  2 - Consultar módulo")
    print("  3 - Exibir matriz de adjacência")
    print("  4 - Exibir lista de adjacência")
    print("  5 - Algoritmos de rede (BFS / DFS / Dijkstra / Pontes)")
    print("  6 - Simulações de falha e sobrecarga")
    print("  7 - Modelagem matemática de perda de energia")
    print("  8 - Relatório de sustentabilidade e governança")
    print("  9 - Limpar tela")
    print("  0 - Sair do sistema")
    print("-" * 50)


def submenu_simulacoes() -> None:
    """
    Exibe o submenu de simulações do sistema.
    """
    print("\n\033[1m=== SUBMENU DE SIMULAÇÕES ===\033[0m")
    print("  1 - Simular falha de módulo")
    print("  2 - Simular falha de conexão")
    print("  3 - Simular sobrecarga de módulo")
    print("  4 - Simular falha em todas as pontes (uma a uma)")
    print("  0 - Voltar ao menu principal")
    print("-" * 40)


def aguardar_enter() -> None:
    """
    Pausa a execução até que o usuário pressione ENTER.
    """
    input("\nPressione ENTER para continuar...")


def menu_algoritmos(lista_adj: dict[int, list[tuple[int, float]]]) -> None:
    """
    Executa o submenu de algoritmos de rede com entrada do usuário.
    """
    while True:
        print("\n\033[1m=== ALGORITMOS DE REDE ===\033[0m")
        print("  1 - Busca em Largura (BFS)")
        print("  2 - Busca em Profundidade (DFS)")
        print("  3 - Menor caminho (Dijkstra)")
        print("  4 - Detectar pontes (Tarjan)")
        print("  0 - Voltar")
        print("-" * 35)
        opcao = input("Escolha: ").strip()

        if opcao == "0":
            break
        elif opcao == "1":
            try:
                origem = int(input("ID de origem: "))
                visitados, distancias, niveis = bfs(origem, lista_adj)
                print(f"\nBFS a partir de {MODULOS[origem]['nome']}:")
                print(f"  Ordem de visita: {visitados}")
                print(f"  Distâncias (saltos): {distancias}")
                print(f"  Níveis: {niveis}")
            except (ValueError, KeyError):
                print("Entrada inválida.")
        elif opcao == "2":
            try:
                origem = int(input("ID de origem: "))
                visitados = dfs(origem, lista_adj)
                print(f"\nDFS a partir de {MODULOS[origem]['nome']}:")
                print(f"  Ordem de visita: {visitados}")
            except (ValueError, KeyError):
                print("Entrada inválida.")
        elif opcao == "3":
            try:
                origem = int(input("ID de origem: "))
                destino = int(input("ID de destino: "))
                caminho, custo = dijkstra(origem, destino, lista_adj)
                if caminho:
                    nomes = " → ".join([MODULOS[m]["nome"] for m in caminho])
                    print(f"\nMenor caminho: {nomes}")
                    print(f"Distância total: {custo:.2f}m")
                else:
                    print("Não existe caminho entre os módulos.")
            except (ValueError, KeyError):
                print("Entrada inválida.")
        elif opcao == "4":
            pontes = detectar_pontes(lista_adj, len(MODULOS))
            if pontes:
                print("\nPontes detectadas:")
                for u, v in pontes:
                    print(f"  {MODULOS[u]['nome']} ↔ {MODULOS[v]['nome']}")
            else:
                print("\nNenhuma ponte detectada.")
        else:
            print("Opção inválida.")
        aguardar_enter()


# ===================================================================
# SEÇÃO 9 — MAIN
# ===================================================================
if __name__ == "__main__":
    # Inicialização da rede: matriz e lista de adjacência.
    matriz_adj, lista_adj = inicializar_rede()

    while True:
        exibir_menu()
        escolha = input("Digite a opção desejada: ").strip()

        if escolha == "0":
            print("\n\033[1mEncerrando o SIGIC. Até a próxima, colônia Aurora Siger!\033[0m")
            break

        elif escolha == "1":
            listar_modulos()
            aguardar_enter()

        elif escolha == "2":
            entrada = input("Digite o ID ou nome do módulo: ").strip()
            try:
                id_ou_nome = int(entrada)
            except ValueError:
                id_ou_nome = entrada
            modulo = consultar_modulo(id_ou_nome)
            if modulo:
                print(f"\nMódulo encontrado: {modulo['nome']}")
                for chave, valor in modulo.items():
                    print(f"  {chave}: {valor}")
            else:
                print("Módulo não encontrado.")
            aguardar_enter()

        elif escolha == "3":
            exibir_matriz(matriz_adj)
            aguardar_enter()

        elif escolha == "4":
            exibir_lista_adj(lista_adj)
            aguardar_enter()

        elif escolha == "5":
            menu_algoritmos(lista_adj)

        elif escolha == "6":
            while True:
                submenu_simulacoes()
                sub = input("Escolha: ").strip()
                if sub == "0":
                    break
                elif sub == "1":
                    try:
                        id_mod = int(input("ID do módulo para simular falha: "))
                        simular_falha_modulo(id_mod, matriz_adj, lista_adj)
                    except (ValueError, KeyError):
                        print("Entrada inválida.")
                elif sub == "2":
                    try:
                        orig = int(input("ID de origem: "))
                        dest = int(input("ID de destino: "))
                        simular_falha_conexao(orig, dest, matriz_adj, lista_adj)
                    except (ValueError, KeyError):
                        print("Entrada inválida.")
                elif sub == "3":
                    try:
                        id_mod = int(input("ID do módulo para simular sobrecarga: "))
                        simular_sobrecarga(id_mod, matriz_adj, lista_adj)
                    except (ValueError, KeyError):
                        print("Entrada inválida.")
                elif sub == "4":
                    pontes = detectar_pontes(lista_adj, len(MODULOS))
                    if not pontes:
                        print("Não há pontes para simular.")
                    else:
                        for u, v in pontes:
                            simular_falha_conexao(u, v, matriz_adj, lista_adj)
                            print("-" * 40)
                else:
                    print("Opção inválida.")
                aguardar_enter()

        elif escolha == "7":
            modelagem_perda_energetica(CONEXOES)
            aguardar_enter()

        elif escolha == "8":
            relatorio_sustentabilidade(MODULOS, matriz_adj, lista_adj, CONEXOES)
            aguardar_enter()

        elif escolha == "9":
            limpar_tela()

        else:
            print("Opção inválida. Tente novamente.")
            aguardar_enter()