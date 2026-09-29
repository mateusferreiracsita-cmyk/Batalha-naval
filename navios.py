import random


def obter_frota():
    # Aqui se coloca a frota que quer, no exemplo, temos 1 navio de 4 pontos e
    # 2 navios de 2 pontos, depois faca com que o usuario digite e escolha!
    return [4, 2, 2]


def obter_tipo_navio(tamanho):
    # Pelo tamanho do navio descobre se ele e pequeno (2) ou grande (4)
    if tamanho == 2:
        return "pequeno"
    return "grande"


def posicao_valida(tabuleiro, linha, coluna, tamanho, orientacao):
    # Verifica se o navio nao ultrapassa os  limites e se nao vai ocorrer
    # sobreposição

    if orientacao == "H":  # limites
        if coluna + tamanho > 10:
            return False

        for c in range(coluna, coluna + tamanho):  # sobreposicao
            if tabuleiro[linha][c] == "N":
                return False

    elif orientacao == "V":  # limites
        if linha + tamanho > 10:
            return False

        for lin in range(linha, linha + tamanho):  # sobreposicao
            if tabuleiro[lin][coluna] == "N":
                return False

    return True  # se der td certo, return True


def posicionar_navios_aleatorios(tabuleiro):
    frotas = obter_frota()  # pega a frota escolhida
    lista_de_navios = []  # guarda as coordenadas de cada navio individualmente

    for tamanho in frotas:
        posicionado = False

        while not posicionado:
            orientacao = random.choice(["H", "V"])
            linha = random.randint(0, 9)  # random
            coluna = random.randint(0, 9)

            if posicao_valida(tabuleiro, linha, coluna, tamanho, orientacao):
                coordenadas_navio = []

                if orientacao == "H":
                    for c in range(coluna, coluna + tamanho):
                        tabuleiro[linha][c] = "N"  # colocando os N do navio
                        # adiciona a coordenada do navio na lista
                        coordenadas_navio.append((linha, c))
                else:
                    for lin in range(linha, linha + tamanho):
                        tabuleiro[lin][coluna] = "N"  # colocando os N do navio
                        # adiciona a coordenada do navio na lista
                        coordenadas_navio.append((lin, coluna))

                # Guarda o navio completo na lista
                lista_de_navios.append(coordenadas_navio)

                posicionado = True

    return tabuleiro, lista_de_navios


def verificar_e_atualizar_afundados(tabuleiro, lista_de_navios):
    # Devolve uma lista com o tipo de cada navio que acabou de afundar agora
    navios_recem_afundados = []

    for navio in lista_de_navios:
        navio_afundado = True  # assume que ele está afundado

        for lin, c in navio:  # for que percorre as coord do navio
            if tabuleiro[lin][c] == "N":
                navio_afundado = False
                # Se achar um N, da break e ja sabe que não está afundado
                break

        if navio_afundado:
            # Se ja nao foi marcado como 'A', muda tudo para 'A' e conta
            ja_estava_afundado = True
            for lin, c in navio:
                if tabuleiro[lin][c] != "A":
                    ja_estava_afundado = False
                    # mudando os X por A para simbolizar Afundado
                    tabuleiro[lin][c] = "A"

            # Se acabou de afundar agora, guarda o tipo dele (pequeno ou
            # grande)
            if not ja_estava_afundado:
                navios_recem_afundados.append(obter_tipo_navio(len(navio)))

    return navios_recem_afundados
