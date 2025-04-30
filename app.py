import os
from flask import Flask
from flask_cors import CORS
from models import db, EnvironmentalReport
from routes.api import api_bp
from routes.views import views_bp

def create_app(test_config=None):
    # Cria e configura a aplicação Flask
    app = Flask(__name__, instance_relative_config=True)
    
    # Configurações básicas
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'database.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        UPLOAD_FOLDER=os.path.join(app.static_folder, 'uploads'),
    )

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
    app.run(debug=True, host='0.0.0.0')