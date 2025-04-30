/**
 * EnviroMap - JavaScript para mapa interativo
 */

// Configuração inicial do mapa
let map = null;
let markers = L.layerGroup();
let reports = [];

// Ícones personalizados para diferentes tipos de problemas
const problemIcons = {
    queimada: L.icon({
        iconUrl: '/static/img/fire.png',
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [0, -32]
    }),
    fumaca: L.icon({
        iconUrl: '/static/img/smoke.png',
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [0, -32]
    }),
    desmatamento: L.icon({
        iconUrl: '/static/img/tree.png',
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [0, -32]
    }),
    poluicao: L.icon({
        iconUrl: '/static/img/pollution.png',
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [0, -32]
    }),
    default: L.icon({
        iconUrl: '/static/img/marker.png',
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [0, -32]
    })
};

// Cores para os níveis de severidade
const severityColors = {
    1: '#5cb85c',  // Verde - Baixa
    2: '#5bc0de',  // Azul
    3: '#f0ad4e',  // Amarelo - Média
    4: '#ff9800',  // Laranja
    5: '#d9534f'   // Vermelho - Alta
};

// Inicialização do mapa
function initMap() {
    // Criar mapa Leaflet
    map = L.map('map').setView([-15.7801, -47.9292], 5); // Centro inicial no Brasil
    
    // Adicionar camada do OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>'
    }).addTo(map);
    
    // Adicionar camada de marcadores
    markers.addTo(map);
    
    // Carregar dados iniciais
    loadReports();
    
    // Configurar evento para botão de filtros
    document.getElementById('btn-apply-filters').addEventListener('click', applyFilters);
}

// Carregar relatos da API
async function loadReports() {
    try {
        const response = await fetch('/api/reports');
        if (!response.ok) {
            throw new Error('Erro ao carregar dados');
        }
        
        reports = await response.json();
        updateMarkers();
    } catch (error) {
        console.error('Erro ao carregar relatos:', error);
        showAlert('Erro ao carregar dados do servidor. Tente novamente mais tarde.', 'danger');
    }
}

// Atualizar marcadores no mapa com base nos filtros
function updateMarkers() {
    // Limpar marcadores existentes
    markers.clearLayers();
    
    // Obter valores dos filtros
    const filterType = document.getElementById('filter-type').value;
    const filterSeverity = document.getElementById('filter-severity').value;
    const filterDate = document.getElementById('filter-date').value;
    
    // Filtrar relatos
    let filteredReports = reports;
    
    if (filterType) {
        filteredReports = filteredReports.filter(report => report.problem_type === filterType);
    }
    
    if (filterSeverity) {
        filteredReports = filteredReports.filter(report => report.severity === parseInt(filterSeverity));
    }
    
    if (filterDate) {
        const now = new Date();
        const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
        
        filteredReports = filteredReports.filter(report => {
            const reportDate = new Date(report.reported_at);
            
            switch (filterDate) {
                case 'today':
                    return reportDate >= today;
                case 'week':
                    const weekAgo = new Date(now);
                    weekAgo.setDate(now.getDate() - 7);
                    return reportDate >= weekAgo;
                case 'month':
                    const monthAgo = new Date(now);
                    monthAgo.setMonth(now.getMonth() - 1);
                    return reportDate >= monthAgo;
                default:
                    return true;
            }
        });
    }
    
    // Adicionar marcadores para cada relato filtrado
    filteredReports.forEach(report => {
        addReportMarker(report);
    });
}

// Adicionar marcador para um relato
function addReportMarker(report) {
    // Selecionar ícone com base no tipo de problema
    const icon = problemIcons[report.problem_type] || problemIcons.default;
    
    // Criar marcador
    const marker = L.marker([report.latitude, report.longitude], { icon });
    
    // Adicionar popup com informações básicas
    marker.bindPopup(`
        <strong>${report.title}</strong><br>
        Tipo: ${report.problem_type}<br>
        Severidade: ${report.severity}<br>
        <button class="btn btn-sm btn-primary mt-2 view-details-btn" 
                data-report-id="${report.id}">Ver detalhes</button>
    `);
    
    // Evento de clique para abrir o modal
    marker.on('click', function() {
        marker.openPopup();
    });
    
    // Adicionar à camada de marcadores
    markers.addLayer(marker);
    
    // Adicionar event listener ao botão dentro do popup
    marker.on('popupopen', function() {
        const btn = document.querySelector(`.view-details-btn[data-report-id="${report.id}"]`);
        if (btn) {
            btn.addEventListener('click', function() {
                openReportModal(report);
            });
        }
    });
}

// Abrir modal com detalhes do relato
function openReportModal(report) {
    // Preencher dados no modal
    document.getElementById('report-title').textContent = report.title;
    document.getElementById('report-description').textContent = report.description || 'Sem descrição fornecida.';
    document.getElementById('report-type').textContent = report.problem_type;
    document.getElementById('report-severity').textContent = `${report.severity} / 5`;
    document.getElementById('report-location').textContent = report.location_name || `${report.latitude.toFixed(6)}, ${report.longitude.toFixed(6)}`;
    
    // Formatar data
    const reportDate = new Date(report.reported_at);
    document.getElementById('report-date').textContent = reportDate.toLocaleDateString('pt-BR', {
        day: '2-digit', month: '2-digit', year: 'numeric',
        hour: '2-digit', minute: '2-digit'
    });
    
    // Status do relato
    document.getElementById('report-status').textContent = 
        report.verified ? 'Verificado' : 'Reportado';
    
    // Imagem, se disponível
    const imageContainer = document.getElementById('report-image-container');
    const imageElement = document.getElementById('report-image');
    
    if (report.image_path) {
        imageElement.src = `/${report.image_path}`;
        imageContainer.classList.remove('d-none');
    } else {
        imageContainer.classList.add('d-none');
    }
    
    // Link para detalhes completos
    document.getElementById('report-detail-link').href = `/reports/${report.id}`;
    
    // Abrir modal
    new bootstrap.Modal(document.getElementById('reportModal')).show();
}

// Aplicar filtros
function applyFilters() {
    updateMarkers();
}

// Mostrar alerta na tela
function showAlert(message, type = 'info') {
    const alertContainer = document.createElement('div');
    alertContainer.className = `alert alert-${type} alert-dismissible fade show`;
    alertContainer.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Fechar"></button>
    `;
    
    document.body.appendChild(alertContainer);
    
    // Auto-remover após 5 segundos
    setTimeout(() => {
        alertContainer.remove();
    }, 5000);
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', initMap);