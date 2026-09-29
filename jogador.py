def obter_nome_jogador():
    # Pede o nome do usuario e garante que nao esta vazio
    nome = input("Digite o seu nome de capitao: ").strip()

    while not nome:
        print("Nome invalido. Por favor, insira um nome.")
        nome = input("Digite o seu nome de capitao: ").strip()

    return nome
