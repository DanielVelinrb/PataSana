document.addEventListener('DOMContentLoaded', function() {
    const resetPasswordBtn = document.querySelector('#resetPasswordBtn');
    resetPasswordBtn.addEventListener('click', function(event) {
        event.preventDefault();
        alert('¡Se ha enviado el correo!');
        window.location.href = '/';
    });
});
