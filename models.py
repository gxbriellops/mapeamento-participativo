from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class EnvironmentalReport(db.Model):
    """Modelo para armazenar relatos de problemas ambientais."""
    id = db.Column(db.Integer, primary_key=True)
    
    # Detalhes do relato
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    problem_type = db.Column(db.String(50), nullable=False)  # queimada, fumaça, etc.
    severity = db.Column(db.Integer, nullable=False)  # 1-5
    
    # Localização
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    location_name = db.Column(db.String(200), nullable=True)
    
    # Metadados
    reported_at = db.Column(db.DateTime, default=datetime.utcnow)
    reporter_name = db.Column(db.String(100), nullable=True)
    reporter_email = db.Column(db.String(100), nullable=True)
    
    # Status
    status = db.Column(db.String(20), default='reported')  # reported, verified, resolved
    verified = db.Column(db.Boolean, default=False)
    verified_at = db.Column(db.DateTime, nullable=True)
    
    # Imagens (armazenará apenas os caminhos para as imagens)
    image_path = db.Column(db.String(255), nullable=True)
    
    def __repr__(self):
        return f"<EnvironmentalReport {self.id}: {self.title} at ({self.latitude}, {self.longitude})>"
    
    def to_dict(self):
        """Converte o modelo para um dicionário JSON-serializável."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'problem_type': self.problem_type,
            'severity': self.severity,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'location_name': self.location_name,
            'reported_at': self.reported_at.isoformat(),
            'status': self.status,
            'verified': self.verified,
            'image_path': self.image_path
        }