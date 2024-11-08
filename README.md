<p align="center">
  <img src="https://github.com/gb-cs-rt/projeto_compiladores/blob/main/assets/banner.png" alt="Pystache Banner">
</p>

Pystache é uma linguagem de programação de alto nível projetada para ser acessível a programadores de todos os níveis de experiência. Com palavras-chave em português, a linguagem facilita o aprendizado para iniciantes.

## Principais Características
- **Linguagem em Português (PT-BR)**
- **Linguagem indentada** (indentação faz parte da gramática)
- **Variados tipos de iteradores**
- **Tipagem implícita** (realiza auto-casting)
- **Controle de escopo**
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
- ```pystache <nome_do_arquivo.pyst> -hash``` - Exibe o dicionário de tipos atribuídos às variáveis.

## Expressões Regulares
```id: [a-zA-Z_][a-zA-Z0-9_]*```<br>
```number: [0-9]+```<br>
```double: [0-9]*.[0-9]+```<br>
```string: "[a-zA-Z0-9_+-*/@=^<>!,.&()[]%$#&~...]*```<br>
```bool: verdadeiro | falso```<br>
```plus: +```<br>
```minus: -```<br>
```div: /```<br>
```div_int: //```<br>
```mod: %```<br>
```pow: ^```<br>
```assign: :```<br>
```plus_assign: +:```<br>
```minus_assign: -:```<br>
```mult_assign: *:```<br>
```div_assign: /:```<br>
```div_int_assign: //:```<br>
```mod_assign: %:```<br>
```pow_assign: ^:```<br>
```greater: >```<br>
```less: <```<br>
```greater_equal: >=```<br>
```less_equal: <=```<br>
```equals: =```<br>
```different: !=```<br>
```and: &```<br>
```or: |```<br>
```open_bracket: [```<br>
```close_bracket: ]```<br>
```open_parenthesis: (```<br>
```close_parenthesis: )```<br>
```comma: ,```<br>
```reserved_se: se```<br>
```reserved_entao: entao```<br>
```reserved_exiba: exiba```<br>
```reserved_senao: senao```<br>
```reserved_repita: repita```<br>
```reserved_vezes: vezes```<br>
```reserved_de: de```<br>
```reserved_ate: ate```<br>
```reserved_sendo: sendo```<br>
```reserved_enquanto: enquanto```<br>
```reserved_funcao: funcao```<br>
```reserved_retorne: retorne```<br>
```reserved_entrada: entrada```<br>
```reserved_passe: passe```<br>
```reserved_pare: pare```<br>
```reserved_passo: passo```<br>
```eof: $```

## Gramática
```prog -> bloco```<br>
```bloco -> cmd bloco | ε```<br>
```cmd -> cmdID | cmdIf | cmdFor | cmdWhile | cmdReturn | cmdDefFunc | cmdPrint | cmdInput | <reserved_passe> | <reserved_pare>```<br>
```cmdID -> ID acessoListaOp complemento```<br>
```cmdIf -> <reserved_se> valor <reserved_entao> <indent> bloco <dedent> cmdElse```<br>
```cmdElse -> <reserved_senao> <indent> bloco <dedent> | ε```<br>
```complemento -> cmdAtrib | composicao```<br>
```cmdAtrib -> atribComum | atribComOp```<br>
```atribComum -> <assign> valor```<br>
```atribComOp -> assignOp valor```<br>
```assignOp -> <plus_assign> | <minus_assign> | <mult_assign> | <div_assign> | <div_int_assign> | <mod_assign> | <pow_assign>```<br>
```composicao -> acessoLista | chamadaFuncao```<br>
```acessoLista -> <open_bracket> expressaoAritmetica <close_bracket>```<br>
```chamadaFuncao -> <open_parenthesis> corpoLista <close_parenthesis>```<br>
```acessoListaOp -> acessoLista | ε```<br>
```valor -> expressaoLogica | lista | cmdPrint | cmdInput```<br>
```expressaoLogica -> expressaoRelacional (opLogico expressaoRelacional)*```<br>
```opLogico -> <and> | <or>```<br>
```expressaoRelacional -> expressaoAritmetica (opRelacional expressaoAritmetica)*```<br>
```opRelacional -> <greater> | <less> | <equals> | <different> | <greater_equal> | <less_equal>```<br>
```expressaoAritmetica -> termo (opAd termo)*```<br>
```opAd -> <plus> | <minus>```<br>
```termo -> fator (opMul fator)*```<br>
```opMul -> <mult> | <div> | <div_int> | <mod>```<br>
```fator -> elemento (opPow elemento)*```<br>
```opPow -> <pow>```<br>
```elemento -> <num> | <double> | <id> X | <open_parenthesis> expressaoLogica <close_parenthesis> | <string> | <bool>```<br>
```X -> composicao | ε```<br>
```lista -> <open_bracket> corpoLista <close_bracket>```<br>
```corpoLista -> valor entradaLista | ε```<br>
```entradaLista -> <comma> valor entradaLista | ε```<br>
```cmdFor -> <reserved_repita> variavelFor <indent> bloco <dedent>```<br>
```variavelFor -> forVezes | forIntervalo | forSendo```<br>
```forVezes -> expressaoAritmetica <reserved_vezes>```<br>
```forIntervalo -> <reserved_de> expressaoAritmetica <reserved_ate> expressaoAritmetica passoFor```<br>
```passoFor -> <reserved_passo> expressaoAritmetica | ε```<br>
```forSendo -> <reserved_sendo> <id> forIntervalo```<br>
```cmdWhile -> <reserved_enquanto> valor <indent> bloco <dedent>```<br>
```cmdDefFunc -> <reserved_funcao> <id> <open_parenthesis> listaParametros <close_parenthesis> <indent> bloco <dedent>```<br>
```listaParametros -> <id> entradaListaParam | ε```<br>
```entradaListaParam -> <comma> <id> entradaListaParam | ε```<br>
```cmdReturn -> <reserved_retorne> valorRetorno```<br>
```valorRetorno -> valor | ε```<br>
```cmdPrint -> <reserved_exiba> <open_parenthesis> corpoLista <closeParenthesis>```<br>
```cmdInput -> <reserved_entrada> <open_parenthesis> corpoLista <closeParenthesis>```
