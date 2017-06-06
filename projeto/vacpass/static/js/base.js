$(document).ready(function () {
    console.log("TESTE");

    $("#id_username, #id_cpf").on('keypress', function (e) {
        var mascara = "###.###.###-##";
        var i = this.value.length;
        if (i > 13 && e.keyCode != 8) {
            e.preventDefault();
        } else if (e.keyCode != 8) {
            var saida = mascara.substring(0, 1);
            var texto = mascara.substring(i);

            if (texto.substring(0, 1) != saida) {
                this.value += texto.substring(0, 1);
            }
        }
    }).on('keydown', function (e) {
        if (e.keyCode == 8)
            $('element').trigger('keypress');
    });

    // When the user clicks on the button, open the modal
    $('.abremodal').click(function () {
        $(this).next().show();
    });

    // When the user clicks on <span> (x), close the modal
     $(".close").click(function () {
        $(this).parent().parent().hide();
    });
});

//Estas funções estão a ser usadas em views.py. Não deixe o pycharm lhe enganar
function fecha_modal(){
    $(".close").trigger("click")
}

function adiciona_mensagem(classe, mensagem){
    $(".messagelist").append($("<li>").attr('class', classe).text(mensagem));
}