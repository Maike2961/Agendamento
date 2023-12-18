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
                    { "data": "id", render: function (data) { return '<a href="/remover_cadastro/' + data + ' "><img class="icon" src="static/img/delete.png"/></a>' } },
                    { "data": "id", render: function (data) { return '<a href="/editar_cadastro/' + data + ' "><img class="icon" src="static/img/edit.png"/></a>' } }
                ]
            });
        })
})