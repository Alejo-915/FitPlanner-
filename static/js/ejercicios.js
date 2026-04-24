let tablaEjercicios;
let ejercicioGlobal = null;

const modalDetalles = document.getElementById('modal-detalles-ejercicio');
const modalTitle = document.getElementById('modal-ejercicio-title');
const closeModalBtn = document.getElementById('close-modal-btn-ejercicio');
const detallesContainer = document.getElementById('detalles-container-ejercicio');
const modalCrear = document.getElementById('modal-crear-ejercicio');
const btnCrearEjercicio = document.getElementById('btn-crear-ejercicio');
const closeModalCrearBtn = document.getElementById('close-modal-crear-btn');
const formCrear = document.getElementById('modal-crear-content');

const closeModal = () => { if (modalDetalles) modalDetalles.style.display = 'none'; };
const closeModalCrear = () => { if (modalCrear) modalCrear.style.display = 'none'; };

function youtubeEmbed(url) {
    if (!url) return null;
    const match = url.match(/(?:v=|youtu\.be\/)([a-zA-Z0-9_-]{11})/);
    return match ? `https://www.youtube.com/embed/${match[1]}` : null;
}

function badgeDificultad(d) {
    const map = {
        'fácil': 'background:#23d160;color:#fff;',
        'moderado': 'background:#ffdd57;color:#333;',
        'difícil': 'background:#ff3860;color:#fff;',
    };
    const style = map[d] || 'background:#ddd;color:#333;';
    return `<span style="padding:2px 8px;border-radius:12px;font-size:12px;${style}">${d || 'moderado'}</span>`;
}

$(document).ready(function () {
    tablaEjercicios = $('#tabla-ejercicios').DataTable({
        ajax: { url: '/ejercicios/', dataSrc: '', error: (xhr) => console.error('AJAX:', xhr) },
        columns: [
            { data: 'id' },
            { data: 'nombre' },
            { data: 'grupo_muscular' },
            { data: 'equipo' },
            { data: 'dificultad', render: (d) => badgeDificultad(d) },
            {
                data: 'restricciones',
                render: (d) => d
                    ? d.split(',').map(r => `<span style="background:#fee;color:#c00;border-radius:8px;padding:1px 6px;font-size:11px;margin:1px;display:inline-block;">${r.trim()}</span>`).join('')
                    : '<span style="color:#999;">Ninguna</span>',
            },
            {
                data: 'video_url',
                render: (d) => d
                    ? `<a href="${d}" target="_blank" class="button is-small is-link"><i class="fab fa-youtube"></i> Ver</a>`
                    : '<span style="color:#999;">Sin video</span>',
            },
            {
                data: null, orderable: false,
                render: (data, type, row) =>
                    `<div class="btn-group">
                        <button class="btn btn-sm btn-danger" onclick="viewDeleteEjercicio(${row.id})">🗑️</button>
                        <button class="btn btn-sm btn-info" onclick="viewDetailsEjercicio(${row.id})">✏️</button>
                    </div>`,
            },
        ],
        dom: "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>><'row'<'col-sm-12'tr>><'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>><'row'<'col-sm-12'B>>",
        buttons: [
            { extend: 'excel', text: 'Excel', className: 'btn btn-success' },
            { extend: 'csv', text: 'CSV', className: 'btn btn-info' },
            { extend: 'pdf', text: 'PDF', className: 'btn btn-danger' },
            { extend: 'print', text: 'Imprimir', className: 'btn btn-warning' },
        ],
        language: { info: '_START_ a _END_ de _TOTAL_ ejercicios', search: 'Buscar:', lengthMenu: 'Mostrar _MENU_ por página' },
    });

    if (closeModalBtn) closeModalBtn.addEventListener('click', e => { e.preventDefault(); closeModal(); });
    window.addEventListener('click', e => {
        if (e.target === modalDetalles) closeModal();
        if (e.target === modalCrear) closeModalCrear();
    });
    if (btnCrearEjercicio) btnCrearEjercicio.addEventListener('click', e => { e.preventDefault(); abrirModalCrear(); });
    if (closeModalCrearBtn) closeModalCrearBtn.addEventListener('click', e => { e.preventDefault(); closeModalCrear(); });
    if (formCrear) formCrear.addEventListener('submit', async e => { e.preventDefault(); await crearNuevoEjercicio(); });

    if (detallesContainer) {
        detallesContainer.addEventListener('click', e => {
            e.preventDefault();
            if (e.target.classList.contains('btn-edit')) {
                const inp = e.target.closest('.input-container').querySelector('.input_field');
                inp.disabled = !inp.disabled;
                e.target.textContent = inp.disabled ? '✏️' : '✔️';
                return;
            }
            if (e.target.id === 'submit-btn') {
                const data = {};
                document.querySelectorAll('#detalles-container-ejercicio .input_field').forEach(i => { data[i.name] = i.value; });
                fetch(`/ejercicios/${ejercicioGlobal.id}`, {
                    method: 'PATCH',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data),
                })
                .then(r => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json(); })
                .then(() => { alert('Ejercicio actualizado'); closeModal(); tablaEjercicios.ajax.reload(null, false); })
                .catch(err => alert('Error: ' + err.message));
            }
        });
    }
});

function abrirModalCrear() {
    ['nuevo-nombre', 'nuevo-equipo', 'nuevo-descripcion', 'nuevo-video-url'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.value = '';
    });
    document.querySelectorAll('.chk-restriccion').forEach(c => c.checked = false);
    modalCrear.style.display = 'flex';
}

async function crearNuevoEjercicio() {
    const nombre = document.getElementById('nuevo-nombre').value;
    const grupo_muscular = document.getElementById('nuevo-grupo-muscular').value;
    const equipo = document.getElementById('nuevo-equipo').value;
    const dificultad = document.getElementById('nuevo-dificultad').value;
    const descripcion = document.getElementById('nuevo-descripcion').value;
    const video_url = document.getElementById('nuevo-video-url').value;
    const restricciones = Array.from(document.querySelectorAll('.chk-restriccion:checked'))
        .map(c => c.value).join(',') || null;

    if (!nombre || !grupo_muscular || !equipo || !descripcion) {
        alert('Completa todos los campos obligatorios');
        return;
    }

    try {
        const res = await fetch('/ejercicios/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nombre, grupo_muscular, equipo, dificultad, descripcion, video_url: video_url || null, restricciones }),
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        alert('¡Ejercicio creado!');
        closeModalCrear();
        tablaEjercicios.ajax.reload(null, false);
    } catch (err) {
        alert('Error al crear ejercicio: ' + err.message);
    }
}

window.viewDetailsEjercicio = async (id) => {
    try {
        const res = await fetch(`/ejercicios/${id}`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const ej = await res.json();
        ejercicioGlobal = ej;
        modalTitle.textContent = `Ejercicio #${ej.id}`;
        modalDetalles.style.display = 'flex';

        const embedUrl = youtubeEmbed(ej.video_url);
        const videoSection = embedUrl
            ? `<div style="margin-top:12px;"><iframe width="100%" height="200" src="${embedUrl}" frameborder="0" allowfullscreen></iframe></div>`
            : ej.video_url
                ? `<a href="${ej.video_url}" target="_blank" class="button is-link"><i class="fab fa-youtube"></i> Ver Video</a>`
                : '<p style="color:#999;">Sin video</p>';

        detallesContainer.innerHTML = `
            <label>Nombre:<div class="input-container"><input disabled class="input_field" name="nombre" value="${ej.nombre || ''}"><button type="button" class="btn-edit">✏️</button></div></label>
            <label>Grupo Muscular:<div class="input-container"><input disabled class="input_field" name="grupo_muscular" value="${ej.grupo_muscular || ''}"><button type="button" class="btn-edit">✏️</button></div></label>
            <label>Equipo:<div class="input-container"><input disabled class="input_field" name="equipo" value="${ej.equipo || ''}"><button type="button" class="btn-edit">✏️</button></div></label>
            <label>Dificultad:<div class="input-container"><input disabled class="input_field" name="dificultad" value="${ej.dificultad || 'moderado'}"><button type="button" class="btn-edit">✏️</button></div></label>
            <label>Restricciones:<div class="input-container"><input disabled class="input_field" name="restricciones" value="${ej.restricciones || ''}"><button type="button" class="btn-edit">✏️</button></div></label>
            <label>Descripción:<div class="input-container"><textarea disabled class="input_field" name="descripcion" rows="3">${ej.descripcion || ''}</textarea><button type="button" class="btn-edit">✏️</button></div></label>
            <label>URL Video:<div class="input-container"><input disabled class="input_field" name="video_url" value="${ej.video_url || ''}"><button type="button" class="btn-edit">✏️</button></div></label>
            ${videoSection}
            <button type="button" id="submit-btn">Guardar cambios</button>
        `;
    } catch (err) {
        alert('Error al cargar ejercicio: ' + err.message);
    }
};

window.viewDeleteEjercicio = (id) => {
    if (!id || !confirm('¿Seguro que deseas eliminar este ejercicio?')) return;
    fetch(`/ejercicios/${id}`, { method: 'DELETE' })
        .then(r => r.json())
        .then(() => { alert('Ejercicio eliminado'); tablaEjercicios.ajax.reload(null, false); })
        .catch(err => alert('Error: ' + err.message));
};