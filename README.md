# API de Autenticação com FastAPI

Este projeto é uma API de autenticação de usuários completa, desenvolvida como um item de portfólio para demonstrar habilidades em desenvolvimento de backend, DevOps e automação.

A API oferece endpoints para cadastro de novos usuários, login com JWT (JSON Web Token) e acesso a recursos protegidos. A infraestrutura e o processo de desenvolvimento são automatizados com ferramentas modernas.

## Tecnologias Utilizadas

* **Python:** A linguagem de programação principal, escolhida por sua simplicidade e poder para o desenvolvimento de APIs.
* **FastAPI:** Um framework web de alta performance para a criação da API, conhecido por sua velocidade e documentação automática.
* **PostgreSQL:** Um sistema de gerenciamento de banco de dados relacional robusto e confiável, usado para armazenar os dados dos usuários.
* **uv e pyproject.toml:** Ferramentas modernas de gerenciamento de dependências e ambiente virtual, proporcionando builds mais rápidos e uma gestão de pacotes mais organizada.
* **Docker:** Usado para containerizar a aplicação, garantindo que ela rode em qualquer ambiente de forma consistente.
* **GitHub Actions:** O coração do nosso pipeline de CI/CD (Integração e Entrega Contínuas), responsável por automatizar o build, teste e push da imagem Docker.
* **JWT (JSON Web Token):** O padrão de autenticação para a API, usado para gerar tokens de acesso seguros para usuários logados.


## Instalação e Execução Local

Siga estes passos para ter o projeto rodando em sua máquina local.

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/kbrum/api-autenticacao.git](https://github.com/kbrum/api-autenticacao.git)
    cd api-autenticacao
    ```

2.  **Configure o arquivo `.env`:**
    Crie um arquivo `.env` na raiz do projeto e adicione suas credenciais do banco de dados e a chave secreta.

    ```
    # Conteúdo do arquivo .env
    DATABASE_URL=postgresql://user:password@host:port/database
    SECRET_KEY=sua_chave_secreta_jwt_aqui
    ```

3.  **Instale as dependências:**
    Use o `uv` para criar um ambiente virtual e instalar todas as dependências do `pyproject.toml`.

    ```bash
    uv venv
    source .venv/bin/activate
    uv pip install .
    ```

4.  **Inicie a API:**
    Execute o comando abaixo para iniciar a aplicação com o Uvicorn.
    ```bash
    uvicorn main:app --reload
    ```
    A API estará acessível em `http://127.0.0.1:8000`.

## Endpoints da API

A API possui a seguinte lista de endpoints para interação. Você pode testá-los diretamente na documentação interativa em `http://127.0.0.1:8000/docs`.

* `GET /`: Endpoint de apresentação.
* `POST /cadastro`: Registra um novo usuário com nome de usuário e senha.
* `POST /login`: Autentica um usuário e retorna um token de acesso.
* `GET /showUser`: Rota protegida que retorna informações do usuário logado (requer um token de acesso válido).

## Automação com GitHub Actions

O projeto conta com um pipeline de **Integração Contínua (CI)** configurado com GitHub Actions. O workflow `ci-cd.yml` é executado automaticamente em cada `push` para o branch `dev` e realiza as seguintes tarefas:

1.  **Build da Imagem Docker:** Constrói uma imagem Docker da aplicação.
2.  **Login no Docker Hub:** Faz o login em sua conta do Docker Hub usando um Token de Acesso Pessoal (PAT) armazenado com segurança como um secret do GitHub.
3.  **Push para o Docker Hub:** Envia a imagem construída para o repositório do Docker Hub com duas tags: `latest` e o SHA do commit.

Este pipeline garante que a imagem da sua aplicação esteja sempre atualizada e pronta para ser i