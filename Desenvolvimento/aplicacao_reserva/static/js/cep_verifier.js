async function consultar_cep(cep){
  cep = cep.replace('-', '')
  var url = 'http://cep.republicavirtual.com.br/web_cep.php?cep=' + cep + '&formato=jsonp';
  const res = await fetch(url);
  const promiseJson = await res.json();
  console.log(cep);
  if (promiseJson.resultado == '0')
    console.log('CEP NÃO ENCONTRADO');
  if (promiseJson.resultado == '1') {
    return promiseJson;
  }
}

var alterar_campos = function(tipo){
  let id = `id_${tipo}_cep`;
  var valor_cep = document.getElementById(id).value;
  let resultado = consultar_cep(valor_cep);
  resultado.then(jsonCep => {
    // console.log(jsonCep);
    if (jsonCep != undefined){
      document.getElementById(`id_${tipo}_bairro`).value = jsonCep.bairro;
      document.getElementById(`id_${tipo}_cidade`).value = jsonCep.cidade;
      document.getElementById(`id_${tipo}_logradouro`).value = jsonCep.tipo_logradouro + ' ' + jsonCep.logradouro;
      document.getElementById(`id_${tipo}_estado`).value = jsonCep.uf;

      document.getElementById(`id_${tipo}_bairro`).readOnly = true;
      document.getElementById(`id_${tipo}_cidade`).readOnly = true;
      document.getElementById(`id_${tipo}_logradouro`).readOnly = true;
      document.getElementById(`id_${tipo}_estado`).disabled = true;
    }
    else{
      document.getElementById(`id_${tipo}_bairro`).value = '';
      document.getElementById(`id_${tipo}_cidade`).value = '';
      document.getElementById(`id_${tipo}_logradouro`).value = '';
      document.getElementById(`id_${tipo}_estado`).value = '';

      document.getElementById(`id_${tipo}_bairro`).readOnly = false;
      document.getElementById(`id_${tipo}_cidade`).readOnly = false;
      document.getElementById(`id_${tipo}_logradouro`).readOnly = false;
      document.getElementById(`id_${tipo}_estado`).disabled = false;
    }
  })
}

const forms = ['pessoa', 'empresa', 'funcionario']


// CONFERE FORM PESSOA
try{
  var inputPessoaCep = document.querySelector("#id_pessoa_cep");
  inputPessoaCep.addEventListener("change", e => {alterar_campos('pessoa')});

  document.getElementById('enviar_form_pessoa').addEventListener('click',()=>{
    document.getElementById(`id_pessoa_estado`).disabled = false;
  });
} catch {
  console.log('Form pessoa não localizado')
}

// CONFERE FORM EMPRESA
try {
  var inputPessoaCep = document.querySelector("#id_empresa_cep");
  inputPessoaCep.addEventListener("change", e => {alterar_campos('empresa')});

  document.getElementById('enviar_form_empresa').addEventListener('click',()=>{
    document.getElementById(`id_empresa_estado`).disabled = false;
  });  
} catch {
  console.log('Form funcionário não localizado')
}

// CONFERE FORM FUNCIONARIO
try {
  var inputPessoaCep = document.querySelector("#id_funcionario_cep");
  inputPessoaCep.addEventListener("change", e => {alterar_campos('funcionario')});

  document.getElementById('enviar_form_funcionario').addEventListener('click',()=>{
    document.getElementById(`id_funcionario_estado`).disabled = false;
  });  
} catch {
  console.log('Form funcionário não localizado')
}


// CONFERE FORM ADMINISTRADOR
try {
  var inputPessoaCep = document.querySelector("#id_administrador_cep");
  inputPessoaCep.addEventListener("change", e => {alterar_campos('administrador')});

  document.getElementById('enviar_form_administrador').addEventListener('click',()=>{
    document.getElementById(`id_administrador_estado`).disabled = false;
  });
} catch {
  console.log('Form funcionário não localizado')
}




// var eventListeners = []


// function load() {
//   const forms = ['pessoa', 'empresa']
//   for (i in forms){
//     var inputCep = document.querySelector(`#id_${forms[i]}_cep`);
    
//     eventListeners.push(inputCep.addEventListener("change", e => {alterar_campos(forms[i]);}));
//     console.log(eventListeners)
//   }
// }

// window.onload = load();
