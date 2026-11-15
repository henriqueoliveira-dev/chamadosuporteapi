# 📋 Chamados de Suporte API

API REST desenvolvida em **Python com FastAPI** para gerenciamento de chamados de suporte técnico.

O projeto foi desenvolvido com o objetivo de praticar a construção de uma API completa, trabalhando conceitos de **rotas, operações CRUD, banco de dados relacional, ORM, validação de dados, organização de projeto e testes de endpoints**.

---

## 🚀 Tecnologias utilizadas

- **Python 3.10+**
- **FastAPI**
- **SQLModel**
- **MySQL**
- **Uvicorn**
- **Git / GitHub**
- **Thunder Client** para testes da API

---

## 🎯 Objetivo do projeto

O sistema permite o gerenciamento de chamados de suporte técnico.

Cada chamado possui informações como:

- Título
- Descrição
- Status
- Prioridade
- Identificador único

A API foi construída seguindo o padrão REST, permitindo que os recursos sejam manipulados através de requisições HTTP.

---

# 🏗️ Estrutura da aplicação

A aplicação utiliza o FastAPI como framework principal e o SQLModel para trabalhar com o banco de dados.

Fluxo simplificado:

```text
Cliente
   │
   │ Requisição HTTP
   ▼
FastAPI
   │
   ├── Rotas
   ├── Validação dos dados
   └── Regras da aplicação
          │
          ▼
       SQLModel
          │
          ▼
        MySQL
```

---

# 📌 Funcionalidades

A API possui operações para gerenciamento dos chamados:

| Método | Operação  | Descrição                       |
| ------ | --------- | ------------------------------- |
| GET    | Listar    | Retorna os chamados cadastrados |
| GET    | Buscar    | Consulta um chamado específico  |
| POST   | Criar     | Cadastra um novo chamado        |
| PUT    | Atualizar | Atualiza um chamado existente   |
| DELETE | Excluir   | Remove um chamado               |

Essas operações representam as principais operações de um CRUD:

```text
Create → POST
Read   → GET
Update → PUT
Delete → DELETE
```

---

# 🗄️ Banco de dados

O projeto utiliza **MySQL** para armazenamento persistente dos chamados.

A tabela principal utilizada pela aplicação é:

```text
chamados_suporte
```

Os registros possuem informações semelhantes a:

```text
id
titulo
descricao
status
prioridade
```

O banco de dados permite que os chamados permaneçam armazenados mesmo após o encerramento da aplicação.

---

# 🧱 SQLModel

O **SQLModel** é utilizado para representar os dados da aplicação através de classes Python.

A ideia é utilizar um modelo que represente a estrutura dos registros armazenados no banco.

Exemplo conceitual:

```python
class Chamado(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    titulo: str
    descricao: str
    status: str
    prioridade: str
```

### O que esse modelo representa?

```text
Chamado
   │
   ├── id          → identificador do chamado
   ├── titulo      → título do problema
   ├── descricao   → descrição detalhada
   ├── status      → situação do chamado
   └── prioridade  → nível de prioridade
```

O SQLModel utiliza essas informações para trabalhar com os registros do banco de dados.

---

# ⚡ FastAPI

O FastAPI é responsável por receber as requisições HTTP e direcioná-las para as operações correspondentes.

Por exemplo:

```text
POST /chamados
```

representa uma solicitação para criar um novo chamado.

Enquanto:

```text
GET /chamados
```

é utilizada para consultar os chamados cadastrados.

A documentação automática disponibilizada pelo FastAPI também facilita os testes e a compreensão dos endpoints.

---

# 🔄 Exemplo de criação de chamado

Uma requisição `POST` pode enviar informações semelhantes a:

```json
{
    "titulo": "Computador não inicia",
    "descricao": "O computador apresenta erro ao iniciar o sistema.",
    "status": "Aberto",
    "prioridade": "Alta"
}
```

A aplicação recebe os dados, realiza a validação e registra o chamado no banco de dados.

Uma resposta de sucesso pode retornar informações como:

```json
{
    "id": 1,
    "titulo": "Computador não inicia",
    "descricao": "O computador apresenta erro ao iniciar o sistema.",
    "status": "Aberto",
    "prioridade": "Alta"
}
```

O `id` é gerado para identificar o registro no banco de dados.

---

# 🧪 Testes da API

Durante o desenvolvimento, os endpoints foram testados utilizando o **Thunder Client**.

Foram realizadas requisições utilizando diferentes métodos HTTP:

```text
GET
POST
PUT
DELETE
```

Esses testes permitiram verificar o funcionamento das operações da API e a comunicação com o banco de dados.

---

# 📁 Organização do projeto

A estrutura pode ser representada de forma geral como:

```text
secao06/
│
├── .venv/
│
├── main.py
├── requirements.txt
├── criar_tabelas.py
└── README.md
```

### `main.py`

Arquivo principal da aplicação.

Responsável pela inicialização da API, definição das rotas e execução da aplicação FastAPI.

### `criar_tabelas.py`

Utilizado para preparar as tabelas necessárias no banco de dados.

### `requirements.txt`

Arquivo que registra as principais dependências utilizadas pelo projeto.

Exemplo:

```text
fastapi
mysql-connector-python
sqlmodel
uvicorn
```

### `.venv`

Ambiente virtual utilizado para isolar as dependências do projeto.

O ambiente virtual **não deve ser enviado para o GitHub**.

---

# ▶️ Como executar o projeto localmente

## 1. Clonar o repositório

```bash
git clone git@github.com:henriqueoliveira-dev/chamadosuporteapi.git
```

Entrar no diretório:

```bash
cd chamadosuporteapi
```

---

## 2. Criar o ambiente virtual

No Linux:

```bash
python3 -m venv .venv
```

Ativar utilizando Fish:

```bash
source .venv/bin/activate.fish
```

---

## 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

---

## 4. Configurar o banco de dados

O MySQL deve estar instalado e em execução.

As configurações de conexão devem ser ajustadas de acordo com o ambiente utilizado.

> Recomenda-se não armazenar senhas ou credenciais diretamente no código-fonte.

---

## 5. Criar as tabelas

Executar:

```bash
python criar_tabelas.py
```

---

## 6. Executar a API

```bash
uvicorn main:app --reload
```

A aplicação ficará disponível localmente em:

```text
http://127.0.0.1:8000
```

A documentação interativa pode ser acessada através de:

```text
http://127.0.0.1:8000/docs
```

---

# 📚 Documentação automática

O FastAPI disponibiliza uma interface interativa para testar os endpoints.

A documentação pode ser acessada em:

```text
/docs
```

Nessa interface é possível visualizar as rotas disponíveis, seus métodos HTTP, parâmetros e modelos utilizados pela API.

---

# 🌐 Deploy — visão geral

O projeto atualmente é executado em ambiente local.

Caso seja necessário disponibilizar a API na internet, a aplicação poderá ser implantada em um servidor Linux, como uma VPS.

Um fluxo de deploy profissional poderia seguir esta arquitetura:

```text
GitHub
   │
   │ Código da aplicação
   ▼
Servidor Linux
   │
   ├── Python
   ├── Ambiente virtual
   ├── FastAPI
   ├── Uvicorn
   └── MySQL
        │
        ▼
      Nginx
        │
        ▼
      HTTPS
        │
        ▼
   API disponível
   pela internet
```

De forma resumida, o processo envolveria:

1. Criar uma máquina virtual Linux.
2. Configurar acesso SSH.
3. Clonar o projeto do GitHub.
4. Instalar Python e as dependências.
5. Configurar o banco de dados.
6. Executar a aplicação FastAPI.
7. Utilizar um servidor de aplicação adequado para produção.
8. Configurar o Nginx como proxy reverso.
9. Configurar HTTPS e certificado SSL.
10. Monitorar a aplicação e o servidor.

> **Observação:** o deploy descrito acima é uma visão arquitetural para uma futura implantação. Este repositório não considera o deploy como concluído.

---

# 🔐 Segurança

Em um ambiente de produção, informações sensíveis não devem ser armazenadas diretamente no código ou no repositório.

Entre elas:

```text
Senhas
Chaves de API
Credenciais do banco
Tokens
Informações privadas
```

Uma abordagem adequada seria utilizar **variáveis de ambiente** ou um sistema de gerenciamento de segredos.

---

# 📈 Possíveis melhorias futuras

O projeto pode ser evoluído posteriormente com funcionalidades como:

- Autenticação de usuários
- Controle de permissões
- Filtros de chamados
- Paginação
- Busca por status e prioridade
- Relacionamento entre usuários e chamados
- Histórico de alterações
- Logs da aplicação
- Testes automatizados
- Docker
- Deploy em servidor Linux
- HTTPS
- Integração com serviços externos

Essas funcionalidades não fazem parte necessariamente da versão atual e podem ser adicionadas conforme a evolução do projeto.

---

# 👨‍💻 Sobre o projeto

Este projeto faz parte dos estudos de desenvolvimento de sistemas e foi desenvolvido com foco no aprendizado prático de **Python, APIs REST, FastAPI, banco de dados e integração entre aplicação e infraestrutura**.

O objetivo principal é demonstrar a evolução prática na construção de uma aplicação backend, desde a criação das rotas até a persistência dos dados em banco de dados relacional.

---

## 📌 Status

**Projeto funcional em ambiente local.**

### Implementado

- [x] API REST
- [x] FastAPI
- [x] CRUD de chamados
- [x] MySQL
- [x] SQLModel
- [x] Validação dos dados
- [x] Testes dos endpoints
- [x] Documentação automática do FastAPI
- [x] Versionamento com Git
- [x] Repositório no GitHub

### Planejado / futuro

- [ ] Testes automatizados
- [ ] Autenticação
- [ ] Docker
- [ ] Deploy em servidor Linux
- [ ] HTTPS
- [ ] Monitoramento

---

## 📄 Licença

Este projeto foi desenvolvido para fins de estudo e portfólio.
