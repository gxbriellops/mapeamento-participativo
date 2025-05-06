import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from models import db, EnvironmentalReport

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Extensões de arquivo permitidas para upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api_bp.route('/reports', methods=['GET'])
def get_reports():
    """Retorna todos os relatos ambientais."""
    reports = EnvironmentalReport.query.all()
    return jsonify([report.to_dict() for report in reports])

@api_bp.route('/reports/<int:report_id>', methods=['GET'])
def get_report(report_id):
    """Retorna um relato específico pelo ID."""
    report = EnvironmentalReport.query.get_or_404(report_id)
    return jsonify(report.to_dict())

@api_bp.route('/reports', methods=['POST'])
def create_report():
    """Cria um novo relato ambiental."""
    data = request.form.to_dict()
    
    # Validação básica
    required_fields = ['title', 'problem_type', 'severity', 'latitude', 'longitude']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Campo obrigatório ausente: {field}'}), 400
    
    # Cria o relato
    new_report = EnvironmentalReport(
        title=data['title'],
        description=data.get('description', ''),
        problem_type=data['problem_type'],
        severity=int(data['severity']),
        latitude=float(data['latitude']),
        longitude=float(data['longitude']),
        location_name=data.get('location_name', ''),
        reporter_name=data.get('reporter_name', ''),
        reporter_email=data.get('reporter_email', '')
    )
    
    # Processa o upload de imagem, se houver
    if 'image' in request.files:
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Usa timestamp para garantir unicidade do nome do arquivo
            import time
            unique_filename = f"{int(time.time())}_{filename}"
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            # Armazena o caminho relativo para uso nas URLs
            new_report.image_path = f"uploads/{unique_filename}"
    
    # Salva no banco de dados
    db.session.add(new_report)
    db.session.commit()
    
    return jsonify({
        'message': 'Relato criado com sucesso!',
        'report': new_report.to_dict()
    }), 201

@api_bp.route('/reports/<int:report_id>', methods=['PUT', 'PATCH'])
def update_report(report_id):
    """Atualiza um relato existente."""
    report = EnvironmentalReport.query.get_or_404(report_id)
    data = request.form.to_dict() if request.form else request.get_json()
    
    # Atualiza os campos
    if 'title' in data:
        report.title = data['title']
    if 'description' in data:
        report.description = data['description']
    if 'problem_type' in data:
        report.problem_type = data['problem_type']
    if 'severity' in data:
        report.severity = int(data['severity'])
    if 'status' in data:
        report.status = data['status']
    if 'verified' in data:
        report.verified = bool(data['verified'])
        if report.verified:
            from datetime import datetime
            report.verified_at = datetime.utcnow()
    
    # Salva as alterações
    db.session.commit()
    
    return jsonify({
        'message': 'Relato atualizado com sucesso',
        'report': report.to_dict()
    })

@api_bp.route('/reports/<int:report_id>', methods=['DELETE'])
def delete_report(report_id):
    """Remove um relato."""
    report = EnvironmentalReport.query.get_or_404(report_id)
    
    # Remove o arquivo de imagem se existir
    if report.image_path:
        try:
            os.remove(os.path.join(current_app.static_folder, report.image_path))
        except (FileNotFoundError, OSError):
            # Ignora erros ao remover o arquivo
            pass
    
    db.session.delete(report)
    db.session.commit()
    
    return jsonify({'message': 'Relato removido com sucesso'})

@api_bp.route('/reports/types', methods=['GET'])
def get_problem_types():
    """Retorna tipos de problemas e suas contagens."""
    types = db.session.query(
        EnvironmentalReport.problem_type, 
        db.func.count(EnvironmentalReport.id)
    ).group_by(EnvironmentalReport.problem_type).all()
    
    return jsonify([{'type': t[0], 'count': t[1]} for t in types])