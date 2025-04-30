from flask import Blueprint, render_template
from models import db, EnvironmentalReport

views_bp = Blueprint('views', __name__)
@views_bp.route('/')
def index():
    """Página inicial com o mapa."""
    return render_template('index.html')

@views_bp.route('/report')
def report_form():
    """Página com formulário para criar um novo relato."""
    return render_template('report.html')

@views_bp.route('/dashboard')
def dashboard():
    """Dashboard com estatísticas e visualizações."""
    # Busca dados agregados para o dashboard
    total_reports = EnvironmentalReport.query.count()
    
    # Contagem por tipo de problema
    problem_types = EnvironmentalReport.query.with_entities(
        EnvironmentalReport.problem_type,
        db.func.count(EnvironmentalReport.id)
    ).group_by(EnvironmentalReport.problem_type).all()
    
    # Contagem por severidade
    severity_counts = EnvironmentalReport.query.with_entities(
        EnvironmentalReport.severity,
        db.func.count(EnvironmentalReport.id)
    ).group_by(EnvironmentalReport.severity).all()
    
    # Passa as estatísticas para o template
    return render_template(
        'dashboard.html',
        total_reports=total_reports,
        problem_types=problem_types,
        severity_counts=severity_counts
    )

@views_bp.route('/reports/<int:report_id>')
def view_report(report_id):
    """Visualização detalhada de um relato específico."""
    report = EnvironmentalReport.query.get_or_404(report_id)
    return render_template('report_detail.html', report=report)