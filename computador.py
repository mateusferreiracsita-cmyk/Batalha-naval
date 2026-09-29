import random


def jogada_computador(tabuleiro_adversario):
    """IA Avancada de Batalha Naval:
    1. Modo Direcional: Se encontrar 2 ou mais 'X' alinhados, continua a
    disparar nas extremidades dessa mesma linha/coluna.
    2. Modo Caca: Se encontrar apenas 1 'X' isolado, testa os vizinhos
    imediatos.
    3. Modo Busca: Joga aleatoriamente se nao houver alvos pendentes.
    """

    alvos_direcionais = []  # modo direcional
    alvos_vizinhos = []  # modo caca

    # procurando por 'X' no tabuleiro
    for lin in range(10):
        for c in range(10):
            if tabuleiro_adversario[lin][c] == "X":
                # Verifica se tem um 'X' vizinho na HORIZONTAL para modo
                # direcional
                if ((c + 1 < 10 and tabuleiro_adversario[lin][c + 1] == "X")
                        or (c - 1 >= 0
                            and tabuleiro_adversario[lin][c - 1] == "X")):
                    # Continuacao horizontal (procura nas pontas esquerda e
                    # direita)
                    for dc in [-1, 1]:
                        nc = c + dc
                        if (0 <= nc < 10 and
                                tabuleiro_adversario[lin][nc] in ["~", "N"]):
                            alvos_direcionais.append((lin, nc))

                # Verifica se tem um 'X' vizinho na VERTICAL para modo
                # direcional
                if ((lin + 1 < 10
                     and tabuleiro_adversario[lin + 1][c] == "X")
                        or (lin - 1 >= 0
                            and tabuleiro_adversario[lin - 1][c] == "X")):
                    # Continuacao vertical (procura nas pontas cima e baixo)
                    for dl in [-1, 1]:
                        nl = lin + dl
                        if (0 <= nl < 10
                                and tabuleiro_adversario[nl][c] in ["~", "N"]):
                            alvos_direcionais.append((nl, c))

                # Caso seja apenas um 'X' isolado, vai para modo caca e  guarda
                # os vizinhos em cruz
                vizinhos = [(lin - 1, c), (lin + 1, c),
                            (lin, c - 1), (lin, c + 1)]
                for vl, vc in vizinhos:
                    if (0 <= vl < 10 and 0 <= vc < 10
                            and tabuleiro_adversario[vl][vc] in ["~", "N"]):
                        # validacao dos vizinhos em cruz para nao acessar
                        # posicoes inexistentes
                        alvos_vizinhos.append((vl, vc))

    # Se ja descobriu a direcao (2 ou mais 'X' alinhados), segue a ponta!
    if alvos_direcionais:
        linha, coluna = random.choice(alvos_direcionais)
        letra = "ABCDEFGHIJ"[coluna]
        return linha, coluna

    # Se tem apenas 1 'X', atira nos vizinhos
    if alvos_vizinhos:
        linha, coluna = random.choice(alvos_vizinhos)
        letra = "ABCDEFGHIJ"[coluna]
        return linha, coluna

    # Se não tem 'X', modo aleatorio
    while True:
        linha = random.randint(0, 9)
        coluna = random.randint(0, 9)

        if tabuleiro_adversario[linha][coluna] in ["~", "N"]:
            letra = "ABCDEFGHIJ"[coluna]
            return linha, coluna
