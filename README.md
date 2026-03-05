# 🧠 Simulação de IA: Busca Heurística com A* (A-Estrela)

Este projeto é uma simulação de *Pathfinding* (Busca de Caminhos) desenvolvida em Python com a biblioteca Pygame. O objetivo do agente (personagem) é encontrar a rota mais eficiente do ponto inicial até a linha de chegada, desviando de obstáculos gerados proceduralmente.

Projeto desenvolvido como requisito para a disciplina de **Inteligência Artificial**, ministrada pela **Professora Ana Marina**.

## 🎯 O Problema
O agente encontra-se em um ambiente bidimensional (Grid) desconhecido, que gera "paredões" de obstáculos com passagens (buracos) em posições aleatórias. O desafio é calcular matematicamente a melhor rota até o objetivo sem colidir com os obstáculos, executando o trajeto em tempo real.

## 🤖 Inteligência Artificial Aplicada

Para resolver o labirinto, o projeto implementa o algoritmo de busca heurística **A\* (A-Estrela)**. Ele é ideal para essa simulação pois não faz uma busca "cega", mas sim uma busca informada e otimizada baseada na função de custo:

**`f(n) = g(n) + h(n)`**

Onde:
* **`g(n)`**: É o custo exato do caminho do ponto de partida até o nó atual `n`.
* **`h(n)`**: É a nossa **Heurística**. 
* **`f(n)`**: É o custo total estimado. O algoritmo sempre expande o nó com o menor `f(n)`.

### A Heurística: Distância de Manhattan
Como a movimentação do nosso agente ocorre em uma grade (movimentos verticais e horizontais prioritários), a heurística escolhida foi a **Distância de Manhattan**. O algoritmo calcula a distância absoluta em blocos de `X` e `Y` entre a posição testada e a linha de chegada, "puxando" a busca na direção correta e poupando processamento.

## ✨ Funcionalidades
* **Geração Procedural:** A cada nova execução, o mapa cria barreiras verticais com passagens aleatórias, garantindo que a IA sempre enfrente um problema inédito.
* **Cálculo em Tempo Real:** O algoritmo varre o mapa e encontra a saída em milissegundos assim que o cenário é gerado.
* **Modo Apresentação (Visualização de Rota):** É possível alternar a visibilidade da linha vermelha que representa a rota calculada pela heurística, facilitando a explicação didática do algoritmo operando por baixo dos panos.

## 🛠️ Tecnologias Utilizadas
* **Python 3.x**
* **Pygame** (Manipulação de gráficos e renderização do grid)
* **Dotenv** (Gerenciamento de ambiente, conforme estrutura base)

## 🚀 Como Executar

1. Clone este repositório:
```bash
git clone [https://github.com/gabriellina640/runner_py.git](https://github.com/gabriellina640/runner_py.git)
Entre na pasta do projeto:

Bash
cd runner_py
Instale as dependências necessárias utilizando o arquivo requirements.txt:

Bash
pip install -r requirements.txt
Execute a simulação:

Bash
python main.py
⌨️ Controles da Simulação
1 (Número Um): Gera um novo mapa procedural e inicia o cálculo da IA.

H: Oculta/Mostra a linha vermelha da rota traçada pela Heurística (Excelente para demonstrações ao vivo).

👨‍💻 Autor
Desenvolvido por Gabriel.