# EnviroMap - Mapeamento Ambiental Participativo

EnviroMap é uma plataforma web de mapeamento participativo que permite aos cidadãos reportar e visualizar problemas ambientais em suas comunidades e nasceu por conta da minha atividade de extensão da faculdade. O projeto combina tecnologia acessível com participação comunitária para enfrentar desafios ambientais locais.

## 📋 Visão Geral

EnviroMap representa uma inovação social que capacita os cidadãos a se tornarem agentes ativos na proteção do meio ambiente e da saúde pública. Ao criar um sistema de mapeamento colaborativo, o projeto:

- Documenta problemas ambientais locais como queimadas, desmatamento e poluição
- Catalisa processos de conscientização, mobilização e transformação social
- Serve como ferramenta de cidadania ambiental para visualizar, compreender e atuar sobre desafios territoriais
- Supera barreiras educacionais e digitais com uma interface intuitiva e acessível

O caráter inovador está em sua abordagem inclusiva e na combinação de tecnologia com estratégias de comunicação acessíveis, construindo pontes entre o mundo digital e a realidade concreta das comunidades.

## 🚀 Funcionalidades

- **Mapa Interativo**: Visualização geográfica de todos os relatos ambientais
- **Formulário de Relatos**: Interface simples para reportar problemas ambientais
- **Filtros Avançados**: Busca por tipo de problema, severidade e data
- **Dashboard Analítico**: Visualização de estatísticas e tendências dos dados coletados
- **API RESTful**: Integração com outros sistemas e aplicações

## 💻 Tecnologias

- **Backend**: Python, Flask, SQLAlchemy
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Mapas**: Leaflet.js
- **Banco de Dados**: SQLite (desenvolvimento), compatível com PostgreSQL (produção)
- **Implantação**: Preparado para Docker e serviços de hospedagem como Heroku

## ⚙️ Instalação e Configuração

### Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes do Python)
- Git

### Clonando o Repositório

```bash
git clone https://github.com/seu-usuario/mapeamento-participativo.git
cd mapeamento-participativo
```

### Configurando o Ambiente Virtual

```bash
# Criando ambiente virtual
python -m venv venv

# Ativando ambiente virtual (Windows)
venv\Scripts\activate

# Ativando ambiente virtual (Linux/macOS)
source venv/bin/activate

# Instalando dependências
pip install -r requirements.txt
```

### Configurando Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```
FLASK_ENV=development
SECRET_KEY=seu-segredo-aqui
DATABASE_URL=sqlite:///instance/database.db
```

### Inicializando o Banco de Dados

```bash
flask run
```

O banco de dados será criado automaticamente na primeira execução.

## 🏃‍♂️ Executando o Projeto

```bash
# Em modo de desenvolvimento
flask run

# Em modo de produção
gunicorn app:create_app()
```

Por padrão, a aplicação estará disponível em `http://127.0.0.1:5000`

## 📁 Estrutura do Projeto

```
mapeamento-participativo/
├── app.py                  # Configuração principal da aplicação
├── config.py               # Configurações do ambiente
├── models.py               # Modelos do banco de dados
├── requirements.txt        # Dependências do projeto
├── routes/                 # Rotas da aplicação
│   ├── __init__.py
│   ├── api.py              # API RESTful
│   └── views.py            # Rotas para renderização de templates
├── static/                 # Arquivos estáticos
│   ├── css/
│   ├── img/
│   ├── js/
│   └── uploads/            # Imagens enviadas pelos usuários
└── templates/              # Templates HTML
    ├── base.html
    ├── dashboard.html
    ├── index.html
    └── report.html
```

## 🔄 Fluxo de Trabalho

1. **Reportar Problema**:
   - Usuário acessa o formulário de relato
   - Preenche detalhes do problema (título, tipo, severidade)
   - Marca a localização no mapa
   - Opcional: envia uma foto e seus contatos
   - Submete o relato

2. **Visualizar Problemas**:
   - Usuário acessa o mapa interativo
   - Filtra por tipo, severidade ou data se necessário
   - Clica em marcadores para ver detalhes
   - Acessa dashboard para análises e estatísticas

## 🌐 API RESTful

O EnviroMap disponibiliza uma API para integração com outros sistemas:

- `GET /api/reports` - Lista todos os relatos
- `GET /api/reports/<id>` - Obtém detalhes de um relato específico
- `POST /api/reports` - Cria um novo relato
- `PUT /api/reports/<id>` - Atualiza um relato existente
- `DELETE /api/reports/<id>` - Remove um relato
- `GET /api/reports/types` - Lista tipos de problemas e suas contagens

## 📊 Dashboard

O sistema inclui um dashboard analítico que apresenta:

- Total de relatos cadastrados
- Distribuição por tipo de problema
- Distribuição por nível de severidade
- Visualização dos relatos mais recentes

## 🤝 Como Contribuir

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Faça commit das alterações (`git commit -m 'Adiciona nova funcionalidade'`)
4. Envie para o repositório original (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📞 Contato

Gabriel Lopes - gabriellopes.ct07@gmail.com

---

EnviroMap - Mapeamento Ambiental Participativo © 2025
