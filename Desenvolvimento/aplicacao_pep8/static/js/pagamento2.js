// Step #3
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
// alert(csrftoken)
const cardForm = mp.cardForm({
    amount: "100.5",  // valor da compra
    autoMount: true,
    form: {
      id: "form-checkout",
      cardholderName: {
        id: "id_nome_cartao",
        placeholder: "Titular do cartão",
      },
      cardholderEmail: {
        id: "id_email",
        placeholder: "E-mail",
      },
      cardNumber: {
        id: "id_numero_cartao",
        placeholder: "Número do cartão",
      },
      cardExpirationMonth: {
        id: "id_mes_vencimento",
        placeholder: "Mês de vencimento",
      },
      cardExpirationYear: {
        id: "id_ano_vencimento",
        placeholder: "Ano de vencimento",
      },
      securityCode: {
        id: "id_codigo_seguranca",
        placeholder: "Código de segurança",
      },
      installments: {
        id: "id_parcelas",
        placeholder: "Parcelas",
      },
      identificationType: {
        id: "id_tipo_documento",
        placeholder: "Tipo de documento",
      },
      identificationNumber: {
        id: "id_numero_documento",
        placeholder: "Número do documento",
      },
      issuer: {
        id: "id_banco",
        placeholder: "Banco emissor",
      },
    },
    callbacks: {
      onFormMounted: error => {
        if (error) return console.warn("Form Mounted handling error: ", error);
        console.log("Form mounted");
      },
      onSubmit: async function (event) {
        event.preventDefault();
        
        const {
          paymentMethodId: payment_method_id,
          issuerId: issuer_id,
          cardholderEmail: email,
          amount,
          token,
          installments,
          identificationNumber,
          identificationType,
        } = cardForm.getCardFormData();
  
        const res = await fetch("/api/pagamento?format=json", {
          method: "POST",
          headers: {
            'X-CSRFToken': csrftoken,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            token,
            issuer_id,
            payment_method_id,
            transaction_amount: Number(amount),
            installments: Number(installments),
            description: "Descrição do produto",
            payer: {
              email,
              identification: {
                type: identificationType,
                number: identificationNumber,
              },
            },
            id_reserva: document.getElementById(`id_reserva`).value,
          }),
        });
        // alert(res.data)
        console.log(res);
        const json = await res.json();
        let mensagem_de_erro = json.mensagem_de_erro;
        console.log(mensagem_de_erro);
        document.getElementById(`mensagem_de_erro`).value = mensagem_de_erro;
        // res.then(json => {
        //   // console.log(jsonCep);
        //   console.log('ENTROU');
        //   if (json != undefined) {
        //     document.getElementById(`mensagem_de_erro`).value = json.mensagem_de_erro;
        //     console.log('ENTROU2');
        //     console.log(json.mensagem_de_erro);
        //   }
        // });
        if (mensagem_de_erro == 'none' || mensagem_de_erro == '')
        document.forms['form-checkout'].submit();
        else{
          let element = document.getElementById(`mensagem_de_erro`);
          let mensagem = element.value;
          let caixa_alerta_erro = document.getElementById(`alerta_de_erro`);
          caixa_alerta_erro.style.display = 'block';          // Show
          caixa_alerta_erro.textContent = mensagem;
              
          /* if (mensagem != "" || mensagem != "none"){
              let caixa_alerta_erro = document.getElementById(`alerta_de_erro`);
              caixa_alerta_erro.style.display = 'block';          // Show
          }
          else
          caixa_alerta_erro.style.display = 'none'; */
        }
        // cardForm.submit();
        },
        onFetching: (resource) => {
        console.log("Fetching resource: ", resource);
  
        // Animate progress bar
        const progressBar = document.querySelector(".progress-bar");
        progressBar.removeAttribute("value");
  
        return () => {
          progressBar.setAttribute("value", "0");
        };
      },
    },
  });