import json  # para ler arquivo em data
import os

# caminho do arquivo onde o historico fica salvo (pasta data/)
CAMINHO_HISTORICO = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "data", "estatisticas.json")


def criar_estatisticas():
    # dicionario
    stats = {"tiros_totais": 0, "acertos": 0, "erros": 0,
             "navios_afundados": 0}
    return stats


def registrar_tiro(stats, acertou):
    # Atualiza as estatisticas apos um tiro
    stats["tiros_totais"] += 1
    if acertou:
        stats["acertos"] += 1
    else:
        stats["erros"] += 1


def calcular_precisao(stats):
    # Calcula a percentagem de precisao dos tiros
    if stats["tiros_totais"] == 0:
        return 0.0
    precisao = (stats["acertos"] / stats["tiros_totais"]) * 100
    return round(precisao, 2)


def exibir_estatisticas(stats):
    # mostra o relatorio final das estatisticas do jogador
    precisao = calcular_precisao(stats)

    print("\n" + "=" * 30)
    print("=== ESTATISTICAS DA PARTIDA ===")
    print("=" * 30)
    print(f"Total de tiros disparados: {stats['tiros_totais']}")
    print(f"Acertos (em navios): {stats['acertos']}")
    print(f"Erros (na agua): {stats['erros']}")
    print(f"Precisao: {precisao}%")
    print("=" * 30)


def carregar_historico():
    # Le o historico salvo em data/. Se nao existir ou estiver corrompido,
    # comeca vazio
    try:
        with open(CAMINHO_HISTORICO, "r", encoding="utf-8") as arquivo:
            historico = json.load(arquivo)
    except (OSError, json.JSONDecodeError):
        return {}

    if not isinstance(historico, dict):
        return {}
    return historico


def salvar_historico(historico):
    # Grava o historico em data/estatisticas.json (cria a pasta se precisar)
    try:
        os.makedirs(os.path.dirname(CAMINHO_HISTORICO), exist_ok=True)
        with open(CAMINHO_HISTORICO, "w", encoding="utf-8") as arquivo:
            json.dump(historico, arquivo, indent=2, ensure_ascii=False)
    except OSError:
        print("Aviso: nao foi possivel salvar o historico de estatisticas.")


def atualizar_historico(nome, stats, venceu):
    # Soma a partida que acabou de terminar no historico do jogador
    historico = carregar_historico()
    jogador = historico.get(nome, {})

    for chave in ("partidas", "vitorias", "tiros_totais", "acertos"):
        jogador.setdefault(chave, 0)  # garante que todas as chaves existem

    jogador["partidas"] += 1
    if venceu:
        jogador["vitorias"] += 1
    jogador["tiros_totais"] += stats["tiros_totais"]
    jogador["acertos"] += stats["acertos"]

    historico[nome] = jogador
    salvar_historico(historico)


def exibir_historico():
    # Mostra o historico acumulado de todos os jogadores (RF12)
    historico = carregar_historico()

    print("\n" + "=" * 30)
    print("=== HISTORICO DE JOGADORES ===")
    print("=" * 30)

    if not historico:
        print("Ainda nao existem partidas registradas. "
              "Jogue uma partida primeiro!")
        print("=" * 30)
        return

    for nome, dados in sorted(historico.items()):
        precisao = calcular_precisao(dados)  # aproveitamento = acertos / tiros
        print(f"Jogador: {nome}")
        print(f"  Partidas: {dados['partidas']} | "
              f"Vitorias: {dados['vitorias']}")
        print(f"  Tiros: {dados['tiros_totais']} | "
              f"Acertos: {dados['acertos']}")
        print(f"  Aproveitamento: {precisao}%")
        print("-" * 30)
