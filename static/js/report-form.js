/**
 * EnviroMap - JavaScript para formulário de relato
 */

// Variáveis globais
let reportMap = null;
let reportMarker = null;

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar mapa para seleção de localização
    initLocationMap();
    
    // Configurar evento de envio do formulário
    document.getElementById('report-form').addEventListener('submit', handleFormSubmit);
});

// Inicializar mapa para seleção de localização
function initLocationMap() {
    // Criar mapa Leaflet
    reportMap = L.map('location-map').setView([-15.7801, -47.9292], 5); // Centro inicial no Brasil
    
    // Adicionar camada do OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>'
    }).addTo(reportMap);
    
    // Tentar obter localização do usuário
    if ('geolocation' in navigator) {
        navigator.geolocation.getCurrentPosition(
            // Sucesso
            function(position) {
                const userLat = position.coords.latitude;
                const userLng = position.coords.longitude;
                
                // Centralizar mapa na localização do usuário
                reportMap.setView([userLat, userLng], 13);
                
                // Colocar marcador na localização do usuário
                setMarkerPosition(userLat, userLng);
            },
            // Erro ou permissão negada
            function(error) {
                console.log('Erro ao obter localização:', error);
                // Continue com a visualização padrão
            }
        );
    }
    
    // Configurar evento de clique no mapa
    reportMap.on('click', function(e) {
        setMarkerPosition(e.latlng.lat, e.latlng.lng);
    });
}

// Definir posição do marcador e atualizar campos de latitude/longitude
function setMarkerPosition(lat, lng) {
    // Atualizar campos de formulário
    document.getElementById('latitude').value = lat.toFixed(6);
    document.getElementById('longitude').value = lng.toFixed(6);
    
    // Remover marcador existente
    if (reportMarker) {
        reportMap.removeLayer(reportMarker);
    }
    
    // Criar novo marcador
    reportMarker = L.marker([lat, lng], {
        draggable: true // Permitir arrastar para ajuste fino
    }).addTo(reportMap);
    
    // Configurar evento ao arrastar o marcador
    reportMarker.on('dragend', function(e) {
        const position = reportMarker.getLatLng();
        document.getElementById('latitude').value = position.lat.toFixed(6);
        document.getElementById('longitude').value = position.lng.toFixed(6);
    });
}

// Tratamento do envio do formulário
async function handleFormSubmit(e) {
    e.preventDefault();
    
    // Validar se uma localização foi selecionada
    const latitude = document.getElementById('latitude').value;
    const longitude = document.getElementById('longitude').value;
    
    if (!latitude || !longitude) {
        showAlert('Por favor, selecione uma localização no mapa.', 'warning');
        return;
    }
    
    // Coletar dados do formulário
    const formData = new FormData(e.target);
    
    try {
        // Enviar dados para a API
        const response = await fetch('/api/reports', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Erro ao enviar relato');
        }
        
        const result = await response.json();
        
        // Mostrar mensagem de sucesso
        showAlert('Relato enviado com sucesso!', 'success');
        
        // Limpar formulário
        document.getElementById('report-form').reset();
        
        // Remover marcador do mapa
        if (reportMarker) {
            reportMap.removeLayer(reportMarker);
            reportMarker = null;
        }
        
        // Redirecionar para a página do mapa após 2 segundos
        setTimeout(() => {
            window.location.href = '/';
        }, 2000);
        
    } catch (error) {
        console.error('Erro ao enviar relato:', error);
        showAlert('Erro ao enviar relato: ' + error.message, 'danger');
    }
}

// Mostrar alerta no formulário
function showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('alert-container');
    alertContainer.innerHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Fechar"></button>
        </div>
    `;
    alertContainer.style.display = 'block';
    
    // Rolar até o alerta
    alertContainer.scrollIntoView({ behavior: 'smooth' });
}