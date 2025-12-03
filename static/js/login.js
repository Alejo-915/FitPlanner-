document.addEventListener('DOMContentLoaded', function() {
    // Efectos de inputs (común)
    initInputEffects();

    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
});

function initInputEffects() {
    document.querySelectorAll('.input-custom').forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.parentElement.classList.add('is-focused');
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.parentElement.classList.remove('is-focused');
        });
    });
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

async function handleLogin(e) {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const remember = document.getElementById('remember').checked;
    
    // Validación básica
    if (!email || !password) {
        alert('Por favor, completa todos los campos');
        return;
    }
    
    if (!isValidEmail(email)) {
        alert('Por favor, ingresa un email válido');
        return;
    }
    
    const loginData = {
        email: email,
        password: password,
        remember: remember
    };

    console.log('Datos de login capturados:', loginData);

    // Mostrar estado de carga
    const button = document.querySelector('.btn-login');
    const originalContent = button.innerHTML;
    button.innerHTML = '<span class="icon"><i class="fas fa-spinner fa-spin"></i></span><span>Iniciando...</span>';
    button.disabled = true;

    try {
        // Llamada real a la API
        const response = await fetch('/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(loginData)
        });

        if (response.ok) {
            window.location.href = '/home/user';
        } else {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Error en login');
        }
        
    } catch (error) {
        console.error('Error durante el login:', error);
        alert('Error al iniciar sesión. Por favor intente nuevamente.');
        button.innerHTML = originalContent;
        button.disabled = false;
    }
}
