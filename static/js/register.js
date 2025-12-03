document.addEventListener('DOMContentLoaded', function() {
    // Efectos de inputs y validaciones en tiempo real
    initInputEffects();
    initPasswordStrength();
    initPasswordMatch();

    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
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

async function handleRegister(e) {
    e.preventDefault();
    
    const firstName = document.getElementById('firstName').value;
    const lastName = document.getElementById('lastName').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const age = document.getElementById('age').value;
    const goal = document.getElementById('goal').value;
    const terms = document.getElementById('terms').checked;
    const fullname = `${firstName} ${lastName}`;
    
    // Validaciones
    if (!fullname || !email || !password || !confirmPassword || !age || !goal) {
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
    
    const registerData = {
        fullname,
        email,
        password,
        age: parseInt(age),
        goal,
        termsAccepted: terms
    };

    console.log('Datos de registro capturados:', registerData);

    // Mostrar estado de carga
    const button = document.querySelector('.btn-register');
    const originalContent = button.innerHTML;
    button.innerHTML = '<span class="icon"><i class="fas fa-spinner fa-spin"></i></span><span>Creando cuenta...</span>';
    button.disabled = true;

    try {
        // Llamada real a la API
        const response = await fetch('/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(registerData)
        });

        // Simulación de delay
        // await new Promise(resolve => setTimeout(resolve, 2000));
        
        if (response.ok) {
            window.location.href = '/home/user';
        } else {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Error en registro');
        }
        
    } catch (error) {
        console.error('Error durante el registro:', error);
        alert('Error al crear la cuenta. Por favor intente nuevamente.');
        button.innerHTML = originalContent;
        button.disabled = false;
    }
}
