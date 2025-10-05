# Uma interface para o projeto Scientific wRIGHTing
# Guia de incialização

## Quick Start

### Pré-requisitos

- Python 3.8+
- Node.js 16+
- MySQL/MariaDB

### 1. Clone o repositório

```bash
git clone <your-repository-url>
cd Scientific-wRIGHTing-Interface-main/Project_full_code
```

### 2. Setup do Backend

```bash
# Navegue para o Backend
cd backend

# Instale as dependências do Python
pip install -r requirements.txt

# Faça o setup do banco de dados
mysql -u root -p
CREATE DATABASE tcc_zilli CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit

# Carregue o schema
mysql -u root -p tcc_zilli < flaskr/schema.sql

# Inicie o servidor do Flask
python app.py
```

O Backend ficará disponível na URL `http://localhost:5000`

### 3. Setup do Frontend

```bash
# Navegue para o Frontend (em um novo terminal)
cd frontend/react-flask-app

# Instale as dependências do Node.js
npm install

# Inicie o servidor do React
npm start
```

O Frontend ficará disponível na URL `http://localhost:3000`

## Guia rápido da estrutura do projeto

```
Scientific-wRIGHTing-Interface-main/
├── backend/
│   ├── flaskr/
│   │   ├── __init__.py          # Criador da aplicação em Flask
│   │   ├── models.py            # Modelos do banco de dados
│   │   ├── schema.sql           # O schema do banco de dados
│   │   ├── views/
│   │   │   ├── index.py         # Página inicial e abstração da API
│   │   │   ├── analysis.py      # Endpoints da análise
│   │   │   └── resumo.py        # Individualização dos resumos
│   │   └── static/              # Arquivos estáticos do React
│   ├── app.py                   # Local de entrada da aplicação
│   ├── load_full_schema.py      # Script que carrega o banco de dados
│   └── requirements.txt         # Dependênciad do Python
├── frontend/
│   └── react-flask-app/
│       ├── src/
│       │   ├── components/
│       │   │   ├── BotoesResumos.jsx    # Home page da aplicação
│       │   │   ├── BotoesResumos.css    # Estilização da home page
│       │   │   ├── CaixaDialogo.jsx     # Código e lógica dos modais da aplicação
│       │   │   └── CaixaDialogo.css     # Estilização dos modais
│       │   ├── App.js                   # O componente do React
│       │   └── App.css                  # Estilização global
│       └── package.json                 # Dependências do Node.js
└── README.md                    # O arquivo que vos fala
```

## Licença de uso

This project is part of academic research. Please cite appropriately if used in research. (Texto pronto em inglês, quando o trabalho estiver publicado eu vou colocar o link aqui)

**Se você um dia usar essa aplicação, eu espero que ela atenda suas necessidades!**
