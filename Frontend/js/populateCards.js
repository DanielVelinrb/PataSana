document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('pet-cards-container');
    const token = 'Bearer ' + localStorage.getItem('token'); // Asumiendo que guardas el token en localStorage

    fetch('/mascotas/listar', {
        method: 'GET',
        headers: {
            'Authorization': "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYmEyNjc0OTYtMGMwNy00ZGM0LTg1NzMtYWJmOTAxOGRmYzRlIiwidXNlcl9yb2wiOiJ1c3VhcmlvIn0.0aDJbF5uhjwgZN6UZ8YKEmRtqqZtxLF4ZI08E_rB9mg",
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.mascotas && data.mascotas.length > 0) {
            data.mascotas.forEach(mascotaArray => {
                // Desestructurando el array de mascota
                const [id, nombre, raza, especie, edad, observaciones, userId] = mascotaArray;

                const card = document.createElement('div');
                card.className = 'col-xl-3 col-md-6 mb-4';

                card.innerHTML = `
                    <div class="card">
                        <div class="card-header">
                            ${nombre}
                        </div>
                        <img src="/assets/img/dog-svgrepo-com.svg" class="card-img-top" alt="Icono de un perro">
                        <div class="card-body">
                            <p class="card-text"><strong>Especie:</strong> ${especie}</p>
                            <p class="card-text"><strong>Raza:</strong> ${raza}</p>
                            <p class="card-text"><strong>Edad:</strong> ${edad} años</p>
                            <p class="card-text"><strong>Observaciones:</strong> ${observaciones}</p>
                        </div>
                    </div>
                `;
                container.appendChild(card);
            });
        } else {
            container.innerHTML = '<p>No hay mascotas registradas.</p>';
        }
    })
    .catch(error => {
        console.error('Error al obtener las mascotas:', error);
        container.innerHTML = '<p>Error al cargar las mascotas.</p>';
    });
    
});
