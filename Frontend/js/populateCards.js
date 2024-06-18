document.addEventListener("DOMContentLoaded", function() {
    fetch("http://127.0.0.1:8000/api/mascotas/")
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById("pet-cards-container");
            data.forEach(pet => {
                const card = document.createElement("div");
                card.className = "col-xl-3 col-md-6 mb-4";
                card.innerHTML = `
                    <div class="card">
                        <img src="assets/img/dog-svgrepo-com.svg" class="card-img-top" alt="Icono de un perro">
                        <div class="card-body">
                            <h5 class="card-title">${pet.Nombre}</h5>
                            <p class="card-text"><strong>Especie:</strong> ${pet.Especie}</p>
                            <p class="card-text"><strong>Raza:</strong> ${pet.Raza}</p>
                            <p class="card-text"><strong>Edad:</strong> ${pet.Edad} años</p>
                            <p class="card-text"><strong>Observaciones:</strong> ${pet.Observaciones}</p>
                        </div>
                    </div>
                `;
                container.appendChild(card);
            });
        })
        .catch(error => console.error("Error fetching data: ", error));
});
