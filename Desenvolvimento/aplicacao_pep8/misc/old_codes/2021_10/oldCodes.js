cep_verifier.js = ''

/* const response = fetch('http://cep.republicavirtual.com.br/web_cep.php?cep=91010000&formato=jsonp');
const myJson = response.json; //extract JSON from the http response
  // do something with myJson
window.alert(myJson)
window.alert('teste') */

/* const userAction = async () => {
  const response = await fetch('http://example.com/movies.json');
  const myJson = await response.json(); //extract JSON from the http response
  // do something with myJson
  window.alert(myJson)
} */

/* window.onload = function UserAction() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
       if (this.readyState == 4 && this.status == 200) {
           alert(this.responseText);
       }
  };
  xhttp.open("POST", "http://cep.republicavirtual.com.br/web_cep.php?cep=91010000&formato=jsonp", true);
  xhttp.setRequestHeader("Content-type", "application/json");
} */

/* $.ajax({ 
  type: "GET",
  dataType: "jsonp",
  url: "http://cep.republicavirtual.com.br/web_cep.php?cep=91010000&formato=jsonp&callback=?",
  success: function(data){
    console.log(data);
    alert(data.bairro)
  }
}); */

/* function consultar_cep(cep){
  cep = cep.replace('-', '')
  var url = 'http://cep.republicavirtual.com.br/web_cep.php?cep=' + cep + '&formato=jsonp';
  return fetch(url)
 .then(res => res.json())
 .then(json => {
    if (json.resultado == '0')
      console.log('CEP NÃO ENCONTRADO');
      console.log(url);
    if (json.resultado == '1') {
      console.log('CEP ENCONTRADO AAAAAE');
      return json;
    }
      })
} */

/* async function consultar_cep(cep){
  cep = cep.replace('-', '')
  var url = 'http://cep.republicavirtual.com.br/web_cep.php?cep=' + cep + '&formato=jsonp';
  const res = await fetch(url);
  const json = await res.json();
  if (json.resultado == '0')
    console.log('CEP NÃO ENCONTRADO');
  console.log(url);
  if (json.resultado == '1') {
    console.log('CEP ENCONTRADO AAAAAE');
    return json;
  }
} */

/* fetch('http://cep.republicavirtual.com.br/web_cep.php?cep=91010000&formato=jsonp')
 .then(res => res.json())
 .then(json => {
    if (json.resultado == '0')
      console.log('CEP NÃO ENCONTRADO');
    if (json.resultado == '1') {
      console.log('SUCESSO');
      console.log(json);
    }
      }) */

OLDcep_verifier = '';

// async function consultar_cep(cep){
//   cep = cep.replace('-', '')
//   var url = 'http://cep.republicavirtual.com.br/web_cep.php?cep=' + cep + '&formato=jsonp';
//   const res = await fetch(url);
//   const promiseJson = await res.json();
//   if (promiseJson.resultado == '0')
//     console.log('CEP NÃO ENCONTRADO');
//   if (promiseJson.resultado == '1') {
//     return promiseJson;
//   }
// }

// var alterar_campos = function(tipo){
//   let id = `id_${tipo}_cep`;
//   var valor_cep = document.getElementById(id).value;
//   let resultado = consultar_cep(valor_cep);
//   resultado.then(jsonCep => {
//     // console.log(jsonCep);
//     if (jsonCep != undefined){
//       document.getElementById(`id_${tipo}_bairro`).value = jsonCep.bairro;
//       document.getElementById(`id_${tipo}_cidade`).value = jsonCep.cidade;
//       document.getElementById(`id_${tipo}_logradouro`).value = jsonCep.tipo_logradouro + ' ' + jsonCep.logradouro;
//       document.getElementById(`id_${tipo}_estado`).value = jsonCep.uf;
//     }
//     else{
//       document.getElementById(`id_${tipo}_bairro`).value = '';
//       document.getElementById(`id_${tipo}_cidade`).value = '';
//       document.getElementById(`id_${tipo}_logradouro`).value = '';
//       document.getElementById(`id_${tipo}_estado`).value = '';
//     }
//   })
// }



// /* var inputPessoaCep = document.querySelector("#id_pessoa_cep");
// inputPessoaCep.addEventListener("change", e => {
//   var valor_cep = document.getElementById("id_pessoa_cep").value;
//   console.log('Dentro do input consult');
//   let resultado = consultar_cep(valor_cep);
//   resultado.then(jsonCep => {
//     console.log(jsonCep);
//     if (jsonCep != undefined){
//       document.getElementById("id_pessoa_bairro").value = jsonCep.bairro;
//       document.getElementById("id_pessoa_cidade").value = jsonCep.cidade;
//       document.getElementById("id_pessoa_logradouro").value = jsonCep.tipo_logradouro + ' ' + jsonCep.logradouro;
//       document.getElementById("id_pessoa_estado").value = jsonCep.uf;
//     }
//     else{
//       document.getElementById("id_pessoa_bairro").value = '';
//       document.getElementById("id_pessoa_cidade").value = '';
//       document.getElementById("id_pessoa_logradouro").value = '';
//       document.getElementById("id_pessoa_estado").value = '';
//     }
//   })
// }); */

// // CONFERE FORM PESSOA
// var inputPessoaCep = document.querySelector("#id_pessoa_cep");
// inputPessoaCep.addEventListener("change", e => {alterar_campos('pessoa')});

// // CONFERE FORM EMPRESA
// var inputPessoaCep = document.querySelector("#id_pessoa_cep");
// inputPessoaCep.addEventListener("change", e => {alterar_campos('pessoa')});

// // CONFERE FORM FUNCIONARIO

// // CONFERE FORM ADMINISTRADOR

// // CONFERE CAMPO CEP DO FORMULÁRIO empresa E ALTERA OS DADOS CONFORME O CEP INSERIDO
// var inputEmpresaCep = document.querySelector("#id_empresa_cep");
// inputEmpresaCep.addEventListener("change", e => {
//   var valor_cep = document.getElementById("id_empresa_cep").value;
//   console.log('Dentro do input consult');
//   let resultado = consultar_cep(valor_cep);
//   resultado.then(jsonCep => {
//     console.log(jsonCep);
//     if (jsonCep != undefined){
//       document.getElementById("id_empresa_bairro").value = jsonCep.bairro;
//       document.getElementById("id_empresa_cidade").value = jsonCep.cidade;
//       document.getElementById("id_empresa_logradouro").value = jsonCep.tipo_logradouro + ' ' + jsonCep.logradouro;
//       document.getElementById("id_empresa_estado").value = jsonCep.uf;
//     }
//     else{
//       document.getElementById("id_empresa_bairro").value = '';
//       document.getElementById("id_empresa_cidade").value = '';
//       document.getElementById("id_empresa_logradouro").value = '';
//       document.getElementById("id_empresa_estado").value = '';
//     }
//   })
// });