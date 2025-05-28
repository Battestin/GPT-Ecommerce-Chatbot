let chat = document.querySelector('#chat');
let input = document.querySelector('#input');
let botaoEnviar = document.querySelector('#botao-enviar');
let selectedImage;
let attachButton = document.querySelector('#more-file');
let imageThumbnail;

async function takeImage() {
    let fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = 'image/*';

    fileInput.onchange = async e => {
        if (imageThumbnail) {
            imageThumbnail.remove();
        }

        selectedImage = e.target.files[0];

        imageThumbnail = document.createElement('img');
        imageThumbnail.src = URL.createObjectURL(selectedImage);
        imageThumbnail.imageThumbnail.style.maxWidth = '3rem';
        imageThumbnail.imageThumbnail.style.maxHeight = '3rem';
        imageThumbnail.imageThumbnail.style.margin = '0.5rem';

        document.querySelector('.input__container').insertBefore(imageThumbnail, input);
        
        let formData = new FormData();
        formData.append('image', selectedImage);

        const response = await fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            body: formData
        });

        const resposta = await response.text();
        console.log(resposta);
        console.log(selectedImage);
    }
    fileInput.click();
}

async function enviarMensagem() {
    if(input.value == "" || input.value == null) return;
    let mensagem = input.value;
    input.value = "";


    if (imageThumbnail) {
        imageThumbnail.remove();
    }


    let novaBolha = criaBolhaUsuario();
    novaBolha.innerHTML = mensagem;
    chat.appendChild(novaBolha);

    let novaBolhaBot = criaBolhaBot();
    chat.appendChild(novaBolhaBot);
    vaiParaFinalDoChat();
    novaBolhaBot.innerHTML = "Analisando ..."
    
    // Envia requisição com a mensagem para a API do ChatBot
    const resposta = await fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: {
        "Content-Type": "application/json",
        },
        body: JSON.stringify({'msg':mensagem}),
    });
    const textoDaResposta = await resposta.text();
    console.log(textoDaResposta);
    novaBolhaBot.innerHTML = textoDaResposta.replace(/\n/g, '<br>');
    vaiParaFinalDoChat();
}

function criaBolhaUsuario() {
    let bolha = document.createElement('p');
    bolha.classList = 'chat__bolha chat__bolha--usuario';
    return bolha;
}

function criaBolhaBot() {
    let bolha = document.createElement('p');
    bolha.classList = 'chat__bolha chat__bolha--bot';
    return bolha;
}

function vaiParaFinalDoChat() {
    chat.scrollTop = chat.scrollHeight;
}

botaoEnviar.addEventListener('click', enviarMensagem);
input.addEventListener("keyup", function(event) {
    event.preventDefault();
    if (event.keyCode === 13) {
        botaoEnviar.click();
    }
});

attachButton.addEventListener('click', takeImage);