function atualizarHora(){
    const agora = new Date();
    hora.textContent = agora.toLocaleTimeString("pt-BR",{hour:"2-digit",minute:"2-digit"});
}

const hora = document.querySelector("#hora");
atualizarHora();
setInterval(atualizarHora,1000);