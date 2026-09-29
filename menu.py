def exibir_menu_principal():
    print("\n" + "=" * 40)
    print("      BATALHA NAVAL - GPTECH GAMES      ")
    print("=" * 40)
    print("1. Nova partida")
    print("2. Ver estatisticas")
    print("3. Assistir replay da ultima partida")
    print("4. Creditos")
    print("5. Sair")
    print("=" * 40)

    opcao = input("Escolha uma opcao: ").strip()
    return opcao


def exibir_menu_modo_jogo():  # submenu para modo de jogo
    print("\n" + "=" * 35)
    print("      SELECIONE O MODO DE JOGO      ")
    print("=" * 35)
    print("[1] Jogador vs Computador")
    print("[2] Dois Jogadores")
    print("[0] Voltar ao menu")
    print("=" * 35)

    opcao = input("Escolha o modo: ").strip()
    return opcao


def exibir_creditos():
    # Mostra os creditos do projeto conforme menu principal
    print("\n" + "=" * 40)
    print("=== CREDITOS ===")
    print("=" * 40)
    print("Desenvolvedor: Desenvolvedor(a) Junior - GPTech Games")
    print("Disciplina: Programacao em Python")
    print("Professor: Guido Pantuza")
    print("=" * 40)

    input("Pressione [ENTER] para voltar...")
