# Lox: Compilador de Expressões Aritméticas

## Integrantes

*   **Mateus Bastos dos Santos** - Matrícula: 211062240 - Turma: 01 (16hr)

## Sobre o Projeto

Este projeto implementa um compilador simples para **expressões aritméticas**, demonstrando as fases de: **Análise Léxica**, **Análise Sintática** e **Geração de Código**. O compilador converte expressões em uma sequência de instruções para uma **máquina de pilha hipotética**.

## Linguagem Suportada

A linguagem de entrada aceita expressões aritméticas básicas, incluindo:

*   **Números Inteiros:** Ex: `10`, `42`
*   **Operadores Aritméticos:** `+`, `-`, `*`, `/`
*   **Agrupamento:** Parênteses `()` para controlar a precedência.

A sintaxe segue a notação infixa padrão. A semântica é a avaliação usual das operações aritméticas, respeitando a **precedência de operadores** (multiplicação/divisão antes de adição/subtração) e o **agrupamento por parênteses**.

**Exemplos:**
*   `1 + 2`
*   `10 * 3 - 5`
*   `(2 + 3) * 4`
*   `20 / (5 - 3)`



## Estrutura do Projeto

```
.github/             # Configurações do GitHub
.vscode/             # Configurações do VS Code
lox/                 # Código-fonte do compilador Lox
├── __init__.py      # Indica que 'lox' é um pacote Python
├── lexer.py         # Analisador Léxico
├── parser.py        # Analisador Sintático e classes AST
├── code_generator.py # Lógica de Geração de Código
├── main.py          # Ponto de entrada principal
└── errors.py        # Classes de tratamento de erros
tests/               # Testes unitários
├── __init__.py
├── test_lexer.py    # Testes para o analisador léxico
├── test_parser.py   # Testes para o analisador sintático
exemplos/            # Arquivos de exemplo de expressões
├── simples.expr
├── precedencia.expr
├── parenteses.expr
└── complexo.expr
README.md            # Documentação do projeto
.gitignore           # Arquivos ignorados pelo Git
pyproject.toml       # Gerenciamento de pacotes
venv/                # Ambiente virtual Python
```

## Referências

Este projeto foi desenvolvido com base nos conceitos fundamentais de construção de compiladores. Uma referência notável que aborda em profundidade as fases de análise léxica e sintática, além da geração de árvores de sintaxe abstrata, é:

*   **Crafting Interpreters** por Robert Nystrom
    *   [https://craftinginterpreters.com/](https://craftinginterpreters.com/)
    *   Este recurso foi fundamental para a compreensão das etapas iniciais de um compilador, desde a tokenização da entrada até a construção da árvore de sintaxe abstrata (AST) e a geração de código de máquina de pilha para expressões.

## Como Executar

Este projeto foi desenvolvido em **Python 3**. Recomenda-se o uso de um ambiente virtual para gerenciar as dependências.

1.  **Clonar o repositório:**
    ```
    git clone https://github.com/fcte-compiladores/trabalho-final-trabalhofinal-com.git
    cd trabalho-final-trabalhofinal-com
    ```

2.  **Configurar e ativar o ambiente virtual (venv):**
    ```
    python3 -m venv venv
    source venv/bin/activate  # No Linux/macOS
    # Ou venv\Scripts\activate para Windows CMD/PowerShell
    ```

3.  **Rodar o compilador:**
    
    *   **Passando uma expressão direto na linha de comando:**
        ```
        python3 -m lox.main "10 + 2 * (3 - 1)"
        ```
    *   **Lendo de um arquivo de exemplo:**
        ```
        python3 -m lox.main -f exemplos/complexo.expr
        ```
    *   **No modo interativo (REPL):**
        ```
        python3 -m lox.main
        ```
        No prompt `>>> `, digite suas expressões e `sair` para finalizar.

## Como Testar o Projeto

Para verificar o funcionamento completo do compilador, você pode usar os exemplos e a suíte de testes unitários:

### Testando com Arquivos de Exemplo

A pasta `exemplos/` contém arquivos `.expr` com diversas expressões. Você pode executá-los para ver o resultado da análise léxica, sintática e geração de código:

*   **Exemplo de uso:**
    ```
    python3 -m lox.main -f exemplos/simples.expr
    ```

    Isso irá processar a expressão `5 + 3` e mostrar os tokens, a estrutura da AST e o código de máquina de pilha gerado.

### Rodando os Testes Unitários

Os testes unitários verificam o comportamento esperado do lexer e do parser de forma automatizada. Certifique-se de que o ambiente virtual está ativado antes de rodar os testes.

*   **Para testar o lexer (analisador léxico):**
    ```
    python3 -m unittest tests/test_lexer.py
    ```

*   **Para testar o parser (analisador sintático):**
    ```
    python3 -m unittest tests/test_parser.py
    ```

*   **Para rodar todos os testes de uma vez:**
    ```
    python3 -m unittest discover tests
    ```

    Após a execução, você verá um resumo indicando quantos testes passaram (`OK`) ou falharam (`FAILED`).

## Bugs/Limitações/Problemas Conhecidos

Este projeto é uma implementação inicial de um compilador, focada em demonstrar as fases básicas para **expressões aritméticas**. Suas principais limitações e pontos para melhoria futura incluem:

*   **Escopo da Linguagem:** Atualmente, o compilador suporta apenas operações aritméticas com números inteiros, adição, subtração, multiplicação, divisão e parênteses. Não há suporte para:
    *   Variáveis
    *   Atribuições
    *   Estruturas de controle de fluxo (condicionais como `if/else`, loops como `while/for`)
    *   Definição e chamada de funções
    *   Tipos de dados mais complexos (strings, booleanos, ponto flutuante)
*   **Análise Semântica:** O compilador não possui uma fase de análise semântica robusta para verificar erros de tipo, variáveis não declaradas ou outras inconsistências lógicas. Erros desse tipo passariam despercebidos até a fase de geração de código ou execução.
*   **Mensagens de Erro dos Testes do Parser:** Conforme observado nos testes unitários, os testes `test_missing_rparen_error` e `test_unexpected_token_error` no `tests/test_parser.py` estão atualmente comentados. Isso se deve a um problema na correspondência exata da mensagem de erro da exceção com a expressão regular do teste.
*   **Otimizações:** O código gerado para a máquina de pilha é uma tradução direta da AST e não inclui otimizações.
*   **Tratamento de Erros de Runtime:** Não há um interpretador para a máquina de pilha, então o código gerado não é executado, e erros de runtime (como divisão por zero) não são detectados.


