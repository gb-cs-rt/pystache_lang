<p align="center">
  <img src="https://github.com/gb-cs-rt/projeto_compiladores/blob/main/assets/banner.png" alt="Pystache Banner">
</p>

Pystache é uma linguagem de programação de alto nível projetada para ser acessível a programadores de todos os níveis de experiência. Com palavras-chave em português, a linguagem facilita o aprendizado para iniciantes.

## Principais Características
- **Linguagem em Português (PT-BR)**
- **Linguagem com indentação**
- **Variados tipos de iteradores**
- **Tipagem implícita** (realiza auto-casting)
- **Extensão para o VSCode**, que simplifica o uso da linguagem

## Primeiros Passos

### Sistemas Operacionais Suportados
- ![Ubuntu 22 Shield](https://img.shields.io/badge/Ubuntu-22.04-orange)

### Pré-requisitos
- **G++**
- **Python 3.10** ou mais recente
- **Git**
- **VSCode** (caso deseje utilizar a extensão)

### Instalação
1. Clone o repositório:
   ```bash
   git clone https://github.com/gb-cs-rt/projeto_compiladores

2. Conceda permissão de execução e rode o script de instalação:
   ```bash
   chmod +x install.sh && ./install.sh

3. Crie um arquivo com a extensão ```.pyst``` e execute o compilador:
   ```bash
   pystache <nome_do_arquivo.pyst>

### Extensão para VSCode
1. Acesse o Marketplace de extensões do VSCode e pesquise por **Pystache**.
2. Instale a extensão e abra um arquivo com a extensão ```.pyst```. A extensão fornece:
- Syntax highlighting específico para a linguagem
- Atalho para compilar e rodar o código rapidamente (necessário ter a linguagem instalada)
- Tema de cor personalizado

## Opções adicionais

### Flags
- ```pystache <nome_do_arquivo.pyst> -tree``` - Exibe a árvore sintática do código fonte.
- ```pystache <nome_do_arquivo.pyst> -tokens``` - Exibe a lista de tokens reconhecidos no código fonte.

## Expressões Regulares
- id:
```
[a-z A-Z _][a-z A-Z 0-9 _]*
```
- Assign:
```
":"  
```
- Number:
```
[0-9]+
```
- Double:
```
[0-9]*"."[0-9]+
```
- String:
```
""" [a-z A-Z 0-9 _ + - * / @ = ^ < > ! , . **etc**]*"
```
- open_bracket:
```
"["
```
- close_bracket:
```
"]"
```
- comma:
```
","
```
- reserved_se:
```
"se"
```
- greater:
```
">"
```
- less:
```
"<"
```
- reserved_entao:
```
"entao"
```
- reserved_exiba:
```
"exiba"
```
- open_parenthesis:
```
"("
```
- close_parenthesis:
```
")"
```
- reserved_senao:
```
"senao"
```
- reserved_repita:
```
"repita"
```
- reserved_vezes:
```
"vezes"
```
- reserved_de:
```
"de"
```
- reserved_ate:
```
"ate"
```
- reserved_sendo:
```
"sendo"
```
- reserved_enquanto:
```
"enquanto"
```
- reserved_funçao:
```
"funçao"
```
- reserved_retorne:
```
"retorne"
```
- reserved_entrada:
```
"entrada"
```
- plus:
```
"+"
```
- minus:
```
"-"
```
- mult:
```
"*"
```
- div:
```
"/"
```
- div_int:
```
"//"
```
- mod:
```
"%"
```
- pow:
```
"^"
```
- grater_equal:
```
">="
```
- less_equal:
```
"<="
```
- equals:
```
"="
```
- different:
```
"!="
```
- and:
```
"&"
```
- or:
```
"|"
```
- not:
```
"!"
```
- plus_assign:
```
"+:"
```
- minus_assign:
```
"-:"
```
- mult_assign:
```
"*:"
```
- div_assign:
```
"/:"
```
- div_int_assign:
```
"//:"
```
- mod_assign:
```
"%:"
```
- pow_assign:
```
"^:"
```
- reserved_passe:
```
"passe"
```
- reserved_pare:
```
"pare"
```
- reserved_passo:
```
"passo"
```
- eof:
```
"$"
```
- reserved_senao:
```
"senao"
```

## Gramática

prog -> bloco

bloco -> cmd bloco | ε

cmd -> cmdIf | cmdFor | cmdWhile | cmdAtrib | cmdDefFunc | cmdCallFunc | cmdPrint | cmdInput | cmdReturn | <reserved_passe> | <reserved_pare>

cmdIf -> <reserved_se> valor <reserved_entao>
<indent> bloco <dedent> cmdElse

cmdElse -> expressaoLogica | lista | cmdPrint | cmdCallFunc | acessoLista

expressaoLogica -> expressaoRelacional(opLogico expressaoRelacional)

expressaoRelacional -> expressaoAritimetica(opRelacional expressaoAritimetica)*

opAd -> <plus>|<minus>

opLogico -> <and>|<or>

opRelacional -> <greater> | <less> | <greater_equal> | <less_equal> | <equals> | <different>

termo -> fator(opMul fator)*

elemento -> <number> | <double> | <id> | <open_parenthesis> expressaoLogica <close_parenthesis> | <string> | <bool>

lista -> <open_bracket> corpoLista <close_bracket>

corpoLista -> valor entradaLista | ε

entradaLista -> <comma> valor entradaLista | ε

cmdAtrib -> <id> tipoAtrib

tipoAtrib -> atribComum | atribComOp

atribComum -> <assign> valor

atribComOp -> assignOp valor

assignOp -> <plus_assign> | <minus_assign> | <mult_assign> | <div_assign> | <div_int_assign> | <mod_assign> | <pow_assign>

cmdFor -> <reserved_repita> variavelFor <ident> bloco <dedent>

variavelFor -> forVezes | forIntervalor | forSendo

forVezes -> expressaoAritimetica <reserved_vezes>

forIntervalo -> <reserved_de> expressaoAritimetica <reserved_ate> expressaoAritimetica passoFor

passoFor -> <reserved_passo> expressaoAritimetica | ε

forSendo -> <reserved_sendo> <id> forIntervalo

cmdWhile -> <reserved_funcao> <id> <open_parenthesis> listaParametros <close_parenthesis> <ident> bloco <dedent>

listaParametros -> <id> entradaListaParam | ε

entradaListaParam -> <comma> <id> entradaListaParam | ε

valorRetorno -> valor | ε

cmdCallFunc -> <id> <open_parenthesis> corpoLista <close_parenthesis>

acessoLista -> <id> <open_bracket> expressaoAritimetica <close_bracket>

cmdPrint -> <reserved_exiba> <open_parenthesis> corpoLista <close_parenthesis>

cmdInput -> <reserved_entrada> <open_parenthesis> corpoLista <close_parenthesis>
