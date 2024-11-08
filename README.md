<p align="center">
  <img src="https://github.com/gb-cs-rt/projeto_compiladores/blob/main/assets/banner.png" alt="Pystache Banner">
</p>

Pystache é uma linguagem de programação de alto nível desenvolvida como projeto da disciplina de Compiladores (CC6252) do Centro Universitário FEI. Foi projetada para facilitar o aprendizado de iniciantes e, ao mesmo tempo, ser conveniente para programadores de todos os níveis de experiência.

## Principais Características
- **Linguagem com _keywords_ em português**
- **Linguagem indentada** (indentação faz parte da gramática)
- **Variados tipos de laços de repetição**
- **Tipagem implícita** (realiza auto-casting)
- **Controle de escopo**
- **Geração de código intermediário em C++**
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
   git clone https://github.com/gb-cs-rt/pystache_lang.git
   cd pystache_lang

2. Conceda permissão de execução e rode o script de instalação:
   ```bash
   chmod +x install.sh && ./install.sh

3. Crie um arquivo com a extensão ```.pyst``` e execute o compilador:
   ```bash
   pystache <nome_do_arquivo.pyst>

### Extensão para VSCode
1. Acesse o Marketplace de extensões do VSCode e pesquise por **Pystache Lang**.
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

## Exemplos e Equivalência

### Declaração de variável
- Pystache
```
a: 1
b: 2.5
texto: "Olá, mundo!"
lista: [1, 2, 3]
```

- C++
```cpp
int a = 1;
double b = 2.5;
string texto = "Olá, mundo!";
vector<int> lista = {1,2,3};
```

### Entrada de Dados
- Pystache
```
n1: entradaNumero("Insira um número inteiro: ")
n2: entradaReal("Insira um número real: ")
n3: entrada("Insira um texto: ")
```

- C++
```cpp
int n1 = entradaNumero("Insira um número inteiro: ");
double n2 = entradaReal("Insira um número real: ");
string n3 = userInput("Insira um texto: ");
// obs: funções pré-declaradas no código traduzido.
```

### Saída de Dados
- Pystache
```
exiba("O valor de n3 é %s\n", n3)
```

- C++
```cpp
printf("O valor de n3 é %s\n", n3.c_str());
```


### Operações Aritméticas
- Pystache
```
soma: a + b
subtracao: a - b
multiplicacao: a * b
divisao: a / b
divisaoInteira: a // b
modulo: a % 2
potencia: a ^ b
```

- C++
```cpp
double soma = a + b;
double subtracao = a - b;
double multiplicacao = a * b;
double divisao = a / (float)b;
double divisaoInteira = a / b;
int modulo = a % 2;
double potencia = pow(a, b);
```

### Operações Relacionais
- Pystache
```
igual: a = b
diferente: a != b
maior: a > b
menor: a < b
maiorIgual: a >= b
menorIgual: a <= b
```

- C++
```cpp
double igual = a == b;
double diferente = a != b;
double maior = a > b;
double menor = a < b;
double maiorIgual = a >= b;
double menorIgual = a <= b;
```

### Atribuição com Operação
- Pystache
```
a +: 1
a -: 1
a *: 2
a /: 2
a //: 2
a %: 2
a ^: 2
```

- C++
```cpp
a += 1;
a -= 1;
a *= 2;
a /= 2;
a = (int)a / 2;
a %= 2;
a = pow(a,2);
```

### Estrutura de Controle _se senão_
- Pystache
```
se a > b entao
    exiba("a é maior que b\n")
senao
    exiba("b é maior que a\n")
```

- C++
```cpp
if (a > b) {
    printf("a é maior que b\n");
} else {
    printf("b é maior que a\n\n");
};
```

### Laço de repetição _repita "n" vezes_
- Pystache
```
repita 10 vezes
    exiba("essa é a repetição número %d\n", x1)

    se x1 = 5 entao
        pare
```

- C++
```cpp
for (int x1 = 0; x1 < 10; x1++)  {
    printf("essa é a repetição número %d\n",x1);

    if (x1 == 5) {
        break;
    };
};
// obs: xN é a variável interna utilizada nos laços com variável implícita
```

### Laço de repetição _repita de "a" ate "b"_
- Pystache
```
repita de 0 ate n1
    exiba("essa é a repetição número %d\n", x1)

repita de 0 ate 10 passo 2
    exiba("essa é a repetição número %d\n", x1)
```

- C++
```cpp
for (int x1 = 0; x1 < 10; x1++)  {
    printf("essa é a repetição número %d\n",x1);
};

for (int x1 = 0; x1 <= 10; x1 = x1 + 2) {
    printf("essa é a repetição número %d\n",x1);
};
```

### Laço de repetição _repita sendo "i" de "a" ate "b"_
- Pystache
```
repita sendo i de 0 ate 10
    exiba("essa é a repetição número %d\n", i)
```

- C++
```cpp
for (int i = 0; i <= 10; i++) {
    printf("essa é a repetição número %d\n",i);
};
```

### Laço de repetição _enquanto_
- Pystache
```
enquanto a < n1
    exiba("a é menor que 10\n")
    a +: 1

    se a = (n1-1) entao
        exiba("fim.\n\n")
```

- C++
```cpp
while (a < n1) {
    printf("a é menor que 10\n");
    a+=1;

    if (a == (n1-1)) {
        printf("fim.\n\n");
    };
};
```

### Declaração de função
- Pystache
```
funcao soma(a, b)
    retorne a + b

resultado: soma(1, 2)

funcao ping()
    exiba("pong\n")

ping()
```

- C++
```cpp
double soma(int a, int b) {
    return a + b;
};

void ping() {
    printf("pong\n");
};

int main() {
    double resultado = soma(1,2);
    ping();

    return 0;
}
// obs: funções só podem receber inteiros como argumento, e sempre retornam double.
```

### Acesso à lista
- Pystache
```
a: lista[0]
lista[0]: 10

repita sendo i de 0 ate 2
    exiba("O elemento %d da lista é %d\n", i, lista[i])
```

- C++
```cpp
int a = lista[0];
lista[0] = 10;

for (int i = 0; i <= 2; i++) {
    printf("O elemento %d da lista é %d\n", i, lista[i]);
};
```

## Componentes do Grupo
- Cauan Sousa > 24.124.084-5
- Gustavo Bagio > 24.122.012-8
- Ruan Turola > 24.122.050-8