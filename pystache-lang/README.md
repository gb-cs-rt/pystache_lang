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
   git clone https://github.com/gb-cs-rt/pystache_lang.git
   cd pystache_lang

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
