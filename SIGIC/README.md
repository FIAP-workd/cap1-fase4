# SIGIC - Sistema Inteligente de Gerenciamento da Infraestrutura da Colônia

## Descrição do projeto

O SIGIC foi feito para representar a infraestrutura da base marciana fictícia Aurora Siger. A ideia principal foi transformar os setores da colônia em um grafo: cada módulo vira um vértice e cada ligação física entre eles vira uma aresta com peso, usando a distância em metros.

Com isso, o programa consegue listar os módulos, mostrar a matriz e a lista de adjacência, executar algoritmos de busca e menor caminho, simular falhas e gerar uma análise simples de energia e sustentabilidade.

## Objetivos

- Representar a infraestrutura da colônia usando grafos.
- Aplicar matriz de adjacência e lista de adjacência.
- Usar BFS para verificar alcance e níveis da rede.
- Usar DFS para percorrer a estrutura da rede.
- Usar Dijkstra para calcular menores caminhos.
- Detectar conexões críticas com Tarjan.
- Simular falhas de módulo, falhas de conexão e sobrecarga.
- Aplicar uma modelagem matemática para perda de energia.
- Gerar um relatório simples de sustentabilidade e governança.

## Módulos da colônia

| ID | Módulo | Prioridade |
| --- | --- | --- |
| 1 | Habitação | 1 |
| 2 | Centro de Controle | 1 |
| 3 | Armazenamento de Energia | 2 |
| 4 | Agricultura | 3 |
| 5 | Laboratório Científico | 4 |
| 6 | Comunicação | 2 |
| 7 | Suporte Médico | 1 |
| 8 | Produção de Oxigênio | 1 |

Cada módulo guarda dados como nome, tipo, consumo energético, prioridade, capacidade de armazenamento, necessidade de comunicação, status e coordenadas.

## Representação da rede

A rede foi modelada como um grafo não direcionado.

- Vértices: módulos da base.
- Arestas: conexões físicas entre módulos.
- Pesos: distância entre os módulos, em metros.

O projeto usa duas representações:

- Matriz de adjacência, boa para visualizar todas as conexões possíveis.
- Lista de adjacência, mais prática para percorrer os vizinhos nos algoritmos.

## Estruturas de dados usadas

- Dicionários: armazenam os módulos e seus atributos.
- Listas: usadas em filas, pilhas, caminhos e conexões.
- Tuplas: usadas para registrar conexões e dados fixos dos módulos.
- Matrizes: usadas na matriz de adjacência da rede.

## Algoritmos implementados

### BFS - Busca em Largura

Foi usada para percorrer a rede por níveis a partir de um módulo de origem. No teste principal, partindo da Habitação, todos os módulos foram alcançados, mostrando que a rede está conectada.

### DFS - Busca em Profundidade

Foi usada para percorrer a rede indo o mais fundo possível em cada caminho antes de voltar. Ela ajuda a demonstrar a conectividade da rede de outra forma.

### Dijkstra

Foi usado para encontrar o menor caminho entre dois módulos. Um exemplo testado foi o caminho entre Habitação e Produção de Oxigênio, que passou por Comunicação e teve custo total de 45 metros.

### Tarjan - Pontes

Foi usado para verificar se alguma conexão da rede é crítica a ponto de desconectar partes da base quando removida. Na configuração atual, nenhuma ponte foi detectada.

## Simulações

O sistema possui simulações de:

- Falha de módulo.
- Falha de conexão.
- Sobrecarga energética.
- Teste das pontes da rede.

Essas simulações servem para observar como a infraestrutura se comportaria em situações de risco.

## Modelagem matemática

A perda de energia foi modelada pela fórmula:

```text
P(l) = P0 * e^(-alpha * l)
```

Onde:

- P0 é a potência inicial.
- alpha é o coeficiente de perda.
- l é a distância da conexão.
- P(l) é a potência final após a transmissão.

A ideia é mostrar que conexões mais longas tendem a desperdiçar mais energia.

## Funcionalidades do menu

1. Listar módulos da base
2. Consultar módulo
3. Exibir matriz de adjacência
4. Exibir lista de adjacência
5. Algoritmos de rede (BFS / DFS / Dijkstra / Pontes)
6. Simulações de falha e sobrecarga
7. Modelagem matemática de perda de energia
8. Relatório de sustentabilidade e governança
9. Limpar tela
0. Sair do sistema

## Como executar

Requisito:

- Python 3.10 ou superior

Comando:

```bash
python sigic.py
```

## Arquivos da entrega

- `sigic.py`: código principal do sistema.
- `README.md`: documentação do projeto.
- `rede_colonia.pdf`: relatório formal da rede da colônia.
- `exemplos_execucao.pdf`: prints e resultados dos testes.
- `link_video.txt`: link do vídeo de apresentação.

## Conclusão

O projeto mostra como os conceitos de grafos podem ser aplicados em uma situação simulada de gerenciamento de infraestrutura. Mesmo sendo uma base fictícia, a lógica usada no SIGIC se aproxima de problemas reais de conectividade, caminhos mínimos, redundância, consumo de energia e tomada de decisão em sistemas críticos.
