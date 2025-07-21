# Gerador de Código para Expressões Aritméticas (Máquina de Pilha)

---

## Integrantes

* **Mateus Bastos dos Santos** - Matrícula: 211062240 - Turma: 01 (16hr)

---

## Introdução

Este projeto implementa um **Gerador de Código para Expressões Aritméticas** simples, focado em demonstrar as fases fundamentais de um compilador: **Análise Léxica**, **Análise Sintática** e **Geração de Código**. O sistema aceita expressões aritméticas básicas como entrada e as converte em uma sequência de instruções para uma **máquina de pilha hipotética**.

A linguagem de entrada é um subconjunto de expressões aritméticas que suporta:

* **Números Inteiros:** Ex: `10`, `42`, `0`
* **Operadores Aritméticos:** `+` (adição), `-` (subtração), `*` (multiplicação), `/` (divisão)
* **Agrupamento:** Parênteses `()` para alterar a precedência das operações.

### Sintaxe e Semântica da Linguagem de Entrada:

A sintaxe segue a notação infixa padrão que conhecemos para expressões matemáticas. A semântica é a avaliação usual das operações aritméticas, respeitando a **precedência de operadores** (multiplicação e divisão antes de adição e subtração) e o **agrupamento por parênteses**.

**Exemplos de Expressões Válidas:**
* `1 + 2`
* `10 * 3 - 5`
* `(2 + 3) * 4`
* `20 / (5 - 3)`

---

## Instalação

O projeto é desenvolvido em **Python 3** e não possui dependências externas além da biblioteca padrão do Python.

Para clonar o repositório e preparar o ambiente (assumindo que você tem `git` e `python3` instalados):

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/fcte-compiladores/trabalho-final-trabalhofinal-com.git](https://github.com/fcte-compiladores/trabalho-final-trabalhofinal-com.git)
    cd trabalho-final-trabalhofinal-com
    ```
2.  **Executar o programa:**
    Para executar o gerador de código com uma expressão de exemplo (assumindo o `main.py` dentro de `lox/`):
    ```bash
    python lox/main.py "10 + 2 * (3 - 1)"
    ```
    Ou, para uma execução interativa (se implementarmos um `REPL` simples no `main.py`):
    ```bash
    python lox/main.py
    ```
    *(Nota: A funcionalidade de execução interativa ou de leitura de arquivos será implementada no `lox/main.py` à medida que avançarmos.)*

---

## Exemplos

Você encontrará exemplos de uso na pasta `exemplos/`. Cada arquivo `.expr` contém uma expressão aritmética.

Para executar um exemplo a partir de um arquivo (esta funcionalidade será adicionada ao `lox/main.py`):

```bash
python lox/main.py -f exemplos/exemplo_simples.expr