# main.py
import time
from computador import jogada_computador
from estatisticas import criar_estatisticas, exibir_estatisticas
from estatisticas import registrar_tiro
from jogador import obter_nome_jogador
from menu import exibir_menu_modo_jogo, exibir_menu_principal, exibir_creditos
from navios import posicionar_navios_aleatorios
from navios import verificar_e_atualizar_afundados
from estatisticas import atualizar_historico, exibir_historico
from replay import guardar_passo_replay, reproduzir_jogo
from tabuleiro import criar_tabuleiro, exibir_tabuleiro, realizar_tiro
from tabuleiro import exibir_mensagem_jogada, rotulo_resultado
from utils import converter_coordenada, formatar_tempo, validar_coordenada

# Variaveis globais que seguraram os dados da ultima partida
ultimas_estatisticas = None
ultimo_replay = []


def verificar_fim_jogo(tabuleiro):
    # Varre a matriz: se nao houver nenhum 'N', o jogador dono do tabuleiro
    # perdeu
    for linha in tabuleiro:
        if "N" in linha:
            return False
    return True


def gerenciar_fim_de_jogo(vencedor, jogadas, tempo_total_segundos,
                          stats, lista_replay):
    # Atualiza as variaveis globais para acesso via menu que são da ultima
    # partida
    global ultimas_estatisticas, ultimo_replay
    ultimas_estatisticas = stats
    ultimo_replay = lista_replay

    tempo_total_str = formatar_tempo(tempo_total_segundos)

    print("\n" + "=" * 40)
    print("               FIM DE JOGO              ")
    print("=" * 40)
    print(f"Vencedor: {vencedor}")
    print(f"Total de jogadas: {jogadas}")
    print(f"Tempo de partida: {tempo_total_str}")
    print("=" * 40)

    exibir_estatisticas(stats)

    # menu  de fim de jogo
    print("\n[1] Ver replay")
    print("[2] Nova partida")
    print("[3] Menu principal")
    opcao_fim = input("Escolha uma opcao: ").strip()

    if opcao_fim == "1":
        if ultimo_replay:  # somente para verificar se o ultimo_replay funciona
            reproduzir_jogo(ultimo_replay)
    elif opcao_fim == "2":
        iniciar_nova_partida()
    else:
        return
    # Se for outra coisa, sai da funcao e volta naturalmente ao menu principal


def conferir_frota(nome, tabuleiro, navios):
    # RF10: mostra a frota e deixa o jogador sortear de novo ate gostar
    while True:
        print(f"\n--- CONFERENCIA DA FROTA DE {nome.upper()} ---")
        exibir_tabuleiro(tabuleiro)
        opcao = input("[ENTER] confirmar a frota | "
                      "[R] sortear de novo: ").strip().upper()

        if opcao == "":
            return tabuleiro, navios
        elif opcao == "R":
            tabuleiro, navios = posicionar_navios_aleatorios(criar_tabuleiro())
        else:
            print("Opcao invalida. Digite R ou apenas ENTER.")


def executar_partida_contra_computador():
    nome_jogador = obter_nome_jogador()
    stats_jogador = criar_estatisticas()
    lista_replay = []

    print(f"\nBoa sorte, Capitao {nome_jogador} contra o Computador!")
    print("A posicionar frotas...")

    # duas variaveis pois a funcao posicionar_navios_aleatorios retorna 2 itens
    tabuleiro_jogador, navios_jogador = posicionar_navios_aleatorios(
        criar_tabuleiro())
    tabuleiro_computador, navios_computador = posicionar_navios_aleatorios(
        criar_tabuleiro())

    # conferindo frota (o jogador pode sortear de novo se nao gostar)
    tabuleiro_jogador, navios_jogador = conferir_frota(
        nome_jogador, tabuleiro_jogador, navios_jogador)

    tempo_inicio = time.time()
    turno_jogador = True
    jogadas_totais = 0

    while True:
        print("\n" + "=" * 40)

        if turno_jogador:
            print(f"--- TURNO DE {nome_jogador} ---")
            print("O seu tabuleiro:")
            exibir_tabuleiro(tabuleiro_jogador)

            print("\nTabuleiro inimigo:")

            # tabuleiro sem N
            exibir_tabuleiro(tabuleiro_computador, ocultar_navios=True)

            coo_str = input(
                "Digite a coordenada de ataque (ex: C5) ou 'SAIR': ").strip()
            if coo_str.upper() == "SAIR":
                break  # voltando para o menu

            if not validar_coordenada(coo_str):  # validacao
                continue

            linha, coluna = converter_coordenada(coo_str)

            posicao_alvo = tabuleiro_computador[linha][coluna]
            if posicao_alvo in ["O", "X", "A"]:
                print("Ja atacou esta posicao anteriormente. Tente outra.")
                continue  # se for tiro repetido, volta para o inicio do if

            acertou = posicao_alvo == "N"
            realizar_tiro(tabuleiro_computador, linha, coluna)
            registrar_tiro(stats_jogador, acertou)
            jogadas_totais += 1

            # verificar se nao afundou um navio
            navios_afundados = verificar_e_atualizar_afundados(
                tabuleiro_computador, navios_computador)
            exibir_mensagem_jogada(acertou, navios_afundados)

            # replay
            resultado_str = rotulo_resultado(acertou, navios_afundados)
            passo_str = (f"{nome_jogador} atirou em {coo_str.upper()} - "
                         f"{resultado_str}")
            guardar_passo_replay(lista_replay, passo_str)

            # verificar se o jogo ja nao foi finalizado,
            if verificar_fim_jogo(tabuleiro_computador):
                tempo_fim = time.time()  # setando tempo de jogo total
                # salva em data/
                atualizar_historico(nome_jogador, stats_jogador, True)
                gerenciar_fim_de_jogo(nome_jogador, jogadas_totais,
                                      tempo_fim - tempo_inicio,
                                      stats_jogador, lista_replay)
                break

            turno_jogador = False

        else:
            print("--- TURNO DO COMPUTADOR ---")
            l_pc, c_pc = jogada_computador(tabuleiro_jogador)

            colunas_letras = "ABCDEFGHIJ"
            coord_pc_str = f"{colunas_letras[c_pc]}{l_pc + 1}"
            acertou_pc = tabuleiro_jogador[l_pc][c_pc] == "N"

            realizar_tiro(tabuleiro_jogador, l_pc, c_pc)
            jogadas_totais += 1

            # verificar se nao afundou um navio
            navios_afundados_pc = verificar_e_atualizar_afundados(
                tabuleiro_jogador, navios_jogador)
            exibir_mensagem_jogada(acertou_pc, navios_afundados_pc,
                                   por_computador=True)

            # replay
            resultado_pc_str = rotulo_resultado(acertou_pc,
                                                navios_afundados_pc)
            passo_pc_str = (f"Computador atirou em {coord_pc_str} - "
                            f"{resultado_pc_str}")
            guardar_passo_replay(lista_replay, passo_pc_str)

            print(f"\nO seu tabuleiro apos o ataque do computador "
                  f"({coord_pc_str}):")
            exibir_tabuleiro(tabuleiro_jogador)

            # verificar se o jogo ja nao foi finalizado,
            if verificar_fim_jogo(tabuleiro_jogador):
                tempo_fim = time.time()  # setando tempo de jogo total
                # salva em data/
                atualizar_historico(nome_jogador, stats_jogador, False)
                gerenciar_fim_de_jogo("Computador", jogadas_totais,
                                      tempo_fim - tempo_inicio,
                                      stats_jogador, lista_replay)
                break

            turno_jogador = True
            input("\nPressione [ENTER] para o proximo turno...")


def executar_partida_dois_jogadores():
    print("\n--- MODO DOIS JOGADORES ---")
    nome1 = obter_nome_jogador()
    nome2 = input("Digite o nome do Segundo Jogador: ").strip()
    if not nome2:
        nome2 = "Jogador 2"  # para caso que fique sem nome
    if nome2.lower() == nome1.lower():
        nome2 = nome2 + " (2)"  # nomes iguais confundiriam o historico

    # daqui pra frente copiar e colar do executar_partida_contra_computador
    print(f"\nCapitao 1: {nome1} | Capitao 2: {nome2}")
    print("A posicionar frotas para ambos os jogadores...")

    tabuleiro_p1, navios_p1 = posicionar_navios_aleatorios(criar_tabuleiro())
    tabuleiro_p2, navios_p2 = posicionar_navios_aleatorios(criar_tabuleiro())

    tabuleiro_p1, navios_p1 = conferir_frota(nome1, tabuleiro_p1, navios_p1)
    print("\n" * 50)
    input(f"Passe o comando para {nome2} e pressione [ENTER]...")

    tabuleiro_p2, navios_p2 = conferir_frota(nome2, tabuleiro_p2, navios_p2)
    print("\n" * 50)
    input(f"Passe o comando para {nome1} e pressione [ENTER] "
          "para iniciar o jogo...")

    tempo_inicio = time.time()
    tabuleiro_tiros_p1 = criar_tabuleiro()
    tabuleiro_tiros_p2 = criar_tabuleiro()
    stats_p1 = criar_estatisticas()
    stats_p2 = criar_estatisticas()
    lista_replay = []

    vez_jogador_1 = True
    jogadas_totais = 0

    while True:
        print("\n" + "=" * 40)
        # definindo variaveis da rodada dependendo de quem é o turno (para nao
        # criar duas variaveis iguais)

        if vez_jogador_1:
            jogador_atual = nome1
            tab_proprio = tabuleiro_p1
            tab_tiros = tabuleiro_tiros_p1
            navios_adversario = navios_p2
            tab_adversario_real = tabuleiro_p2
            stats_atual = stats_p1

        else:
            jogador_atual = nome2
            tab_proprio = tabuleiro_p2
            tab_tiros = tabuleiro_tiros_p2
            navios_adversario = navios_p1
            tab_adversario_real = tabuleiro_p1
            stats_atual = stats_p2

        print(f"=== TURNO DE {jogador_atual.upper()} ===")
        print("O seu tabuleiro (sua frota):")
        exibir_tabuleiro(tab_proprio)

        print("\n" * 50)  # para esconder tabuleiro do inimigo no inicio!!
        print("\nO seu radar (tiros no inimigo):")
        exibir_tabuleiro(tab_tiros)

        coo_str = input(
            "Digite a coordenada de ataque (ex: C5) ou 'SAIR': ").strip()
        if coo_str.upper() == "SAIR":
            break

        if not validar_coordenada(coo_str):
            continue

        linha, coluna = converter_coordenada(coo_str)

        if tab_tiros[linha][coluna] in ["O", "X", "A"]:
            print("Ja atacou esta coordenada antes. Tente outra.")
            continue

        acertou = tab_adversario_real[linha][coluna] == "N"

        # Realiza o tiro no tabuleiro do inimigo
        realizar_tiro(tab_adversario_real, linha, coluna)
        registrar_tiro(stats_atual, acertou)
        jogadas_totais += 1

        # sincronizando resultado para o tabuleiro de ataque do jogador atual
        if acertou:
            tab_tiros[linha][coluna] = "X"
        else:
            tab_tiros[linha][coluna] = "O"

        # verificando se afundou algum navio
        navios_afundados = verificar_e_atualizar_afundados(
            tab_adversario_real, navios_adversario)
        exibir_mensagem_jogada(acertou, navios_afundados)

        # replay
        resultado_str = rotulo_resultado(acertou, navios_afundados)
        passo_str = (f"{jogador_atual} atirou em {coo_str.upper()} - "
                     f"{resultado_str}")
        guardar_passo_replay(lista_replay, passo_str)

        # sincronizando os afundandos tambem
        for lin in range(10):
            for c in range(10):
                if tab_adversario_real[lin][c] == "A":
                    tab_tiros[lin][c] = "A"

        if verificar_fim_jogo(tab_adversario_real):  # verificando fim de jogo
            tempo_fim = time.time()  # settando tempo total
            # salva em data/
            atualizar_historico(nome1, stats_p1, vez_jogador_1)
            atualizar_historico(nome2, stats_p2, not vez_jogador_1)
            gerenciar_fim_de_jogo(jogador_atual, jogadas_totais,
                                  tempo_fim - tempo_inicio,
                                  stats_atual, lista_replay)
            break

        vez_jogador_1 = not vez_jogador_1
        input("\nPasse o comando para o proximo jogador e pressione "
              "[ENTER]...")
        print("\n" * 50)


def iniciar_nova_partida():  # funcao do submenu
    while True:
        modo = exibir_menu_modo_jogo()
        if modo == "1":
            executar_partida_contra_computador()
            break
        elif modo == "2":
            executar_partida_dois_jogadores()
            break
        elif modo == "0":
            break
        else:
            print("Opcao invalida.")


def main():
    while True:  # funcao do menu principal
        opcao = exibir_menu_principal()

        if opcao == "1":
            iniciar_nova_partida()
        elif opcao == "2":
            if ultimas_estatisticas:
                exibir_estatisticas(ultimas_estatisticas)
            exibir_historico()
            input("\nPressione [ENTER] para voltar ao menu...")
        elif opcao == "3":
            if ultimo_replay:
                reproduzir_jogo(ultimo_replay)
            else:
                print("\nNenhum replay disponivel da ultima partida.")
            input("\nPressione [ENTER] para voltar ao menu...")
        elif opcao == "4":
            exibir_creditos()
        elif opcao == "5":
            print("\nA sair do jogo. Ate logo, Capitao!")
            break
        else:
            print("Opcao invalida. Escolha entre 1 e 5.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):  # Ctrl+C ou Ctrl+D
        print("\n\nJogo encerrado. Ate logo, Capitao!")
