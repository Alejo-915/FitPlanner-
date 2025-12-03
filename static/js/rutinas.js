let tablaRutinas;
let rutinaGlobal = null;

// Modal elements
const modalDetalles = document.getElementById('modal-detalles-rutina');
const modalTitle = document.getElementById('modal-rutina-title');
const closeModalBtn = document.getElementById('close-modal-btn-rutina');
const detallesContainer = document.getElementById('detalles-container-rutina');

// Close modal helper
const closeModal = () => {
    if (modalDetalles) modalDetalles.style.display = 'none';
};

$(document).ready(function() {
    // Initialize DataTables
    tablaRutinas = $('#tabla-rutinas').DataTable({
        ajax: {
            url: "/rutinas/", // Endpoint from routes/rutina.py
            dataSrc: "rutinas", // API returns { "rutinas": [...] }
            error: function(xhr) { console.error('AJAX Error:', xhr); }
        },
        columns: [
            { data: "id" },
            { data: "nombre_rutina" }, // Note: API returns nombre_rutina
            { data: "nivel" },
            { data: "frecuencia" },
            { data: "usuario_id" },
            {
                data: null,
                orderable: false,
                render: function(data, type, row) {
                    return `<div class="btn-group">
                        <button class="btn btn-sm btn-danger" onClick="viewDeleteRutina(${row.id})">🗑️</button>
                        <button class="btn btn-sm btn-info" onClick="viewDetailsRutina(${row.id})">✏️</button>
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
            info: "_START_ a _END_ de _TOTAL_ rutinas",
            paginate: { previous: "‹", next: "›" },
            buttons: { excel: "Excel", csv: "CSV", pdf: "PDF", print: "Imprimir" },
            search: "Buscar:",
            lengthMenu: "Mostrar _MENU_ rutinas por página",
        },
    });

    // Modal Event Listeners
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', e => { 
            e.preventDefault(); 
            closeModal(); 
        });
    }

    window.addEventListener('click', e => { 
        if (e.target === modalDetalles) closeModal(); 
    });

    // Handle Edit/Save inside Modal
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
                const formInputs = document.querySelectorAll('.input_field');
                const data = {};
                formInputs.forEach(input => { 
                    // We need to map inputs back to model fields if names differ, 
                    // but here we'll ensure input names match model fields (e.g., nombre)
                    if (input.name === 'frecuencia' || input.name === 'usuario_id') {
                         data[input.name] = parseInt(input.value);
                    } else {
                         data[input.name] = input.value;
                    }
                });
    
                fetch(`/rutinas/${rutinaGlobal.id}`, {
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
                    alert('Rutina actualizada correctamente');
                    closeModal();
                    tablaRutinas.ajax.reload(null, false);
                })
                .catch(err => {
                    console.error('Error al actualizar rutina:', err);
                    alert('Error al actualizar rutina');
                });
            }
        });
    }
});

// Helper to fetch routine details
const fetchRutina = async (id) => {
    const res = await fetch(`/rutinas/${id}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
};

// Global function to open modal details
window.viewDetailsRutina = async (id) => {
    try {
        const rutina = await fetchRutina(id);
        rutinaGlobal = rutina;
        modalTitle.textContent = `Rutina #${rutina.id}`;
        modalDetalles.style.display = 'flex';

        // Construct exercises list
        let ejerciciosHtml = '';
        if (rutina.ejercicios && rutina.ejercicios.length > 0) {
            ejerciciosHtml = '<ul>';
            rutina.ejercicios.forEach(ej => {
                ejerciciosHtml += `<li>${ej.nombre} (${ej.series}x${ej.repeticiones})</li>`;
            });
            ejerciciosHtml += '</ul>';
        } else {
            ejerciciosHtml = '<p>No hay ejercicios asignados.</p>';
        }

        let html = `
            <label>Nombre:
                <div class="input-container">
                    <!-- Model field is 'nombre', API returns 'nombre_rutina' -->
                    <input disabled class="input_field" name="nombre" value="${rutina.nombre_rutina || ''}">
                    <button type="button" class="btn-edit">✏️</button>
                </div>
            </label>

            <label>Nivel:
                <div class="input-container">
                    <input disabled class="input_field" name="nivel" value="${rutina.nivel || ''}">
                    <button type="button" class="btn-edit">✏️</button>
                </div>
            </label>

            <label>Frecuencia (días/semana):
                <div class="input-container">
                    <input type="number" disabled class="input_field" name="frecuencia" value="${rutina.frecuencia || 0}">
                    <button type="button" class="btn-edit">✏️</button>
                </div>
            </label>

            <label>ID Usuario:
                <div class="input-container">
                    <input type="number" disabled class="input_field" name="usuario_id" value="${rutina.usuario_id || ''}">
                    <button type="button" class="btn-edit">✏️</button>
                </div>
            </label>

            <div class="ejercicios-list">
                <h3>Ejercicios en esta rutina:</h3>
                ${ejerciciosHtml}
            </div>

            <button type="button" id="submit-btn">Guardar cambios</button>
        `;
        detallesContainer.innerHTML = html;
    } catch (err) {
        console.error(err);
        alert("Error al cargar rutina");
    }
};

// Global function to delete routine
window.viewDeleteRutina = (id) => {
    if (!id) return;

    const confirmado = confirm("¿Seguro que deseas eliminar esta rutina?");
    if (!confirmado) return;

    fetch(`/rutinas/${id}`, {
        method: 'DELETE'
    })
    .then(res => res.json())
    .then(data => {
        alert("Rutina eliminada correctamente.");
        tablaRutinas.ajax.reload(null, false);
    })
    .catch(err => alert("Error al eliminar rutina: " + err.message));
};
