import os
from flask import Flask
from flask_cors import CORS
from models import db, EnvironmentalReport
from routes.api import api_bp
from routes.views import views_bp
from config import ProductionConfig, DevelopmentConfig

def create_app(test_config=None):
    # Cria e configura a aplicação Flask
    app = Flask(__name__, instance_relative_config=True)
    
    # Verifica o ambiente para selecionar a configuração adequada
    env = os.environ.get('FLASK_ENV', 'development')
    
    # Configurações com base no ambiente
    if env == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)
    
    # Garante que a pasta instance existe
    try:
        os.makedirs(app.instance_path)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    except OSError:
        pass

    # Inicializa extensões
    CORS(app)  # Permite requisições cross-origin
    db.init_app(app)
    
    # Registra blueprints
    app.register_blueprint(api_bp)
    app.register_blueprint(views_bp)
    
    # Cria as tabelas do banco de dados
    with app.app_context():
        db.create_all()
    
    @app.route('/health')
    def health_check():
        """Endpoint simples para verificar se a aplicação está funcionando."""
        return {'status': 'ok'}
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)