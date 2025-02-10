# Projeto Scrapper - Mercado Livre (Produtos de Computadores)

## Passos para rodar o projeto

### 1. Criar o ambiente virtual

#### Linux:

```bash
python3 -m venv venv
source venv/bin/activate #ativa o ambiente virtual
```

#### Windows:

```bash
python -m venv venv
.\venv\Scripts\activate #ativa o ambiente virtual
```
#### 2. Instalar dependências

Execute o comando abaixo para instalar as dependências do projeto:
```bash
pip install -r requirements.txt
```

> ℹ️ **Atenção:**  
> Para utilizar as variáveis de ambiente, renomeie o arquivo `.env.template` para `.env` e preencha os valores necessários antes de seguir as instruções do projeto.

#### 3. Subir o banco de dados com Docker e rodar migrações

Vai inicie o container Docker para o banco de dados e em seguida executar as migrações para configurar o banco de dados
```bash
task init
```

#### Rodar o projeto
Após as migrações, você pode rodar o projeto com o seguinte comando:
```bash
task run
```

## Módulos utilizados

- **Django**: >=4.0,<5.0 🚀
- **psycopg2-binary**: Para integração com o PostgreSQL 🐘
- **selenium**: >=4.0,<5: Usado para automação de testes e scraping. 🖥️
- **python-decouple**: Para gerenciamento de variáveis de ambiente 🌱
- **taskipy**: Para automação de tarefas 🔧