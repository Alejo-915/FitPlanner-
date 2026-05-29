document.addEventListener('DOMContentLoaded', function() {
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
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

async function handleLogin(e) {
    e.preventDefault();

    const email    = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const remember = document.getElementById('remember').checked;

    if (!email || !password) {
        showError('Por favor, completa todos los campos');
        return;
    }
    if (!isValidEmail(email)) {
        showError('Por favor, ingresa un email válido');
        return;
    }

    const button = document.querySelector('.btn-login');
    const originalContent = button.innerHTML;
    button.innerHTML = '<span class="icon"><i class="fas fa-spinner fa-spin"></i></span><span>Iniciando...</span>';
    button.disabled = true;

    try {
        const response = await fetch('/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password, remember })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Credenciales inválidas');
        }

        // ── Guardar sesión en localStorage ──────────────────────
        localStorage.setItem('user_id', data.user_id);
        localStorage.setItem('nombre',  data.nombre);
        localStorage.setItem('objetivo', data.objetivo || '');
        localStorage.setItem('nivel_condicion', data.nivel_condicion || '');

        window.location.href = '/home/user';

    } catch (error) {
        showError(error.message || 'Error al iniciar sesión. Intente nuevamente.');
        button.innerHTML = originalContent;
        button.disabled = false;
    }
}

function showError(msg) {
    let box = document.getElementById('login-error');
    if (!box) {
        box = document.createElement('div');
        box.id = 'login-error';
        box.style.cssText = `
            background:#fff0f0; border:1px solid #E30005; border-radius:8px;
            color:#c20004; padding:10px 14px; margin-bottom:16px; font-size:14px;
            display:flex; align-items:center; gap:8px;
        `;
        const form = document.getElementById('loginForm');
        form.insertBefore(box, form.firstChild);
    }
    box.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${msg}`;
    box.style.display = 'flex';
}