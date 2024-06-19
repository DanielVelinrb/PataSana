document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const email = document.getElementById('inputEmail').value;
    const password = document.getElementById('inputPassword').value;

    fetch('/api/iniciar_sesion/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.token) {
            // Almacenar el token en el almacenamiento local o en una cookie
            localStorage.setItem('token', data.token);
            // Redirigir a la página de inicio
            window.location.href = 'index.html';
        } else {
            alert('Credenciales inválidas');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
