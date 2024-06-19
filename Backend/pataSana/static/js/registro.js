document.getElementById('registrationForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const nombre = document.getElementById('inputFirstName').value;
    const apellido = document.getElementById('inputLastName').value;
    const email = document.getElementById('inputEmail').value;
    const password = document.getElementById('inputPassword').value;
    const rol = document.getElementById('inputRole').value;

    const nombreCompleto = `${nombre} ${apellido}`;

    fetch('http://127.0.0.1:8000/usuarios/crear', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ nombre: nombreCompleto, email, password, rol }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            // Redirigir a la página de inicio de sesión
            alert(data.error || '¡Has creado tu usuario!');
            window.location.href = '/';
        } else {
            alert(data.error || 'Error al registrar usuario');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
