import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env, se existir
load_dotenv()

class Config:
    """Configurações base."""
    # Chave secreta para sessões, cookies, etc.
    SECRET_KEY = os.environ.get('SECRET_KEY', 'desenvolvimento-secreto')
    
    # Configurações do banco de dados
    # Usa PostgreSQL em produção e SQLite em desenvolvimento
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 
        'sqlite:///instance/database.db'
    )
    
    # Ajuste para o PostgreSQL do Render (caso o prefixo seja postgres://)
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Pasta para uploads de imagens
    UPLOAD_FOLDER = 'static/uploads'
    
    # Tamanho máximo para uploads (5MB)
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

class DevelopmentConfig(Config):
    """Configurações para ambiente de desenvolvimento."""
    DEBUG = True

class TestingConfig(Config):
    """Configurações para ambiente de testes."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/testing.db'
    
class ProductionConfig(Config):
    """Configurações para ambiente de produção."""
    DEBUG = False
    
    # Em produção, garantir que SECRET_KEY não seja o valor padrão
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # Configurações específicas para produção
    # Por exemplo, configurar servidor de e-mail, cache, etc.

# Configuração com base no ambiente
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# Obter a configuração a usar
def get_config():
    env = os.environ.get('FLASK_ENV', 'default')
    return config.get(env, config['default'])