document.addEventListener('DOMContentLoaded', function () {
    initInputEffects();
    initPasswordStrength();
    initPasswordMatch();
    initNingunaCheckbox();

    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }
});

function initInputEffects() {
    document.querySelectorAll('.input-custom').forEach(input => {
        input.addEventListener('focus', function () {
            this.parentElement.parentElement.classList.add('is-focused');
        });
        input.addEventListener('blur', function () {
            this.parentElement.parentElement.classList.remove('is-focused');
        });
    });
}

function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function initPasswordStrength() {
    const passwordInput = document.getElementById('password');
    if (!passwordInput) return;
    passwordInput.addEventListener('input', function () {
        const p = this.value;
        const div = document.getElementById('passwordStrength');
        if (!div) return;
        if (!p) { div.textContent = ''; return; }
        let s = 0;
        if (p.length >= 6) s++;
        if (p.match(/[a-z]/)) s++;
        if (p.match(/[A-Z]/)) s++;
        if (p.match(/[0-9]/)) s++;
        if (p.match(/[^a-zA-Z0-9]/)) s++;
        if (s < 3) { div.textContent = 'Contraseña débil'; div.className = 'password-strength strength-weak'; }
        else if (s < 4) { div.textContent = 'Contraseña media'; div.className = 'password-strength strength-medium'; }
        else { div.textContent = 'Contraseña fuerte'; div.className = 'password-strength strength-strong'; }
    });
}

function initPasswordMatch() {
    const confirm = document.getElementById('confirmPassword');
    if (!confirm) return;
    confirm.addEventListener('input', function () {
        const pw = document.getElementById('password').value;
        this.style.borderColor = (this.value && pw !== this.value) ? '#ff3860' : '#E2E2E2';
    });
}

// Si marca "Ninguna" desmarcar las demás y viceversa
function initNingunaCheckbox() {
    const chkNinguna = document.getElementById('chk-ninguna');
    const otrasChk = document.querySelectorAll('input[name="limitacion"]:not(#chk-ninguna)');

    if (!chkNinguna) return;

    chkNinguna.addEventListener('change', () => {
        if (chkNinguna.checked) {
            otrasChk.forEach(c => { c.checked = false; c.disabled = true; });
        } else {
            otrasChk.forEach(c => { c.disabled = false; });
        }
    });

    otrasChk.forEach(c => {
        c.addEventListener('change', () => {
            if (c.checked) {
                chkNinguna.checked = false;
                chkNinguna.disabled = false;
            }
        });
    });
}

async function handleRegister(e) {
    e.preventDefault();

    const firstName = document.getElementById('firstName').value.trim();
    const lastName = document.getElementById('lastName').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const age = document.getElementById('age').value;
    const goal = document.getElementById('goal').value;
    const peso = document.getElementById('peso').value;
    const altura = document.getElementById('altura').value;
    const meses = parseInt(document.getElementById('meses_sin_ejercicio').value);
    const dias = parseInt(document.getElementById('dias_semana').value);
    const terms = document.getElementById('terms').checked;

    // Recoger limitaciones seleccionadas
    const limitaciones = Array.from(
        document.querySelectorAll('input[name="limitacion"]:checked')
    )
        .map(c => c.value)
        .filter(v => v !== 'ninguna');

    if (!firstName || !lastName || !email || !password || !confirmPassword || !age || !goal) {
        alert('Por favor, completa todos los campos obligatorios');
        return;
    }
    if (!isValidEmail(email)) { alert('Email inválido'); return; }
    if (password.length < 6) { alert('La contraseña debe tener al menos 6 caracteres'); return; }
    if (password !== confirmPassword) { alert('Las contraseñas no coinciden'); return; }
    if (!terms) { alert('Debes aceptar los términos y condiciones'); return; }

    const payload = {
        fullname: `${firstName} ${lastName}`,
        email,
        password,
        age: parseInt(age),
        goal,
        peso: peso ? parseFloat(peso) : null,
        altura: altura ? parseFloat(altura) : null,
        limitaciones,
        meses_sin_ejercicio: meses,
        dias_semana: dias,
    };

    const btn = document.querySelector('.btn-register');
    const orig = btn.innerHTML;
    btn.innerHTML = '<span class="icon"><i class="fas fa-spinner fa-spin"></i></span><span>Creando cuenta...</span>';
    btn.disabled = true;

    try {
        const res = await fetch('/auth/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });
        if (res.ok) {
            window.location.href = '/home/user';
        } else {
            const err = await res.json();
            throw new Error(err.detail || 'Error en registro');
        }
    } catch (error) {
        alert('Error: ' + error.message);
        btn.innerHTML = orig;
        btn.disabled = false;
    }
}