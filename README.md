
# TechInclusiva - Auditoria de Acessibilidade Web

## Sobre o projeto

Trabalho prático da disciplina de Qualidade e Teste de Software.

Professor: MSc. Hugo Menezes Barra.

O projeto realiza uma auditoria automatizada de acessibilidade
em uma página HTML, utilizando Axe-core CLI e Python.

## Tecnologias utilizadas

- HTML
- Python 3.8
- Axe-core CLI
- Node.js
- VSCode
- ReportLab

## Resultados da auditoria

Página original:
- 4 regras violadas
- 11 ocorrências identificadas

Página corrigida:
- 0 violações detectadas pelo Axe

## Como executar

Iniciar o servidor:

    python3 -m http.server 8081

Executar a auditoria com Axe:

    npx axe http://localhost:8081/index.html --chromedriver-path="$PWD/node_modules/chromedriver/lib/chromedriver/chromedriver"

Analisar o JSON:

    python3 parser.py

Gerar o PDF:

    python3 gerar_pdf.py

## Arquivos principais

- index.html: página original
- index_corrigido.html: página corrigida
- resultado_axe.json: auditoria inicial
- resultado_corrigido.json: auditoria final
- parser.py: análise das violações
- gerar_pdf.py: geração do relatório
- relatorio_auditoria.pdf: relatório técnico

## Observação

A ausência de violações automáticas não garante
conformidade completa com a WCAG 2.1 AA.
Testes manuais complementares são necessários.
