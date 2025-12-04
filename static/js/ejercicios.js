let tablaEjercicios;
let ejercicioGlobal = null;

// Modal elements - Detalles
const modalDetalles = document.getElementById('modal-detalles-ejercicio');
const modalTitle = document.getElementById('modal-ejercicio-title');
const closeModalBtn = document.getElementById('close-modal-btn-ejercicio');
const detallesContainer = document.getElementById('detalles-container-ejercicio');

// Modal elements - Crear
const modalCrear = document.getElementById('modal-crear-ejercicio');
const btnCrearEjercicio = document.getElementById('btn-crear-ejercicio');
const closeModalCrearBtn = document.getElementById('close-modal-crear-btn');
const formCrear = document.getElementById('modal-crear-content');

// Close modals
const closeModal = () => {
    if (modalDetalles) modalDetalles.style.display = 'none';
};

const closeModalCrear = () => {
    if (modalCrear) modalCrear.style.display = 'none';
};

$(document).ready(function() {
    // Initialize DataTables
    tablaEjercicios = $('#tabla-ejercicios').DataTable({
        ajax: {
            url: "/ejercicios/",
            dataSrc: "",
            error: function(xhr) { console.error('AJAX Error:', xhr); }
        },
        columns: [
            { data: "id" },
            { data: "nombre" },
            { data: "grupo_muscular" },
            { data: "equipo" },
            { data: "descripcion" },
            {
                data: "video_url",
                render: function(data) {
                    if (data) {
                        return `<a href="${data}" target="_blank" class="button is-small is-link">
                            <i class="fab fa-youtube"></i> Ver Video
                        </a>`;
                    }
                    return '<span style="color: #999;">Sin video</span>';
                }
            },
            {
                data: null,
                orderable: false,
                render: function(data, type, row) {
                    return `<div class="btn-group">
                        <button class="btn btn-sm btn-danger" onClick="viewDeleteEjercicio(${row.id})">🗑️</button>
                        <button class="btn btn-sm btn-info" onClick="viewDetailsEjercicio(${row.id})">✏️</button>
                    </div>`;
                }
            }
        ],
        dom: "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>" +
                "<'row'<'col-sm-12'tr>>" +
                "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>" +
                "<'row'<'col-sm-12'B>>",
        buttons: [
            { extend: 'excel', text: 'Excel', className: 'btn btn-success' },
            { extend: 'csv', text: 'CSV', className: 'btn btn-info' },
            { extend: 'pdf', text: 'PDF', className: 'btn btn-danger' },
            { extend: 'print', text: 'Imprimir', className: 'btn btn-warning' }
        ],
        language: {
            info: "_START_ a _END_ de _TOTAL_ ejercicios",
            paginate: { previous: "‹", next: "›" },
            buttons: { excel: "Excel", csv: "CSV", pdf: "PDF", print: "Imprimir" },
            search: "Buscar:",
            lengthMenu: "Mostrar _MENU_ ejercicios por página",
        },
    });

    // Modal Detalles Event Listeners
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', e => {
            e.preventDefault();
            closeModal();
        });
    }

    window.addEventListener('click', e => {
        if (e.target === modalDetalles) closeModal();
        if (e.target === modalCrear) closeModalCrear();
    });

    // Modal Crear Event Listeners
    if (btnCrearEjercicio) {
        btnCrearEjercicio.addEventListener('click', e => {
            e.preventDefault();
            abrirModalCrear();
        });
    }

    if (closeModalCrearBtn) {
        closeModalCrearBtn.addEventListener('click', e => {
            e.preventDefault();
            closeModalCrear();
        });
    }

    // Form Crear Submit
    if (formCrear) {
        formCrear.addEventListener('submit', async (e) => {
            e.preventDefault();
            await crearNuevoEjercicio();
        });
    }

    // Handle Edit/Save inside Modal Detalles
    if (detallesContainer) {
        detallesContainer.addEventListener('click', e => {
            e.preventDefault();

            // Toggle Edit Mode
            if (e.target.classList.contains('btn-edit')) {
                const inp = e.target.closest('.input-container').querySelector('.input_field');
                inp.disabled = !inp.disabled;
                e.target.textContent = inp.disabled ? '✏️' : '✔️';
                return;
            }

            // Save Changes
            if (e.target.id === 'submit-btn') {
                const formInputs = document.querySelectorAll('#detalles-container-ejercicio .input_field');
                const data = {};
                formInputs.forEach(input => {
                    data[input.name] = input.value;
                });

                fetch(`/ejercicios/${ejercicioGlobal.id}`, {
                    method: 'PATCH',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                })
                .then(res => {
                    if (!res.ok) throw new Error(`HTTP ${res.status}`);
                    return res.json();
                })
                .then(json => {
                    alert('Ejercicio actualizado correctamente');
                    closeModal();
                    tablaEjercicios.ajax.reload(null, false);
                })
                .catch(err => {
                    console.error('Error al actualizar ejercicio:', err);
                    alert('Error al actualizar ejercicio');
                });
            }
        });
    }
});

// Función para abrir modal de crear
function abrirModalCrear() {
    // Limpiar campos
    document.getElementById('nuevo-nombre').value = '';
    document.getElementById('nuevo-grupo-muscular').value = '';
    document.getElementById('nuevo-equipo').value = '';
    document.getElementById('nuevo-descripcion').value = '';
    document.getElementById('nuevo-video-url').value = '';

    modalCrear.style.display = 'flex';
}

// Función para crear nuevo ejercicio
async function crearNuevoEjercicio() {
    const nombre = document.getElementById('nuevo-nombre').value;
    const grupo_muscular = document.getElementById('nuevo-grupo-muscular').value;
    const equipo = document.getElementById('nuevo-equipo').value;
    const descripcion = document.getElementById('nuevo-descripcion').value;
    const video_url = document.getElementById('nuevo-video-url').value;

    if (!nombre || !grupo_muscular || !equipo || !descripcion) {
        alert('Por favor completa todos los campos obligatorios');
        return;
    }

    const nuevoEjercicio = {
        nombre,
        grupo_muscular,
        equipo,
        descripcion,
        video_url: video_url || null
    };

    try {
        const response = await fetch('/ejercicios/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(nuevoEjercicio)
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();
        alert('¡Ejercicio creado exitosamente!');
        closeModalCrear();
        tablaEjercicios.ajax.reload(null, false);

    } catch (error) {
        console.error('Error al crear ejercicio:', error);
        alert('Error al crear el ejercicio. Por favor intenta nuevamente.');
    }
}

// Helper to fetch exercise details
const fetchEjercicio = async (id) => {
    const res = await fetch(`/ejercicios/${id}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
};

// Global function to open modal details (called from HTML onClick)
window.viewDetailsEjercicio = async (id) => {
    try {
        const ejercicio = await fetchEjercicio(id);
        ejercicioGlobal = ejercicio;
        modalTitle.textContent = `Ejercicio #${ejercicio.id}`;
        modalDetalles.style.display = 'flex';

        let html = `
            <label>Nombre:
                <div class="input-container">
                    <input disabled class="input_field" name="nombre" value="${ejercicio.nombre || ''}">
                    <button type="button" class="btn-edit">✏️</button>
                </div>
            </label>

            <label>Grupo Muscular:
                <div class="input-container">
                    <input disabled class="input_field" name="grupo_muscular" value="${ejercicio.grupo_muscular || ''}">
                    <button type="button" class="btn-edit">✏️</button>
                </div>
            </label>

            <label>Equipo:
                <div class="input-container">
                    <input disabled class="input_field" name="equipo" value="${ejercicio.equipo || ''}">
                    <button type="button" class="btn-edit">✏️</button>
                </div>
            </label>

            <label>Descripción:
                <div class="input-container">
                    <textarea disabled class="input_field" name="descripcion" rows="4">${ejercicio.descripcion || ''}</textarea>
                    <button type="button" class="btn-edit">✏️</button>
                </div>
            </label>

            <label>URL del Video (YouTube):
                <div class="input-container">
                    <input disabled class="input_field" name="video_url" value="${ejercicio.video_url || ''}">
                    <button type="button" class="btn-edit">✏️</button>
                </div>
            </label>

            ${ejercicio.video_url ? `
                <div style="margin-top: 15px;">
                    <a href="${ejercicio.video_url}" target="_blank" class="button is-link">
                        <i class="fab fa-youtube"></i> Ver Video en YouTube
                    </a>
                </div>
            ` : ''}

            <button type="button" id="submit-btn">Guardar cambios</button>
        `;
        detallesContainer.innerHTML = html;
    } catch (err) {
        console.error(err);
        alert("Error al cargar ejercicio");
    }
};

// Global function to delete exercise
window.viewDeleteEjercicio = (id) => {
    if (!id) return;

    const confirmado = confirm("¿Seguro que deseas eliminar este ejercicio? Esta acción es irreversible.");
    if (!confirmado) return;

    fetch(`/ejercicios/${id}`, {
        method: 'DELETE'
    })
    .then(res => res.json())
    .then(data => {
        alert("Ejercicio eliminado correctamente.");
        tablaEjercicios.ajax.reload(null, false);
    })
    .catch(err => alert("Error al eliminar ejercicio: " + err.message));
};
