# Analisador Sintático de Matemágica

## Sobre

Trabalho realizado no quarto período de Ciência da Computação na disciplina INF1022, Analisadores Léxicos e Sintáticos, da PUC-RJ, ministrada pelo professor Vitor Pinheiro.

O trabalho consiste na criação de um analisador sintático capaz de compilar programas escritos utilizando a linguagem Matemágica para uma outra linguagem. Ou seja, o analisador recebe como entrada um programa na linguagem Matemágica (.mag) e produz como saída um outro programa escrito em outra linguagem, simulando um compilador.

A linguagem escolhida para o resultado da conversão foi Lua, pela alta compatibilidade entre sua sintaxe e a proposta para a linguagem Matemágica.

## Como utilizar

Clone o repositório ou extraia o zip baixado e abra a pasta do projeto em sua IDE.

O gerador de analisador sintático escolhido para o projeto foi a ferramenta [SLY (Sly Lex-Yacc)](https://github.com/dabeaz/sly), escrita em Python, que implementa o método LaLR(1) para parsing. Não é necessária qualquer instalação adicional além da pasta sly já incluída no projeto para utilizá-la.

É necessário apenas ter uma instalação válida de Python instalada no computador, editar o arquivo codigo.mag para conter o código que deve ser convertido, e executar main.py. A saída estará no arquivo programa.lua.

Para executar a saída, uma instalação válida de Lua também deve estar presente no ambiente de execução.

## A linguagem

A linguagem Matemágica proposta no projeto e adaptada durante a implementação tem a seguinte gramática:

```
programa → cmds

cmds → cmd cmds | cmd

cmd → atribuicao | impressao | operacao | repeticao | condicional | fim

atribuicao → FACA var SER num .| FACA var SER var .

impressao → MOSTRE var .| MOSTRE operacao .| MOSTRE num .

operacao → SOME var COM var .| SOME var COM num .| SOME num COM var .| SOME num COM num .|  
MULTIPLIQUE var POR var .| MULTIPLIQUE var POR num .| MULTIPLIQUE num POR var .| ㅤㅤㅤㅤㅤㅤMULTIPLIQUE num POR num .

repeticao → REPITA num VEZES : cmds FIM | REPITA var VEZES : cmds FIM

condicional → SE var ENTAO cmds SENAO cmds FIM | SE num ENTAO cmds SENAO cmds FIM |  
SE operacao ENTAO cmds SENAO cmds FIM | SE var MAIOR QUE num ENTAO cmds SENAO cmds FIM |  
SE var MAIOR QUE var ENTAO cmds SENAO cmds FIM | SE num MAIOR QUE var ENTAO cmds SENAO cmds FIM |  
SE num MAIOR QUE num ENTAO cmds SENAO cmds FIM | SE var MENOR QUE num ENTAO cmds SENAO cmds FIM |  
SE var MENOR QUE var ENTAO cmds SENAO cmds FIM | SE num MENOR QUE var ENTAO cmds SENAO cmds FIM |  
SE num MENOR QUE num ENTAO cmds SENAO cmds FIM

fim → FIM
```

Onde:
- Todas as variáveis são do tipo *inteiro e não negativo*.
- var só pode ser formado por *letras* e precisa ter *no mínimo uma letra*.
- num representa um número.
- O terminal SOME indica que deve ser feita uma soma e, MULTIPLIQUE, que deve ser feita uma multiplicação.
- O terminal . sinaliza o fim dos comandos de *atribuição, impressão e operação*.
- O terminal FIM sinaliza o fim de uma *repetição e de uma condicional*.
