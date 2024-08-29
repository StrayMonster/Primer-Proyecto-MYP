
function validarFormulario(){
    const opcion1 = document.getElementById('Parametro1').value;
    const opcion2 = document.getElementById('Parametro2').value;
    const sendButton = document.getElementById('enviar');

    if(opcion1 && opcion2) {
        sendButton.disabled = false;
    } else {
        sendButton.disabled = true;
    }
}

function enviarFormulario(){
    const opcion1 = document.getElementById('Parametro1').value;
    const opcion2 = document.getElementById('Parametro2').value;
    if(opcion1 === opcion2){
        alert("Las opciones no pueden ser iguales.");
    } else {
        fetch('procesar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({Parametro1: opcion1, Parametro2: opcion2})
        })
        .then(response => response.json())
        .then(data => {
            if(data.success){
                alert("Respuestas enviadas correctamente.");
                window.location.href = 'resultado?parametro1=${opcion1}&parametro2=${opcion2}';
                window.location.href = "./Front2.html";
            } else {
                alert("Error al procesar datos.");
            }
        });

    }
}