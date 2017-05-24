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
    // $("input").attr('title','Deu erro');

    //$("#id_username, #id_cpf").mask('000.000.000-00', {reverse: true});// Get the modal
    var modal = $('#myModal');
    console.log("teste");
    // Get the button that opens the modal
    var btn = $('.delete');

// Get the <span> element that closes the modal
    var span = $(".close");

// When the user clicks on the button, open the modal

    btn.click(function () {
        $(this).next().show();
    });

// When the user clicks on <span> (x), close the modal
     span.click(function () {
        $(this).parent().parent().hide();
    });
});