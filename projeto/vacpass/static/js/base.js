$(document).ready(function () {
    $("#id_username, #id_cpf").on('keypress',function (e) {
        var mascara = "###.###.###-##";
        var i = this.value.length;
        if(i > 13 && e.keyCode != 8){
            e.preventDefault();
        }else if(e.keyCode != 8){
            var saida = mascara.substring(0, 1);
            var texto = mascara.substring(i);

            if (texto.substring(0, 1) != saida) {
                this.value += texto.substring(0, 1);
            }
        }
    }).on('keydown', function(e) {
        if (e.keyCode==8)
         $('element').trigger('keypress');
 });
    // $("input").attr('title','Deu erro');

    //$("#id_username, #id_cpf").mask('000.000.000-00', {reverse: true});
});