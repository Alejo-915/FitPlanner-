document.addEventListener('DOMContentLoaded', async function() {
    const userId = localStorage.getItem('user_id');
    
    if (!userId) {
        // Si no hay ID de usuario, redirigir al login
        window.location.href = '/login';
        return;
    }

    try {
        const response = await fetch(`/usuarios/${userId}`);
        if (!response.ok) {
            throw new Error('Error al cargar datos del usuario');
        }

        const user = await response.json();
        updateUserProfile(user);

    } catch (error) {
        console.error('Error:', error);
        alert('Error al cargar el perfil. Por favor inicie sesión nuevamente.');
        window.location.href = '/login';
    }
});

function updateUserProfile(user) {
    // Actualizar Navbar
    const navName = document.getElementById('nav-user-name');
    if (navName) navName.textContent = `Hola, ${user.nombre.split(' ')[0]}`;
    
    // Actualizar Avatar
    const avatar = document.getElementById('user-avatar');
    if (avatar) {
        avatar.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(user.nombre)}&background=E30005&color=fff`;
    }

    // Actualizar Tarjeta de Perfil
    const profileName = document.getElementById('profile-name');
    if (profileName) profileName.textContent = user.nombre;

    const profileAge = document.getElementById('profile-age');
    if (profileAge) profileAge.textContent = `${user.edad} años`;

    const profileWeight = document.getElementById('profile-weight');
    if (profileWeight) profileWeight.textContent = user.peso ? `${user.peso} kg` : '-- kg';

    const profileHeight = document.getElementById('profile-height');
    if (profileHeight) profileHeight.textContent = user.altura ? `${user.altura} m` : '-- m'; // Asumiendo que altura se guardó en metros o cm? 
    // En register.html placeholder era 170 (cm), pero en home.html placeholder era 1.75 m.
    // Vamos a formatear. Si es > 3, asumimos cm y convertimos a m.
    if (profileHeight && user.altura) {
        let heightVal = user.altura;
        if (heightVal > 3) {
            heightVal = heightVal / 100;
        }
        profileHeight.textContent = `${heightVal.toFixed(2)} m`;
    }

    const profileGoal = document.getElementById('profile-goal');
    if (profileGoal) {
        const goals = {
            'lose_weight': 'Perder peso',
            'gain_muscle': 'Ganar músculo',
            'maintain': 'Mantener forma',
            'improve_endurance': 'Mejorar resistencia'
        };
        profileGoal.textContent = goals[user.objetivo] || user.objetivo;
    }
}
