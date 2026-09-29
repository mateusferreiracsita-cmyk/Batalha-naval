# Batalha Naval - GPTech Games

Projeto desenvolvido para a disciplina de Programação em Python (CEFET-MG, Campus Divinópolis), simulando o clássico jogo de tabuleiro Batalha Naval em modo texto.

- **Desenvolvedor:** Mateus Ferreira Carvalho Silva
- **Professor:** Guido Pantuza
- **Data de entrega:** 29/09/2026
- **Vídeo de demonstração:** (https://medal.tv/games/screen-capture/clips/nCBfaD91QYcMDxm40?invite=cr-MSxIeFcsNDE3NTM1NTY3)

## Instruções de execução

1. Tenha o Python 3.10 ou superior instalado (ambiente Linux).
2. Abra o terminal e navegue até a pasta raiz do projeto.
3. Execute o comando principal:

   ```bash
   python3 main.py
   ```

Não há dependências externas: só a biblioteca padrão do Python.

## Como jogar

- **Menu principal:** `1` nova partida, `2` estatísticas, `3` replay da última partida, `4` créditos, `5` sair.
- **Modos:** Jogador x Computador ou Dois Jogadores.
- **Conferência da frota:** antes de começar, cada jogador vê sua frota. Digite `R` para sortear de novo ou apenas `ENTER` para confirmar.
- **Jogadas:** coordenada no formato Letra + Número, de `A1` a `J10` (ex.: `C5`). Digite `SAIR` durante a partida para voltar ao menu.
- **Legenda:** `~` água não jogada | `N` navio | `X` acerto | `O` água jogada | `A` navio afundado.
- **Replay:** `ENTER` avança para a próxima jogada e `Q` sai do replay.
- **Encerrar a qualquer momento:** `Ctrl+C` ou `Ctrl+D` encerram o jogo.

## Estrutura do projeto

```
BatalhaNaval/
├── main.py           # fluxo das partidas e loop principal
├── menu.py           # menus e créditos
├── tabuleiro.py      # matriz 10x10, tiros e mensagens de jogada
├── navios.py         # frota, posicionamento e navios afundados
├── jogador.py        # leitura do nome do jogador
├── computador.py     # jogadas do computador (IA)
├── estatisticas.py   # estatísticas da partida e histórico em arquivo
├── replay.py         # histórico de jogadas e modo replay
├── utils.py          # validação/conversão de coordenadas e tempo
├── data/             # estatisticas.json (gerado automaticamente)
├── docs/
└── README.md
```

## Decisões de projeto e arquitetura

O sistema foi construído com foco em modularização (separação de responsabilidades) e legibilidade. Cada módulo `.py` tem um escopo isolado, o que facilita a manutenção e a leitura do código. As principais decisões técnicas:

- **Estruturas de dados:** o tabuleiro é uma matriz (lista de listas) nativa do Python, com acesso direto a qualquer coordenada. Cada célula guarda um estado: `~`, `N`, `X`, `O` ou `A`.
- **Frota e tipos de navio:** a frota é definida em `obter_frota()` (1 navio grande de 4 posições e 2 pequenos de 2 posições). Cada navio é uma lista de tuplas `(linha, coluna)`, e o tipo (pequeno ou grande) é obtido pelo tamanho. Isso permite verificar se um navio afundou olhando só as suas coordenadas, sem varrer o tabuleiro inteiro.
- **Mensagens de jogada:** `realizar_tiro` só altera o tabuleiro. As mensagens de água, acerto e navio afundado ficam em `exibir_mensagem_jogada`, o que separa a regra do jogo do texto exibido.
- **Inteligência do computador:** o `computador.py` implementa uma IA com três estados. Ao detectar um acerto, ataca os vizinhos imediatos. Com dois acertos alinhados, deduz o eixo do navio e ataca as extremidades. Sem acertos pendentes, joga de forma aleatória, sempre em posições ainda não jogadas.
- **Histórico persistente:** as estatísticas de cada jogador (partidas, vitórias, tiros, acertos) são acumuladas em `data/estatisticas.json`. Se o arquivo não existir ou estiver corrompido, o sistema começa com um histórico vazio em vez de quebrar.
- **Tratamento de exceções e entradas:** `utils.py` valida a coordenada (letra de A a J, apenas dígitos, número de 1 a 10) e usa `try/except` na conversão. O carregamento e o salvamento do histórico tratam erros de arquivo. `Ctrl+C` e `Ctrl+D` são capturados no `main.py`.
- **Replay:** para o histórico da partida, guardam-se apenas strings descrevendo cada jogada, em vez de cópias do tabuleiro a cada turno. Isso economiza memória e permite reproduzir a partida rapidamente.
- **Estilo:** o código segue as convenções do PEP 8 (indentação de 4 espaços, nomes em `snake_case`, funções curtas com responsabilidade única).

## Rastreabilidade dos requisitos

### Requisitos funcionais

| Requisito | Onde está |
|-----------|-----------|
| RF01 | `menu.py` (`exibir_menu_principal`) e loop em `main.py` |
| RF02 | `tabuleiro.py` (`criar_tabuleiro`, `exibir_tabuleiro`) |
| RF03 | `navios.py` (`obter_frota`, `obter_tipo_navio`): navio pequeno (2) e grande (4) |
| RF04 | `navios.py` (`posicao_valida`, `posicionar_navios_aleatorios`): posicionamento automático sem sobreposição |
| RF05 | `utils.py` (`validar_coordenada`) e checagem de tiro repetido em `main.py` |
| RF06 | `tabuleiro.py` (`exibir_mensagem_jogada`) e `navios.py` (`verificar_e_atualizar_afundados`) |
| RF07 | `main.py` (`gerenciar_fim_de_jogo`) e `utils.py` (`formatar_tempo`): vencedor, total de jogadas e tempo |
| RF08 | Opção 1 do menu e opção `[2] Nova partida` no fim do jogo. Com `SAIR` o jogador volta ao menu a qualquer momento |
| RF09 | `main.py`: `executar_partida_contra_computador` e `executar_partida_dois_jogadores` |
| RF10 | `main.py` (`conferir_frota`): o jogador confere a frota e pode sortear de novo antes de começar |
| RF11 | `replay.py` (`guardar_passo_replay`): cada jogada é registrada com jogador, coordenada e resultado |
| RF12 | `estatisticas.py`: partidas, vitórias, tiros, acertos e aproveitamento, acumulados em `data/` |
| RF13 | `replay.py` (`reproduzir_jogo`): replay manual da última partida |

### Regras de negócio

| Regra | Onde está |
|-------|-----------|
| RN01 | `utils.py`: coordenadas Letra + Número, colunas A-J e linhas 1-10 |
| RN02 | `main.py`: jogada em posição já jogada é rejeitada com mensagem, sem consumir a rodada |
| RN03 | `navios.py` (`verificar_e_atualizar_afundados`): navio afunda quando todas as posições são atingidas |
| RN04 | `main.py` (`verificar_fim_jogo`): a partida termina quando todos os navios de um jogador afundam |
| RN05 | `computador.py` (`jogada_computador`): escolhe jogadas válidas sozinho, com IA de caça e direção |

### Requisitos não funcionais

| Requisito | Situação |
|-----------|----------|
| RNF01, RNF02 | Projeto individual, em Python 3.10+ |
| RNF03 | Convenções do PEP 8 (verificar com `python3 -m pycodestyle .`) |
| RNF04 | Módulos coesos, conforme a estrutura definida no enunciado |
| RNF05 | Validação de coordenadas, opções de menu e nomes; tratamento de erros de arquivo e de `Ctrl+C`/`Ctrl+D` |
| RNF06 | Execução verificada em Ubuntu Linux (Python 3.12) com partidas simuladas nos dois modos |
| RNF07 | Interface em modo texto |

## Limitações conhecidas

- O replay guarda apenas a última partida, em memória. Ao fechar o programa ele é perdido.
- Só partidas concluídas entram no histórico de estatísticas. Partidas abandonadas com `SAIR` não contam.
- A frota é sorteada automaticamente. O jogador pode sortear de novo, mas não posiciona os navios manualmente.
- O histórico usa o nome digitado como identificador (maiúsculas e minúsculas contam como nomes diferentes).

## Uso de Inteligência Artificial

Utilizei assistência de Inteligência Artificial (Claude, Gemini e ChatGPT) durante o desenvolvimento, como revisora técnica e apoio de implementação, sempre sob minha direção e revisão: identificação de entradas não tratadas, ajuste da lógica do computador e a estruturação deste README. Como o autor não possui ambiente Linux, a verificação em Linux também foi feita com apoio da IA.
