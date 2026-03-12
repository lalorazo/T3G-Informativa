// Variables globales
let cart = [];

// Inicializar página
document.addEventListener('DOMContentLoaded', async () => {
    await cargarCaracteristicas();
    await cargarTecnologias();
    await cargarKits();
    verificarSesion();
});

// Verificar si hay sesión activa
async function verificarSesion() {
    const token = localStorage.getItem('t3g_token');
    if (token) {
        try {
            const result = await verifyToken(token);
            if (result.valid) {
                // Token válido, redirigir a página de cliente
                window.location.href = '/cliente.html';
            }
        } catch (error) {
            localStorage.removeItem('t3g_token');
        }
    }
}

// Cargar características
async function cargarCaracteristicas() {
    const features = [
        { icon: 'fa-robot', title: 'IA Predictiva', desc: 'Nuestros algoritmos de inteligencia artificial identifican amenazas antes de que ocurran.' },
        { icon: 'fa-bolt', title: 'Respuesta Rápida', desc: 'Sistema de respuesta automatizada que actúa en milisegundos.' },
        { icon: 'fa-globe', title: 'Cobertura Global', desc: 'Protección distribuida en más de 50 centros de datos.' },
        { icon: 'fa-user-shield', title: 'Autenticación Avanzada', desc: 'Sistemas de autenticación multifactor biométrica.' },
        { icon: 'fa-chart-line', title: 'Análisis en Tiempo Real', desc: 'Dashboards interactivos con métricas clave.' },
        { icon: 'fa-database', title: 'Encriptación Total', desc: 'Protección con encriptación de grado militar AES-256.' }
    ];
    
    const grid = document.getElementById('featuresGrid');
    grid.innerHTML = features.map(f => `
        <div class="feature-card">
            <i class="fas ${f.icon}"></i>
            <h3>${f.title}</h3>
            <p>${f.desc}</p>
        </div>
    `).join('');
}

// Cargar tecnologías
async function cargarTecnologias() {
    const techs = [
        { name: 'Python', desc: 'Backend & IA' },
        { name: 'React', desc: 'Frontend' },
        { name: 'AWS', desc: 'Cloud Services' },
        { name: 'TensorFlow', desc: 'Machine Learning' },
        { name: 'Kubernetes', desc: 'Orquestación' },
        { name: 'PostgreSQL', desc: 'Base de Datos' },
        { name: 'Node.js', desc: 'API Services' },
        { name: 'Docker', desc: 'Contenedores' }
    ];
    
    const grid = document.getElementById('techGrid');
    grid.innerHTML = techs.map(t => `
        <div class="tech-card">
            <h4>${t.name}</h4>
            <p>${t.desc}</p>
        </div>
    `).join('');
}

// Cargar kits desde MongoDB
async function cargarKits() {
    try {
        const kits = await getKits();
        const grid = document.getElementById('kitsGrid');
        
        if (kits.length === 0) {
            grid.innerHTML = '<p style="text-align: center;">No hay kits disponibles</p>';
            return;
        }
        
        grid.innerHTML = kits.map(kit => `
            <div class="kit-card ${kit.destacado ? 'featured' : ''}">
                ${kit.destacado ? '<div class="kit-badge">MÁS VENDIDO</div>' : ''}
                <div class="kit-header">
                    <i class="fas ${kit.tipo === 'residencial' ? 'fa-home' : kit.tipo === 'profesional' ? 'fa-building' : 'fa-industry'}"></i>
                    <h3>${kit.nombre}</h3>
                </div>
                <div class="kit-content">
                    <div class="kit-price">
                        $${kit.precio.toFixed(2)} <small>MXN</small>
                    </div>
                    <ul class="kit-features">
                        <li><i class="fas fa-check"></i> ${kit.sensores.camaras} Cámaras 4K</li>
                        <li><i class="fas fa-check"></i> ${kit.sensores.gas} Sensores de gas</li>
                        <li><i class="fas fa-check"></i> ${kit.sensores.movimiento} Sensores de movimiento</li>
                        <li><i class="fas fa-check"></i> ${kit.sensores.calor} Sensores de calor</li>
                        <li><i class="fas fa-check"></i> Instalación profesional</li>
                        <li><i class="fas fa-check"></i> ${kit.meses_monitoreo_gratis} meses de monitoreo gratis</li>
                    </ul>
                    <button onclick="addToCart('${kit.nombre}', ${kit.precio})" class="btn ${kit.destacado ? 'btn-success' : 'btn-primary'} btn-wide">
                        <i class="fas fa-cart-plus"></i> Agregar
                    </button>
                </div>
            </div>
        `).join('');
        
    } catch (error) {
        console.error('Error cargando kits:', error);
        document.getElementById('kitsGrid').innerHTML = '<p style="text-align: center; color: #ef4444;">Error al cargar los kits</p>';
    }
}

// Login

document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const codigo = document.getElementById('codigo').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const errorDiv = document.getElementById('loginError');
    
    try {
        const response = await fetch('http://localhost:5000/api/auth/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({codigo, email, password})
        });
        
        const data = await response.json();
        console.log('📥 Respuesta del servidor:', data);
        
        if (response.ok && data.success) {
            // Guardar en localStorage
            try {
                localStorage.setItem('t3g_token', data.token);
                localStorage.setItem('t3g_cliente', JSON.stringify(data.cliente));
                console.log('✅ Datos guardados en localStorage');
            } catch (e) {
                console.error('Error guardando en localStorage:', e);
            }
            
            // Redirigir según rol
            if (data.cliente.rol === 'admin') {
                window.location.href = '/admin.html';
            } else {
                window.location.href = '/cliente.html';
            }
        } else {
            errorDiv.textContent = data.error || 'Error en el login';
            errorDiv.style.display = 'block';
        }
    } catch (error) {
        console.error('❌ Error:', error);
        errorDiv.textContent = 'Error de conexión con el servidor';
        errorDiv.style.display = 'block';
    }
});

// Demo form
document.getElementById('demoForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const data = {
        nombre: document.getElementById('demoName').value,
        email: document.getElementById('demoEmail').value,
        telefono: document.getElementById('demoPhone').value,
        empresa: document.getElementById('demoCompany').value,
        kit_interes: document.getElementById('demoKit').value,
        mensaje: document.getElementById('demoMessage').value
    };
    
    try {
        const result = await solicitarDemo(data);
        
        // Abrir cliente de correo
        window.location.href = result.mailto;
        
        // Mostrar mensaje de éxito
        const msgDiv = document.getElementById('demoMessage');
        msgDiv.textContent = '¡Solicitud enviada! Te contactaremos pronto.';
        msgDiv.style.display = 'block';
        msgDiv.style.color = '#10b981';
        
        // Resetear formulario
        e.target.reset();
        
    } catch (error) {
        const msgDiv = document.getElementById('demoMessage');
        msgDiv.textContent = error.message || 'Error al enviar solicitud';
        msgDiv.style.display = 'block';
        msgDiv.style.color = '#ef4444';
    }
});

// Funciones del carrito
function addToCart(productName, price) {
    cart.push({
        name: productName,
        price: price,
        id: Date.now()
    });
    
    updateCart();
    showNotification();
}

function removeFromCart(id) {
    cart = cart.filter(item => item.id !== id);
    updateCart();
}

function updateCart() {
    document.getElementById('cartCount').textContent = cart.length;
    
    const cartItems = document.getElementById('cartItems');
    if (cart.length === 0) {
        cartItems.innerHTML = '<p style="text-align: center; color: var(--text-muted);">Tu carrito está vacío</p>';
    } else {
        cartItems.innerHTML = cart.map(item => `
            <div class="cart-item">
                <div class="cart-item-title">${item.name}</div>
                <div class="cart-item-price">$${item.price.toFixed(2)} MXN</div>
                <div class="cart-item-remove" onclick="removeFromCart(${item.id})">
                    <i class="fas fa-trash"></i> Eliminar
                </div>
            </div>
        `).join('');
    }
    
    const total = cart.reduce((sum, item) => sum + item.price, 0);
    document.getElementById('cartTotal').textContent = `$${total.toFixed(2)} MXN`;
}

function toggleCart() {
    document.getElementById('cartSidebar').classList.toggle('open');
    document.getElementById('overlay').classList.toggle('active');
}

function showNotification() {
    const notification = document.getElementById('notification');
    notification.classList.add('show');
    
    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}

function checkout() {
    if (cart.length === 0) {
        alert('Agrega productos al carrito primero');
        return;
    }
    
    const total = cart.reduce((sum, item) => sum + item.price, 0);
    const itemsList = cart.map(item => `- ${item.name}: $${item.price.toFixed(2)} MXN`).join('%0A');
    
    const message = `Hola, estoy interesado en los siguientes kits:%0A%0A${itemsList}%0A%0ATotal: $${total.toFixed(2)} MXN`;
    
    window.open(`https://wa.me/524641161649?text=${message}`, '_blank');
}

// Modal functions
function openLoginModal() {
    document.getElementById('loginModal').classList.add('active');
}

function closeLoginModal() {
    document.getElementById('loginModal').classList.remove('active');
    document.getElementById('loginError').style.display = 'none';
}

// Smooth scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        
        const targetId = this.getAttribute('href');
        if(targetId === '#') return;
        
        const targetElement = document.querySelector(targetId);
        if(targetElement) {
            window.scrollTo({
                top: targetElement.offsetTop - 80,
                behavior: 'smooth'
            });
        }
    });
});

// Header scroll effect
window.addEventListener('scroll', function() {
    const nav = document.querySelector('nav');
    if (window.scrollY > 50) {
        nav.style.backgroundColor = 'rgba(2, 6, 23, 0.95)';
        nav.style.backdropFilter = 'blur(15px)';
    } else {
        nav.style.backgroundColor = 'rgba(2, 6, 23, 0.85)';
        nav.style.backdropFilter = 'blur(10px)';
    }
});

// Close modal with Escape
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeLoginModal();
        if (document.getElementById('cartSidebar').classList.contains('open')) {
            toggleCart();
        }
    }
});

// Close modal clicking outside
window.addEventListener('click', function(e) {
    if (e.target.classList.contains('modal')) {
        closeLoginModal();
    }
});