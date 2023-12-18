$(document).ready(function () {
    fetch("/lista/rodajson").then(response => response.json())
        .then(function (data) {
            console.log(data)
            $('#example').DataTable({
                "language": {
                    "url": "https://cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Portuguese-Brasil.json"
                },
                "data": data.cadastro,
                "columns": [
                    { "data": "nome" },
                    { "data": "idade" },
                    { "data": "endereco" },
                    { "data": "cpf" },
                    { "data": "id", render: function (data) { return '<a href="javascript:sweet(' + data + ')"><img class="icon" src="static/img/delete.png"/></a>' } },
                    { "data": "id", render: function (data) { return '<a href="/editar_cadastro/' + data + ' "><img class="icon" src="static/img/edit.png"/></a>' } }
                ]
            });
        })
})


function sweet(id) {
    console.log(id)
    Swal.fire({
        title: "Deseja Excluir a tarefa",
        showCancelButton: true,
        icon: 'question',
        confirmButtonColor: '#66e04d',
        cancelButtonColor: '#d33',
        cancelButtonText: 'Cancelar',
        confirmButtonText: 'Excluir'

    }).then((result) => {
        if (result.isConfirmed) {
            location.reload()
            let env = {}
            env.id = id
            $.ajax({
                url: "/excluir_cadastro",
                contentType: "application/json; charset=UTF-8",
                data: JSON.stringify(env),
                dataType: "json",
                type: "POST",
                success: function (response) {
                    console.log(response)
                    //$(`#row-${id}`).remove();
                },
                error: function (erro) {
                    console.log(erro)
                }
            })
        }
    })
} 