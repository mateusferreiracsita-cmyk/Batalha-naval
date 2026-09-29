def validar_coordenada(coo):
    # Transforma em maiuscula para facilitar a verificacao
    coo = coo.upper()

    if len(coo) < 2 or len(coo) > 3:
        print("Entrada incorreta (tamanho invalido). Digite novamente!")
        return False

    letra = coo[0]
    parte_numerica_str = coo[1:]

    if letra not in "ABCDEFGHIJ":
        print("Entrada incorreta (letra invalida). Digite novamente!")
        return False

    # so aceita digitos (barra coisas como 'A+5' e 'A 5' que o int() aceitaria)
    if not parte_numerica_str.isdigit():
        print("Entrada incorreta (numero invalido). Digite novamente!")
        return False

    # usando try para n dar erro crítico
    try:
        parte_numerica = int(parte_numerica_str)
    except ValueError:
        print("Entrada incorreta (numero invalido). Digite novamente!")
        return False

    if parte_numerica < 1 or parte_numerica > 10:
        print("Entrada incorreta (fora do tabuleiro). Digite novamente!")
        return False

    return True


def converter_coordenada(coo):
    # Converte 'C5' para os indices da matriz (linha 4, coluna 2)
    coo = coo.upper()
    letra = coo[0]
    parte_numerica = coo[1:]

    coluna = "ABCDEFGHIJ".index(letra)
    linha = int(parte_numerica) - 1

    return (linha, coluna)


def formatar_tempo(segundos_totais):
    # Formato HH:MM:SS
    horas = int(segundos_totais // 3600)
    minutos = int((segundos_totais % 3600) // 60)
    segundos = int(segundos_totais % 60)

    # O :02d garante os dois digitos exigidos
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"
