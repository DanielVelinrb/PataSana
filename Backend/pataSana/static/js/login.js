document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const email = document.getElementById('inputEmail').value;
    const password = document.getElementById('inputPassword').value;

    fetch('http://ec2-18-117-255-119.us-east-2.compute.amazonaws.com/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.token) {
            // Almacenar el token en el almacenamiento local
            localStorage.setItem('token', data.token);

            // Obtener el rol del usuario
            fetch('http://ec2-18-117-255-119.us-east-2.compute.amazonaws.com/get_info_user', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${data.token}`,
                },
            })
            .then(response => response.json())
            .then(userData => {
                // Almacenar el rol del usuario en el almacenamiento local
                localStorage.setItem('role', userData.usuario[4]);
                // Redirigir según el rol del usuario
                if (userData.usuario[4] === 'admin') {
                    window.location.href = '/dashboard_admin';
                } else if (userData.usuario[4] === 'usuario') {
                    window.location.href = '/dashboard_user';
                }
                
            })
            .catch(error => {
                console.error('Error obteniendo información del usuario:', error);
            });
        } else {
            alert('Credenciales inválidas');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
