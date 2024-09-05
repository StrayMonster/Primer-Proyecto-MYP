//Función que hace que el boton no se active hasta que las dos opciones hayan sido activadas.
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

// Función que envía una alerta si los elementos escogidos son iguales, impidiendo enviar el formulario, en otro caso continua el protocolo de procesamiento.
function enviarFormulario(){
    const opcion1 = document.getElementById('Parametro1').value;
    const opcion2 = document.getElementById('Parametro2').value;
    if(opcion1 === opcion2){
        alert("Las opciones no pueden ser iguales.");
    } else {
        document.getElementById("FormularioClima").submit();
    }
}
