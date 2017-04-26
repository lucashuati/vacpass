$(document).ready(function () {
    $("#id_username, #id_cpf").keypress(function (e) {
        var mascara = "###.###.###-##";
        var i = this.value.length;
        if(e.keyCode < 48 || e.keyCode > 57 || i > 13){
            e.preventDefault();
        }else {
            var saida = mascara.substring(0, 1);
            var texto = mascara.substring(i);

            if (texto.substring(0, 1) != saida) {
                this.value += texto.substring(0, 1);
            }
        }
    });
    $("input").attr('title','Deu erro');
});