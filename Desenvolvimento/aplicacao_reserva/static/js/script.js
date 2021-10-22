// let colorPicker = document.getElementById("colorPicker");
// let box = document.getElementById("box");
// let output = document.getElementById("output");
// let alterabackground = document.getElementById("alterabackground");

// box.style.backgroundColor = colorPicker.value;

// colorPicker.addEventListener("input", function(event) {
//   box.style.backgroundColor = event.target.value;
// }, false);

// colorPicker.addEventListener("change", function(event) {
//     alterabackground.style.backgroundColor = box;
// }, false);

function ChangeToReg()
{
location.href="regUsers.html"
console.log("teste");
}

$('#cadastro input[type="radio"]').change(function() {
  console.log("teste");
    let name = this.value;
  
  $('[data-label=' + name + ']').css('display', this.checked ? '' : 'none');
 
 });
 
 $("input[type=radio]").on("change", function() {
  console.log("teste");
  if ($(this).val() == "pessoaFisica") {
      $("[name=formPessoaFisica]").show();
      $("[name=formPessoaJuridica]").hide();
  } else if ($(this).val() == "pessoaJuridica") {
      $("[name=formPessoaJuridica]").show();
      $("[name=formPessoaFisica]").hide();
  }
 
 });
 
//  $("input[type=radio]").on("change", function() {
//   if ($(this).val() == "pessoaFisica") {
//     $("nome, senha, cpf_cnpj, data_nascimento, genero, email, telefone, logradouro, numero, bairro, cidade, estado, cep").show();
//     $("nome, senha, cpf_cnpj, email, telefone, logradouro, numero, bairro, cidade, estado, cep").hide();
//   } else if ($(this).val() == "pessoaJuridica") {
//    $("nome, senha, cpf_cnpj, email, telefone, logradouro, numero, bairro, cidade, estado, cep").show();
//     $("nome, senha, cpf_cnpj, data_nascimento, genero, email, telefone, logradouro, numero, bairro, cidade, estado, cep").hide();
//   }

// });
