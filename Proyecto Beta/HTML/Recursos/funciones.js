
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
        alert("Respuestas enviadas correctamente.");
        window.location.href = "./Front2.html";
    }
}