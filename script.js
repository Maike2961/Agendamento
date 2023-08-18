const cpf = document.getElementById("cpf");

cpf.addEventListener('keypress', () => {
    let valida = cpf.value.length

    if(valida === 3|| valida === 7){
        cpf.value += '.'
    }else if (valida === 11){
        cpf.value += '-'
        console.log(valida)
    }
})