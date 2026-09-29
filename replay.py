# adiciona a joagada para o replay
def guardar_passo_replay(lista_replay, descricao_jogada):

    lista_replay.append(descricao_jogada)


def reproduzir_jogo(lista_replay):
    # reproduz o replay manualmente
    if not lista_replay:
        print("\nNenhum replay disponivel para esta partida.")
        return

    print("\n" + "=" * 40)
    print("=== REPRODUZINDO REPLAY DA ULTIMA PARTIDA ===")
    print("=" * 40)

    total_jogadas = len(lista_replay)

    for i, passo in enumerate(lista_replay, 1):
        print(f"Jogada {i:02d}/{total_jogadas} - {passo}")

        comando = input(
            "[ENTER] Proxima jogada | [Q] Sair do replay: ").strip().upper()
        if comando == "Q":
            break

    print("=" * 40)
    print("=== FIM DO REPLAY ===")
    print("=" * 40)
