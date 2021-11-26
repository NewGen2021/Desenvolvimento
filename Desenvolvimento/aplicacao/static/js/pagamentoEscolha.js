function ChangeToReg()
{
location.href="regUsers.html"
console.log("teste");
}

$('#tipoPagamento input[type="radio"]').change(function() {
  console.log("testePagamentoTotal");
    let name = this.value;
  
  $('[data-label=' + name + ']').css('display', this.checked ? '' : 'none');
 
 });
 
 $("input[type=radio]").on("change", function() {
  console.log("teste");
  if ($(this).val() == "pagar10") {
      $("[name=formPessoaFisica]").show();
      $("[name=formPessoaJuridica]").hide();
  } else if ($(this).val() == "pagarTotal") {
      $("[name=valor_compra]").show(); //variavel de preco total
      $("[name=valor_compra]").hide();
  }
 
 });