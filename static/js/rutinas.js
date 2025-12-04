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
    console.log('Initializing DataTable...');
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
                    // console.log('Rendering row:', row.id);
                    return `<div class="btn-group">
                        <button class="btn btn-sm btn-primary" onClick="viewShowRutina(${row.id})">👁️</button>
                        <button class="btn btn-sm btn-info" onClick="viewEditRutina(${row.id})">✏️</button>
                        <button class="btn btn-sm btn-danger" onClick="viewDeleteRutina(${row.id})">🗑️</button>
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
    // Create Routine Modal Elements
    const btnCrearRutina = document.getElementById('btn-crear-rutina');
    const modalCrearRutina = document.getElementById('modal-crear-rutina');
    const closeCrearRutinaBtn = document.getElementById('close-crear-rutina-btn');
    const formCrearRutina = document.getElementById('form-crear-rutina');
    const listaEjerciciosContainer = document.getElementById('lista-ejercicios-seleccion');
    const ejerciciosParametrosContainer = document.getElementById('ejercicios-parametros');

    // Open Create Modal
    if (btnCrearRutina) {
        btnCrearRutina.addEventListener('click', async () => {
            modalCrearRutina.style.display = 'flex';
            await cargarEjerciciosParaSeleccion();
        });
    }

    // Close Create Modal
    if (closeCrearRutinaBtn) {
        closeCrearRutinaBtn.addEventListener('click', (e) => {
            e.preventDefault();
            modalCrearRutina.style.display = 'none';
        });
    }

    window.addEventListener('click', (e) => {
        if (e.target === modalCrearRutina) {
            modalCrearRutina.style.display = 'none';
        }
    });

    // Load Exercises for Selection
    async function cargarEjerciciosParaSeleccion() {
        try {
            listaEjerciciosContainer.innerHTML = '<p>Cargando...</p>';
            const res = await fetch('/ejercicios/');
            if (!res.ok) throw new Error('Error al cargar ejercicios');
            const ejercicios = await res.json();

            let html = '';
            if (ejercicios.length === 0) {
                html = '<p>No hay ejercicios disponibles.</p>';
            } else {
                ejercicios.forEach(ej => {
                    html += `
                        <div style="display:flex; align-items:center; margin-bottom:5px;">
                            <input type="checkbox" class="ejercicio-check" value="${ej.id}" data-nombre="${ej.nombre}" id="check-ej-${ej.id}">
                            <label for="check-ej-${ej.id}" style="margin-left:8px; cursor:pointer;">
                                <strong>${ej.nombre}</strong> (${ej.grupo_muscular})
                            </label>
                        </div>
                    `;
                });
            }
            listaEjerciciosContainer.innerHTML = html;

            // Add listeners to checkboxes to show parameter inputs
            document.querySelectorAll('.ejercicio-check').forEach(check => {
                check.addEventListener('change', actualizarParametrosEjercicios);
            });

        } catch (error) {
            console.error(error);
            listaEjerciciosContainer.innerHTML = '<p style="color:red">Error al cargar ejercicios</p>';
        }
    }

    function actualizarParametrosEjercicios(e) {
        const check = e.target;
        const id = check.value;
        const nombre = check.dataset.nombre;

        if (check.checked) {
            // Add inputs for this exercise
            const div = document.createElement('div');
            div.id = `params-ej-${id}`;
            div.className = 'params-ejercicio-row';
            div.style = 'border:1px solid #eee; padding:10px; margin-bottom:10px; background:#f9f9f9;';
            div.innerHTML = `
                <p style="margin:0 0 5px 0; font-weight:bold; color:#333;">${nombre}</p>
                <div style="display:flex; gap:10px;">
                    <div>
                        <label style="font-size:0.8em">Series</label>
                        <input type="number" name="series_${id}" value="4" min="1" style="width:60px;">
                    </div>
                    <div>
                        <label style="font-size:0.8em">Reps</label>
                        <input type="number" name="reps_${id}" value="12" min="1" style="width:60px;">
                    </div>
                    <div>
                        <label style="font-size:0.8em">Duración (min)</label>
                        <input type="number" name="duracion_${id}" value="0" min="0" style="width:80px;">
                    </div>
                </div>
            `;
            ejerciciosParametrosContainer.appendChild(div);
        } else {
            // Remove inputs
            const div = document.getElementById(`params-ej-${id}`);
            if (div) div.remove();
        }
    }

    // Handle Create Routine Submit
    if (formCrearRutina) {
        formCrearRutina.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const nombre = formCrearRutina.querySelector('input[name="nombre"]').value;
            const nivel = formCrearRutina.querySelector('select[name="nivel"]').value;
            const frecuencia = parseInt(formCrearRutina.querySelector('input[name="frecuencia"]').value);
            const usuario_id = parseInt(formCrearRutina.querySelector('input[name="usuario_id"]').value);

            // 1. Create Routine
            try {
                const resRutina = await fetch('/rutinas/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ nombre, nivel, frecuencia, usuario_id })
                });

                if (!resRutina.ok) {
                    const err = await resRutina.json();
                    throw new Error(err.detail || 'Error al crear rutina');
                }

                const dataRutina = await resRutina.json();
                const rutinaId = dataRutina.rutina.id;

                // 2. Assign Exercises
                const checkboxes = document.querySelectorAll('.ejercicio-check:checked');
                for (const check of checkboxes) {
                    const ejId = check.value;
                    const series = document.querySelector(`input[name="series_${ejId}"]`).value;
                    const repeticiones = document.querySelector(`input[name="reps_${ejId}"]`).value;
                    const duracion = document.querySelector(`input[name="duracion_${ejId}"]`).value;

                    await fetch('/rutinas_ejercicios/', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            rutina_id: rutinaId,
                            ejercicio_id: parseInt(ejId),
                            series: parseInt(series),
                            repeticiones: parseInt(repeticiones),
                            duracion: parseInt(duracion)
                        })
                    });
                }

                alert('Rutina creada y ejercicios asignados correctamente');
                modalCrearRutina.style.display = 'none';
                formCrearRutina.reset();
                ejerciciosParametrosContainer.innerHTML = '';
                tablaRutinas.ajax.reload(null, false);

            } catch (error) {
                console.error(error);
                alert('Error: ' + error.message);
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

// Global function to show read-only details
window.viewShowRutina = async (id) => {
    try {
        const rutina = await fetchRutina(id);
        modalTitle.textContent = `Detalles Rutina #${rutina.id}`;
        modalDetalles.style.display = 'flex';

        // Construct exercises table
        let ejerciciosHtml = '';
        if (rutina.ejercicios && rutina.ejercicios.length > 0) {
            ejerciciosHtml = `
                <table class="table table-bordered table-striped" style="width:100%; margin-top:10px;">
                    <thead>
                        <tr>
                            <th>Ejercicio</th>
                            <th>Grupo Muscular</th>
                            <th>Equipo</th>
                            <th>Series</th>
                            <th>Reps</th>
                            <th>Duración</th>
                        </tr>
                    </thead>
                    <tbody>
            `;
            rutina.ejercicios.forEach(ej => {
                ejerciciosHtml += `
                    <tr>
                        <td>${ej.nombre}</td>
                        <td>${ej.grupo_muscular}</td>
                        <td>${ej.equipo || '-'}</td>
                        <td>${ej.series}</td>
                        <td>${ej.repeticiones}</td>
                        <td>${ej.duracion} min</td>
                    </tr>
                `;
            });
            ejerciciosHtml += '</tbody></table>';
        } else {
            ejerciciosHtml = '<p>No hay ejercicios asignados.</p>';
        }

        let html = `
            <div class="details-view">
                <p><strong>Nombre:</strong> ${rutina.nombre_rutina}</p>
                <p><strong>Nivel:</strong> ${rutina.nivel}</p>
                <p><strong>Frecuencia:</strong> ${rutina.frecuencia} días/semana</p>
                <p><strong>Usuario:</strong> ${rutina.usuario_nombre} (ID: ${rutina.usuario_id})</p>
                
                <hr>
                <h3>Ejercicios Asignados</h3>
                ${ejerciciosHtml}
            </div>
        `;
        detallesContainer.innerHTML = html;
    } catch (err) {
        console.error(err);
        alert("Error al cargar detalles de la rutina");
    }
};

// Global function to edit details
window.viewEditRutina = async (id) => {
    try {
        const rutina = await fetchRutina(id);
        rutinaGlobal = rutina;
        modalTitle.textContent = `Editar Rutina #${rutina.id}`;
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
