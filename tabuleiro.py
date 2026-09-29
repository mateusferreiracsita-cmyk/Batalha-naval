def criar_tabuleiro():
    # cria somente uma matriz 10 x 10 com ~
    return [["~" for _ in range(10)] for _ in range(10)]


def exibir_tabuleiro(tabuleiro, ocultar_navios=False):
    # printa as letras e os numeros, para simbolizar as linhas e as colunas
    colunas = "   A B C D E F G H I J"
    print(colunas)

    for i, linha in enumerate(tabuleiro):
        numero_linha = f"{i + 1:2d}"  # formatacao

        # Cria uma linha temporaria para exibicao
        linha_formatada = []
        for celula in linha:

            # Se ocultar_navios for True, disfarca o 'N' de agua
            if ocultar_navios and celula == "N":
                linha_formatada.append("~")
            else:
                linha_formatada.append(celula)

        # join para juntar e tirar espaco
        conteudo_linha = " ".join(linha_formatada)
        print(f"{numero_linha} {conteudo_linha}")


def realizar_tiro(tabuleiro, linha, coluna):
    if tabuleiro[linha][coluna] == '~':
        tabuleiro[linha][coluna] = 'O'
        return True  # consumiu turno

    if tabuleiro[linha][coluna] == 'N':
        tabuleiro[linha][coluna] = 'X'
        return True  # consumiu turno

    else:  # jogada repetida (se for X, O ou A)
        print("Ataque repetido!! Tente novamente.")
        return False  # nao consumiu turno


def rotulo_resultado(acertou, navios_afundados):
    # texto curto do resultado, usado no replay
    if navios_afundados:
        return "Afundado"
    if acertou:
        return "Acerto"
    return "Agua"


def exibir_mensagem_jogada(acertou, navios_afundados, por_computador=False):
    # mensagens de agua, acerto e navio afundado (RF06)
    if navios_afundados:
        for tipo in navios_afundados:
            if por_computador:
                print(f"Navio afundado! O computador destruiu um navio "
                      f"{tipo} seu.")
            else:
                print(f"Navio afundado! Voce destruiu um navio {tipo} "
                      f"do adversario.")
    elif acertou:
        if por_computador:
            print("Acerto! O computador atingiu um dos seus navios.")
        else:
            print("Acerto! Voce atingiu um navio inimigo.")
    else:
        if por_computador:
            print("Agua! O computador errou o tiro.")
        else:
            print("Agua! Nenhum navio atingido nessa posicao.")
