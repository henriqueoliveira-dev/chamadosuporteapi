# API de Chamados de Suporte

API REST de estudo construída com FastAPI, SQLAlchemy assíncrono e MySQL. O repositório implementa cadastro/autenticação de usuários e operações CRUD de artigos de suporte; não há um recurso separado chamado `chamados` na versão atual.

## Tecnologias

- Python 3.10+
- FastAPI e Uvicorn
- SQLAlchemy assíncrono (`asyncmy`)
- MySQL
- Pydantic Settings para configuração

## Configuração local

1. Crie e ative um ambiente virtual, instale as dependências e copie o exemplo de configuração:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   ```

2. Edite `.env` com uma URL válida de conexão MySQL. Gere um segredo JWT exclusivo para este ambiente com:

   ```bash
   python -c 'import secrets; print(secrets.token_urlsafe(32))'
   ```

   Configure o valor gerado em `JWT_SECRET`. O aplicativo exige um segredo de pelo menos 32 caracteres e uma variável `DB_URL`; credenciais não devem ser adicionadas ao código nem versionadas. Codifique caracteres especiais da senha conforme as regras de URL.

3. Crie as tabelas e inicie a aplicação:

   ```bash
   python criar_tabelas.py
   uvicorn main:app --reload
   ```

   A API fica em `http://127.0.0.1:8000`; a documentação interativa fica em `/docs`.

`DB_ECHO` é opcional e assume `false`, evitando registrar consultas/parâmetros SQL por padrão. Use `true` somente em desenvolvimento controlado.

## Endpoints

Os endpoints estão sob `/api/v1`.

| Método | Caminho | Acesso | Descrição |
| --- | --- | --- | --- |
| `POST` | `/usuarios/signup` | Público | Cadastra usuário comum |
| `POST` | `/usuarios/login` | Público | Login OAuth2 por formulário (`username` recebe o e-mail) |
| `GET` | `/usuarios/logado` | Autenticado | Retorna a conta do token atual |
| `GET` | `/usuarios/` | Administrador | Lista usuários |
| `GET` | `/usuarios/{id}` | Próprio usuário/administrador | Consulta usuário e artigos |
| `PUT` | `/usuarios/{id}` | Próprio usuário/administrador | Atualiza dados; somente administrador altera privilégio |
| `DELETE` | `/usuarios/{id}` | Próprio usuário/administrador | Exclui usuário |
| `GET` | `/artigos/` | Público | Lista artigos |
| `GET` | `/artigos/{id}` | Público | Consulta artigo |
| `POST` | `/artigos/` | Autenticado | Cria artigo associado à conta autenticada |
| `PUT` | `/artigos/{id}` | Proprietário autenticado | Atualiza artigo sem transferir sua propriedade |
| `DELETE` | `/artigos/{id}` | Proprietário autenticado | Exclui artigo |

Use o botão **Authorize** em `/docs` com o access token. O endpoint de login espera `application/x-www-form-urlencoded`, conforme o fluxo OAuth2 Password usado pela documentação do FastAPI.

Usuários criados por signup não recebem privilégios administrativos. A promoção inicial de um administrador deve ser feita por um processo operacional confiável no banco de dados; não exponha credenciais de banco nem habilite privilégios no formulário público.

## Testes

Os testes unitários de schemas não exigem conexão com o banco:

```bash
python -m unittest discover -s tests -v
```

Ainda não há testes automatizados de integração com MySQL. As tabelas são criadas pelo script `criar_tabelas.py`; em produção, alterações de esquema devem ser planejadas/migradas sem depender de `create_all`.

## Estrutura principal

```text
api/v1/endpoints/   Rotas de artigos e usuários
core/               Configuração, sessão, autenticação e segurança
models/             Modelos ORM
schemas/             Schemas de entrada e saída
criar_tabelas.py     Criação inicial das tabelas
main.py              Instância FastAPI
```
