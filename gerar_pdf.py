
# TechInclusiva - Relatorio de Acessibilidade
# Disciplina: Qualidade e Teste de Software

import json
from xml.sax.saxutils import escape

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Preformatted, PageBreak, Table, TableStyle
)
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# Ler os resultados das auditorias
with open("resultado_axe.json", encoding="utf-8") as arquivo:
    antes = json.load(arquivo)

with open("resultado_corrigido.json", encoding="utf-8") as arquivo:
    depois = json.load(arquivo)

if isinstance(antes, list):
    antes = antes[0]

if isinstance(depois, list):
    depois = depois[0]

violacoes = antes["violations"]
violacoes_corrigidas = depois["violations"]

total_antes = sum(len(v["nodes"]) for v in violacoes)
total_depois = sum(len(v["nodes"]) for v in violacoes_corrigidas)

# Criar documento
pdf = SimpleDocTemplate(
    "relatorio_auditoria.pdf",
    pagesize=A4,
    leftMargin=45,
    rightMargin=45,
    topMargin=45,
    bottomMargin=45
)

estilos = getSampleStyleSheet()

estilos.add(ParagraphStyle(
    name="MeuTitulo",
    parent=estilos["Title"],
    fontSize=17,
    leading=22,
    textColor=colors.HexColor("#17365D"),
    spaceAfter=20
))

estilos.add(ParagraphStyle(
    name="MinhaSecao",
    parent=estilos["Heading2"],
    textColor=colors.HexColor("#17365D"),
    spaceBefore=16,
    spaceAfter=10,
    keepWithNext=True
))

estilos.add(ParagraphStyle(
    name="MeuTexto",
    parent=estilos["Normal"],
    fontSize=10,
    leading=15,
    spaceAfter=9
))

estilo_codigo = ParagraphStyle(
    name="Codigo",
    fontName="Courier",
    fontSize=7,
    leading=10,
    spaceAfter=0
)

conteudo = []

# Funcoes simples para organizar o PDF
def titulo(texto):
    conteudo.append(
        Paragraph(escape(texto), estilos["MeuTitulo"])
    )

def secao(texto):
    conteudo.append(
        Paragraph(escape(texto), estilos["MinhaSecao"])
    )

def texto(conteudo_texto):
    conteudo.append(
        Paragraph(escape(str(conteudo_texto)), estilos["MeuTexto"])
    )

# Capa e identificacao
titulo("Relatório de Auditoria de Acessibilidade Web")

texto("Projeto: Portal TechInclusiva")
texto("Disciplina: Qualidade e Teste de Software")
texto("Professor: MSc. Hugo Menezes Barra")
texto("Ferramentas: Axe-core CLI, Python e VSCode")

secao("1. Objetivo")
texto(
    "Identificar problemas de acessibilidade web, "
    "analisar as violações encontradas e aplicar "
    "correções no código HTML."
)

secao("2. Metodologia")
texto(
    "A página HTML original foi executada em um servidor "
    "local na porta 8081. A ferramenta Axe-core CLI "
    "realizou as auditorias, gerando arquivos JSON. "
    "Um script Python analisou os resultados."
)

secao("3. Diagnóstico inicial")
texto("Regras violadas: " + str(len(violacoes)))
texto("Ocorrências identificadas: " + str(total_antes))

criterios = {
    "wcag111": "1.1.1 - Conteúdo Não Textual (Nível A)",
    "wcag143": "1.4.3 - Contraste Mínimo (Nível AA)"
}

for violacao in violacoes:
    secao("Regra: " + violacao["id"])

    texto("Descrição: " + violacao["help"])
    texto("Severidade: " + str(violacao["impact"]))

    texto("Elementos afetados:")

    for elemento in violacao["nodes"]:
        texto(" - " + ", ".join(elemento["target"]))

    encontrou_wcag = False

    for tag in violacao["tags"]:
        if tag in criterios:
            texto("WCAG: " + criterios[tag])
            encontrou_wcag = True

    if not encontrou_wcag:
        texto(
            "Regra de boa prática sem critério WCAG "
            "diretamente informado pelo Axe."
        )

    texto("Referência: " + violacao["helpUrl"])

secao("4. Correções realizadas")

correcoes = [
    "Melhoria do contraste entre texto e fundo.",
    "Remoção da referência à imagem inexistente.",
    "Organização do conteúdo com header, main e section.",
    "Inclusão de labels nos campos do formulário.",
    "Melhoria na descrição do link de contato."
]

for item in correcoes:
    texto("- " + item)

secao("5. Comparação dos resultados")

tabela = Table([
    ["Indicador", "Antes", "Depois"],
    ["Regras violadas", str(len(violacoes)),
     str(len(violacoes_corrigidas))],
    ["Ocorrências", str(total_antes), str(total_depois)]
], colWidths=[220, 100, 100])

tabela.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("PADDING", (0, 0), (-1, -1), 9),
]))

conteudo.append(tabela)
conteudo.append(Spacer(1, 15))

texto(
    "A auditoria final não identificou violações "
    "nas verificações automáticas realizadas pelo Axe."
)

# HTML corrigido em uma nova pagina
conteudo.append(PageBreak())
secao("6. Código HTML corrigido")

with open("index_corrigido.html", encoding="utf-8") as arquivo:
    linhas = arquivo.readlines()

for linha in linhas:
    conteudo.append(
        Preformatted(
            linha.rstrip("\n") or " ",
            estilo_codigo,
            maxLineLength=85
        )
    )

secao("7. Conclusão")
texto(
    "A auditoria inicial encontrou 11 ocorrências "
    "distribuídas em quatro regras. Após as correções, "
    "a nova auditoria apresentou zero violações."
)

texto(
    "A ausência de violações automáticas não garante "
    "conformidade integral com a WCAG 2.1 AA. "
    "São necessários testes manuais complementares."
)

secao("8. Repositório GitHub")
texto("Link: será adicionado após a publicação.")

# Numero das paginas
def numerar_paginas(canvas, documento):
    canvas.setFont("Helvetica", 9)
    canvas.drawRightString(
        550, 25, "Página " + str(documento.page)
    )

# Gerar o PDF
pdf.build(
    conteudo,
    onFirstPage=numerar_paginas,
    onLaterPages=numerar_paginas
)

print("PDF atualizado com sucesso!")
print("Arquivo: relatorio_auditoria.pdf")

