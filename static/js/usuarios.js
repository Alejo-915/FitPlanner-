let tablaUsuarios;
let usuarioGlobal = null;

// Modal elements
const modalDetalles = document.getElementById('modal-detalles-usuario');
const modalTitle = document.getElementById('modal-usuario-title');
const closeModalBtn = document.getElementById('close-modal-btn-usuario');
const detallesContainer = document.getElementById('detalles-container-usuario');

// Close modal helper
const closeModal = () => {
    if (modalDetalles) modalDetalles.style.display = 'none';
};

$(document).ready(function() {
    // Initialize DataTables
    tablaUsuarios = $('#tabla-usuarios').DataTable({
        ajax: {
            url: "/usuarios/", // Endpoint from routes/usuario.py
            dataSrc: "", // API returns a list [{}, {}], not { data: [] }
            error: function(xhr) { console.error('AJAX Error:', xhr); }
        },
        columns: [
            { data: "id" },
            { data: "nombre" },
            { data: "correo" },
            { data: "edad" },
            { data: "peso" },
            { data: "altura" },
            { data: "objetivo" },
            { 
                data: "activo",
                render: function(data) {
                    return data ? '<span class="badge badge-success">Activo</span>' : '<span class="badge badge-danger">Inactivo</span>';
                }
            },
            {
                data: null,
                orderable: false,
                render: function(data, type, row) {
                    return `<div class="btn-group">
                        <button class="btn btn-sm btn-danger" onClick="viewDeleteUsuario(${row.id})">🗑️</button>
                        <button class="btn btn-sm btn-info" onClick="viewDetailsUsuario(${row.id})">✏️</button>
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
            info: "_START_ a _END_ de _TOTAL_ usuarios",
            paginate: { previous: "‹", next: "›" },
            buttons: { excel: "Excel", csv: "CSV", pdf: "PDF", print: "Imprimir" },
            search: "Buscar:",
            lengthMenu: "Mostrar _MENU_ usuarios por página",
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
                    // Convert numeric fields
                    if (['edad', 'peso', 'altura'].includes(input.name)) {
                        data[input.name] = Number(input.value);
                    } else {
                        data[input.name] = input.value;
                    }
                });
    
                fetch(`/usuarios/${usuarioGlobal.id}`, {
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
                    alert('Usuario actualizado correctamente');
                    closeModal();
                    tablaUsuarios.ajax.reload(null, false);
                })
                .catch(err => {
                    console.error('Error al actualizar usuario:', err);
                    alert('Error al actualizar usuario');
                });
            }
        });
    }
});

// Helper to fetch user details
const fetchUsuario = async (id) => {
    const res = await fetch(`/usuarios/${id}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
};

// Global function to open modal details (called from HTML onClick)
window.viewDetailsUsuario = async (id) => {
    try {
        const usuario = await fetchUsuario(id);
        usuarioGlobal = usuario;
        modalTitle.textContent = `Usuario #${usuario.id}`;
        modalDetalles.style.display = 'flex';

        let html = `
            <label>Nombre:
                <div class="input-container">
                    <input disabled class="input_field" name="nombre" value="${usuario.nombre || ''}">
                    <button type="button" class="btn-edit">✏️</button>
                </div>
            </label>

            <label>Correo:
                <div class="input-container">
                    <input disabled class="input_field" name="correo" value="${usuario.correo || ''}">
                    <button type="button" class="btn-edit">✏️</button>
                </div>
            </label>

            <label>Edad:
                <div class="input-container">
                    <input type="number" disabled class="input_field" name="edad" value="${usuario.edad || 0}">
                    <button type="button" class="btn-edit">✏️</button>
                </div>
            </label>

            <label>Peso:
                <div class="input-container">
                    <input type="number" step="0.1" disabled class="input_field" name="peso" value="${usuario.peso || 0}">
                    <button type="button" class="btn-edit">✏️</button>
                </div>
            </label>

            <label>Altura:
                <div class="input-container">
                    <input type="number" step="0.01" disabled class="input_field" name="altura" value="${usuario.altura || 0}">
                    <button type="button" class="btn-edit">✏️</button>
                </div>
            </label>

            <label>Objetivo:
                <div class="input-container">
                    <input disabled class="input_field" name="objetivo" value="${usuario.objetivo || ''}">
                    <button type="button" class="btn-edit">✏️</button>
                </div>
            </label>

            <button type="button" id="submit-btn">Guardar cambios</button>
        `;
        detallesContainer.innerHTML = html;
    } catch (err) {
        console.error(err);
        alert("Error al cargar usuario");
    }
};

// Global function to delete user
window.viewDeleteUsuario = (id) => {
    if (!id) return;

    const confirmado = confirm("¿Seguro que deseas eliminar este usuario?");
    if (!confirmado) return;

    fetch(`/usuarios/${id}`, {
        method: 'DELETE'
    })
    .then(res => res.json())
    .then(data => {
        alert("Usuario eliminado (desactivado) correctamente.");
        tablaUsuarios.ajax.reload(null, false);
    })
    .catch(err => alert("Error al eliminar usuario: " + err.message));
};
