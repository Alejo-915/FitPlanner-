// FitPlanner - JavaScript para páginas de autenticación (Login y Register)

// Función de validación de email
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Efectos de focus en inputs
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

// Funcionalidad del formulario de login
function initLoginForm() {
    const loginForm = document.getElementById('loginForm');
    if (!loginForm) return;

    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        
        // Validación básica
        if (!email || !password) {
            alert('Por favor, completa todos los campos');
            return;
        }
        
        if (!isValidEmail(email)) {
            alert('Por favor, ingresa un email válido');
            return;
        }
        
        // Simulación de login exitoso
        console.log('Login attempt:', { email, password });
        
        // Mostrar mensaje de éxito
        const button = document.querySelector('.btn-login');
        const originalText = button.innerHTML;
        button.innerHTML = '<span class="icon"><i class="fas fa-spinner fa-spin"></i></span><span>Iniciando...</span>';
        button.disabled = true;
        
        // Simular delay de autenticación
        setTimeout(() => {
            // Redireccionar al home del usuario
            window.location.href = '../user/home.html';
        }, 1500);
    });
}

// Funcionalidad del formulario de registro
function initRegisterForm() {
    const registerForm = document.getElementById('registerForm');
    if (!registerForm) return;

    registerForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const firstName = document.getElementById('firstName').value;
        const lastName = document.getElementById('lastName').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        const age = document.getElementById('age').value;
        const goal = document.getElementById('goal').value;
        const terms = document.getElementById('terms').checked;
        
        // Validaciones
        if (!firstName || !lastName || !email || !password || !confirmPassword || !age || !goal) {
            alert('Por favor, completa todos los campos');
            return;
        }
        
        if (!isValidEmail(email)) {
            alert('Por favor, ingresa un email válido');
            return;
        }
        
        if (password.length < 6) {
            alert('La contraseña debe tener al menos 6 caracteres');
            return;
        }
        
        if (password !== confirmPassword) {
            alert('Las contraseñas no coinciden');
            return;
        }
        
        if (!terms) {
            alert('Debes aceptar los términos y condiciones');
            return;
        }
        
        // Simulación de registro exitoso
        console.log('Register attempt:', { firstName, lastName, email, age, goal });
        
        // Mostrar mensaje de éxito
        const button = document.querySelector('.btn-register');
        button.innerHTML = '<span class="icon"><i class="fas fa-spinner fa-spin"></i></span><span>Creando cuenta...</span>';
        button.disabled = true;
        
        // Simular delay de registro
        setTimeout(() => {
            // Redireccionar al home del usuario
            window.location.href = '../user/home.html';
        }, 2000);
    });
}

// Verificador de fortaleza de contraseña
function initPasswordStrength() {
    const passwordInput = document.getElementById('password');
    if (!passwordInput) return;

    passwordInput.addEventListener('input', function() {
        const password = this.value;
        const strengthDiv = document.getElementById('passwordStrength');
        
        if (!strengthDiv) return;
        
        if (password.length === 0) {
            strengthDiv.textContent = '';
            return;
        }
        
        let strength = 0;
        if (password.length >= 6) strength++;
        if (password.match(/[a-z]/)) strength++;
        if (password.match(/[A-Z]/)) strength++;
        if (password.match(/[0-9]/)) strength++;
        if (password.match(/[^a-zA-Z0-9]/)) strength++;
        
        if (strength < 3) {
            strengthDiv.textContent = 'Contraseña débil';
            strengthDiv.className = 'password-strength strength-weak';
        } else if (strength < 4) {
            strengthDiv.textContent = 'Contraseña media';
            strengthDiv.className = 'password-strength strength-medium';
        } else {
            strengthDiv.textContent = 'Contraseña fuerte';
            strengthDiv.className = 'password-strength strength-strong';
        }
    });
}

// Verificador de coincidencia de contraseñas
function initPasswordMatch() {
    const confirmPasswordInput = document.getElementById('confirmPassword');
    if (!confirmPasswordInput) return;

    confirmPasswordInput.addEventListener('input', function() {
        const password = document.getElementById('password').value;
        const confirmPassword = this.value;
        
        if (confirmPassword && password !== confirmPassword) {
            this.style.borderColor = '#ff3860';
        } else {
            this.style.borderColor = '#E2E2E2';
        }
    });
}

// Inicialización cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar funcionalidades comunes
    initInputEffects();
    
    // Inicializar funcionalidades específicas según la página
    initLoginForm();
    initRegisterForm();
    initPasswordStrength();
    initPasswordMatch();
});
