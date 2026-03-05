# 🏃‍♀️ Runner - Projeto de Inteligência Artificial

Um jogo *side-scroller* estilo "Endless Runner" desenvolvido em Python utilizando a biblioteca Pygame. O jogo possui progressão de dificuldade, geração controlada de inimigos e um final comemorativo em sistema de partículas.

Projeto desenvolvido como requisito para a disciplina de Inteligência Artificial, ministrada pela Professora Ana Marina.

## 🎮 O Jogo
O jogador controla uma personagem que deve pular obstáculos (caracóis e moscas) que aparecem em velocidades crescentes. Sobreviva tempo o suficiente para alcançar a linha de chegada e vencer o jogo!

### ✨ Principais Funcionalidades
* **Máquina de Estados Finitos (FSM):** Arquitetura do jogo dividida em estados isolados (`START`, `PLAYING`, `FINISHING`, `GAME_OVER`, `VICTORY`), garantindo um código limpo e sem bugs de transição.
* **Dificuldade Dinâmica:** A velocidade dos inimigos aumenta progressivamente de acordo com o tempo de sobrevivência do jogador.
* **Spawn Inteligente:** Sistema de geração de inimigos com intervalos de tempo aleatórios (randomização do Pygame Timer), mas posições fixas de saída, prevenindo a criação de "armadilhas impossíveis" de esquivar.
* **Animações e Gravidade:** Física simples de pulo e troca de sprites animadas para o jogador e inimigos.
* **Sistema de Partículas Customizado:** Chuva de confetes gerada matematicamente no código (sem uso de imagens externas) durante a transição para a tela de vitória.

## 🛠️ Tecnologias Utilizadas
* **Python 3.x**
* **Pygame** (Manipulação de gráficos, eventos e áudio)
* **Dotenv** (Gerenciamento de variáveis de ambiente)

## 📁 Estrutura do Projeto
Certifique-se de que os arquivos de mídia estão organizados na seguinte estrutura antes de rodar o jogo:

```text
/
├── graphics/
│   ├── Girl/          # Sprites do jogador (walking/, jumping/)
│   ├── Fly/           # Sprites da mosca
│   ├── snail/         # Sprites do caracol
│   ├── Sky.png        # Fundo
│   ├── ground.png     # Chão
│   ├── game_start.png # Tela inicial
│   ├── game_over1.png # Tela de derrota
│   └── chegada.png    # Sprite da linha de chegada
├── audio/
│   └── jump.mp3       # Efeito sonoro do pulo
├── font/
│   └── Pixeltype.ttf  # Fonte customizada do jogo
├── main.py            # Código principal do jogo
└── requirements.txt   # Dependências do projeto
🚀 Como Executar
Clone este repositório:

Bash
git clone [https://github.com/gabriellina640/runner_py.git](https://github.com/gabriellina640/runner_py.git)
Entre na pasta do projeto:

Bash
cd runner_py
Instale as dependências necessárias utilizando o arquivo requirements.txt:

Bash
pip install -r requirements.txt
Execute o arquivo principal:

Bash
python main.py
⌨️ Controles
ESPAÇO: Pular

1 (Número Um): Iniciar jogo / Reiniciar jogo após Game Over ou Vitória.

👨‍💻 Autor
Desenvolvido por Gabriel.


---

**Dica extra:** Não se esqueça de criar o arquivo `requirements.txt` na raiz da pasta do seu projeto (junto com o `main.py`) com o seguinte conteúdo, para que o comando de instalação funcione perfeitamente para quem baixar:

```text
pygame
python-dotenv