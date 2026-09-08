# Validador de Estágios — IC/UFRJ

Ferramenta desenvolvida pelo projeto de extensão **InovaProcess** para auxiliar a Comissão de Estágio do Instituto de Computação da Universidade Federal do Rio de Janeiro (IC/UFRJ) na pré-análise da elegibilidade acadêmica de alunos para estágio.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![PDFPlumber](https://img.shields.io/badge/PDFPlumber-4A5568?style=for-the-badge)

---

## Sobre o projeto

O processo de análise de solicitações de estágio envolve a verificação de diversas informações acadêmicas presentes no **Boletim de Orientação Acadêmica (BOA)** do aluno.

O objetivo deste projeto é automatizar parte dessa análise, reduzindo tarefas repetitivas e facilitando a identificação de possíveis pendências antes da avaliação final pela Comissão de Estágio.

A aplicação recebe o BOA em formato PDF, extrai as informações acadêmicas relevantes e apresenta um relatório de elegibilidade ao usuário.

> **Importante:** a ferramenta realiza uma pré-análise automatizada. O resultado apresentado não substitui a avaliação oficial da Comissão de Estágio do IC/UFRJ.

---

## Funcionalidades

Atualmente, o sistema é capaz de:

- Extrair informações acadêmicas diretamente do BOA em PDF;
- Identificar o nome e a matrícula do aluno;
- Obter o Coeficiente de Rendimento acumulado;
- Verificar os períodos integralizados e o prazo máximo de integralização;
- Consultar a carga horária de extensão registrada;
- Verificar a quantidade de créditos obtidos;
- Identificar disciplinas obrigatórias ainda pendentes;
- Exibir o código e o nome das disciplinas pendentes;
- Gerar um relatório indicando se o aluno está **APTO** ou **INAPTO** segundo os critérios implementados.

---

## Critérios analisados

A pré-análise considera critérios acadêmicos utilizados no processo de elegibilidade para estágio, incluindo:

- **CR acumulado mínimo:** 6,0;
- **Prazo de integralização:** o número de períodos integralizados não pode ultrapassar o prazo máximo indicado no BOA;
- **Disciplinas obrigatórias:** conclusão das disciplinas obrigatórias previstas até o 4º período;
- **Créditos obtidos:** atendimento à quantidade mínima exigida;
- **Atividades de extensão:** análise da carga horária de extensão de acordo com os critérios acadêmicos aplicáveis ao aluno.

As regras podem ser atualizadas conforme alterações nas normas acadêmicas do IC/UFRJ.

---

## Como funciona

O fluxo da aplicação é:

1. O aluno envia seu **Boletim de Orientação Acadêmica (BOA)** em formato PDF;
2. O sistema extrai os dados acadêmicos do documento;
3. As informações são processadas pelas regras de elegibilidade;
4. A aplicação apresenta um relatório com cada critério analisado;
5. Caso existam disciplinas obrigatórias pendentes, seus códigos e nomes são exibidos ao usuário.

---

## Tecnologias

O projeto utiliza principalmente:

- **Python** — linguagem principal;
- **Streamlit** — interface web;
- **pdfplumber** — extração de informações dos arquivos PDF;
- **Pandas** — manipulação e processamento de dados;
- **NumPy** — operações auxiliares sobre dados.

---

## Estrutura do projeto

```text
automacao-comissao-estagio/
├── assets/
│   └── ...
├── data/
│   └── ...
├── src/
│   ├── components/
│   ├── app.py
│   ├── boa_scraper.py
│   ├── companies_scraper.py
│   └── elegibility_validator.py
├── .streamlit/
│   └── config.toml
├── .gitignore
├── requirements.txt
└── README.md
