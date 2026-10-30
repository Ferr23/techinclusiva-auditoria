
# Trabalho de Auditoria de Acessibilidade Web
# Portal TechInclusiva
# Leitura e análise do relatório gerado pelo Axe

import json

# Abre o arquivo JSON da auditoria
with open("resultado_axe.json", "r", encoding="utf-8") as arquivo:
    dados = json.load(arquivo)

# O Axe salva os resultados em uma lista
# Selecionamos a primeira página analisada
resultado = dados[0] if isinstance(dados, list) else dados

# Obtém as violações identificadas
violacoes = resultado["violations"]

total_regras = 0
total_ocorrencias = 0

# Contadores por severidade
severidades = {
    "critical": 0,
    "serious": 0,
    "moderate": 0,
    "minor": 0
}

print("===================================")
print("RELATORIO DE ACESSIBILIDADE")
print("Portal TechInclusiva")
print("===================================")

# Percorre todas as regras violadas
for violacao in violacoes:

    total_regras += 1

    nome = violacao["id"]
    descricao = violacao["help"]
    severidade = violacao["impact"]
    elementos = violacao["nodes"]

    total_ocorrencias += len(elementos)

    # Conta quantas regras existem em cada severidade
    if severidade in severidades:
        severidades[severidade] += 1

    print("\nRegra:", nome)
    print("Descricao:", descricao)
    print("Severidade:", severidade)

    # Mostra os elementos HTML afetados
    print("Elementos afetados:")

    for elemento in elementos:
        print(" -", elemento["target"])

    # Mostra os criterios WCAG relacionados
    print("Criterios WCAG:")

    for tag in violacao["tags"]:
        if tag.startswith("wcag"):
            print(" -", tag)

print("\n===================================")
print("RESUMO FINAL")
print("===================================")

print("Regras violadas:", total_regras)
print("Ocorrencias encontradas:", total_ocorrencias)

print("\nRegras por severidade:")

for nivel in severidades:
    print(nivel, ":", severidades[nivel])

print("===================================")
