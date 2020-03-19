let btn = document.querySelector("button");
let formulaire = document.querySelector("form");
let input = document.querySelector("input");
let darkBtn = document.querySelector('.btn-dark-mode');

//Responsive Mode
function resetHeight(){
    document.querySelector('#site').style.height=window.innerHeight +"px";
}
window.addEventListener("resize", resetHeight);
resetHeight()

//DarkMode Event
function darkMode(){
    document.body.className='dark';
    darkBtn.textContent='Normal Mode';
    localStorage.setItem('theme','sombre');
}
if (localStorage.getItem('theme')){
    if(localStorage.getItem('theme')=='sombre'){
        darkMode();
    }
}
//Dark Mode Event
darkBtn.addEventListener('click', ()=>{
    if(document.body.classList.contains('dark')){
        document.body.classList.remove('dark');
        darkBtn.textContent = 'Dark mode';
        localStorage.setItem('theme','clair');
    }else{
        darkMode();
    }
});

//Stops the program for a certain time
function wait(ms) {
    var d = new Date();
    var d2 = null;
    do { d2 = new Date(); }
    while(d2-d < ms);
}

//Returns a random element from an array
function randomChoice(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function initMap(response){
    var myLatLng = response.position.coordinates;

        var map = new google.maps.Map(document.querySelector('.blocPapy:last-child .messagePapy .maps'), {
          zoom: 16,
          center: myLatLng
        });

        var marker = new google.maps.Marker({
          position: myLatLng,
          map: map,
          title: `${response.position.town}`
        });


}

//Allows you to format and display the text sent by the user.
function bubbleUser(textUser){
    let blocUser = document.createElement("div");
    let messageUser = document.createElement("div");
    let imageUser = document.createElement('div');
    imageUser.innerHTML="<img src= '../static/images/big_vaultboyset_26.png' width=50px height=50px>";
    messageUser.textContent= textUser;
    blocUser.className='blocUser';
    messageUser.className='messageUser';
    document.querySelector(".messageArea").append(blocUser);
    blocUser.prepend(messageUser);
    blocUser.append(imageUser);

}


//Function returns several possible responses depending on user input
function papyAnswer(response, balise) {

    let answers = [`Ahhhh <strong>${response.position.town}</strong>, quel endroit magnifique. En y réfléchissant j'ai une
    petite anecdote à te raconter sur <strong>${response.position.town}</strong>. Est-ce que je t'ai déjà parlé de ça: 
    <strong>${response.papybot_answer.title}</strong>? Non?<br>
    <ul>
         ${response.papybot_answer.extract}
    
    </ul>
   
    Ca te plaît? Alors mets un pouce bleu, non je rigole t'es pas sur Youtube.<br>
    Retrouve directement cet article sur  <a href="${response.papybot_answer.wiki_url}">Wikipedia.com</a>`,
    `J'aime vraiment la ville de <strong>${response.position.town}</strong>. Et si je te
     racontais une histoire sur : <strong>${response.papybot_answer.title}</strong><br>
    ${response.papybot_answer.extract}
    <br>Tu peux retrouver la suite de cette histoire en allant sur le lien suivant : 
   <a href="${response.papybot_answer.wiki_url}" target="_blank">Wikipedia.com</a><br>`];

    balise.innerHTML = randomChoice(answers);

}

function errorAnswer(response, balise) {

    balise.innerHTML  = `Oula gamin(e), tu vas bien trop vite pour mon vieil âge. Je n'ai malheuresement pas compris ce que
     tu m'as demandé. <br>
    Tu sais je me fais sourd et c'est difficile pour moi de comprendre les jeunes de ton âge. <br>
    Pour bien que je te comprenne écris ta demande sous cette forme : <br>
    <ul>
        <li>Donne moi l'adresse de {ton lieu}</li>
        <li>Dis moi où se situe {ton lieu}</li>
        <li>Je veux aller à {ton lieu}</li>
        <li>Je veux partir à {ton lieu}</li>
        <li>Ou est {ton lieu}</li>
        <li>{ton lieu}</li>
    </ul>
    A toi gamin(e)!`;


}

// Create a specific bubble with Wikipedia image and link to Wikipedia article
function bubbleLink(response) {
    let blocPapy = document.createElement("div");
    let imagePapy = document.createElement("div");
    let messagePapy = document.createElement("div");
    imagePapy.innerHTML="<img src= '../static/images/big_hot_grandpa_2.png' width=50px height=50px>";
    messagePapy.innerHTML =`<a href="${response.papybot_answer.wiki_url}" target="_blank">
      <div class="imageWiki">
      <img src="${response.papybot_answer.image}" alt="">
      </div>
      <div class="banniere">
     Retrouve cet article sur Wikipedia!<br>
     <span>wikipedia.fr</span>
      </div>
    </a>`;
    blocPapy.className='blocPapy';
    messagePapy.className='messagePapy link';
    document.querySelector(".messageArea").append(blocPapy);
    blocPapy.prepend(messagePapy);
    blocPapy.prepend(imagePapy);

}
function bubbleMaps(response) {

    let blocPapy = document.createElement("div");
    let imagePapy = document.createElement("div");
    let messagePapy = document.createElement("div");
    imagePapy.innerHTML="<img src= '../static/images/big_hot_grandpa_2.png' width=50px height=50px>";
    messagePapy.innerHTML = "<div class='maps'></div>"
    blocPapy.className='blocPapy';
    messagePapy.className='messagePapy';
    document.querySelector(".messageArea").append(blocPapy);
    blocPapy.prepend(messagePapy);
    blocPapy.prepend(imagePapy);



}

//Function that creates the tags necessary for loading animation
function loadingAnswer(balise){
    balise.innerHTML = `<div class="loader">
                            <div class="duo duo1">
                                <div class="dot dot-a"></div>
                                <div class="dot dot-b "></div>
                            </div>
                            <div class="duo duo2">
                                <div class="dot dot-a"></div>
                                <div class="dot dot-b"></div>
                            </div>
                        </div>`;

}



//Create the robot bubble and integrate it into the DOM. Here the bubble contains the loading animation
function bubblePapyBotLoading(){
    let blocPapy = document.createElement("div");
    let imagePapy = document.createElement("div");
    let messagePapy = document.createElement("div");
    imagePapy.innerHTML="<img src= '../static/images/big_hot_grandpa_2.png' width=50px height=50px>";
    loadingAnswer(messagePapy);
    blocPapy.className='blocPapy';
    messagePapy.className='loading messagePapy';
    document.querySelector(".messageArea").append(blocPapy);
    blocPapy.prepend(messagePapy);
    blocPapy.prepend(imagePapy);

}

//Change the text of the robot bubble and integrate the text generated following the analysis of user input
function bubblePapyBot(response) {
    messagePapy = document.querySelector('.blocPapy:last-child .messagePapy');
    messagePapy.classList.remove('loading');
    if (response.papybot_answer.extract){
        papyAnswer(response,messagePapy);
    }else{
        errorAnswer(response, messagePapy);
    };

    console.log(response);
    if(response.position.coordinates){
       bubbleMaps(response);

    }

}

//Function which sends the data to the server for analysis and retrieves the response in json format
function postData(url, data){
    return fetch(url,{
        method:"POST",
        body: data
    })
    .then(response => response.json())
    .catch(error =>console.log(error));
}


//Form submission event. The default behavior is canceled. the user's text is processed
//and integrated into the DOM, a response from the robot is integrated into the DOM.
formulaire.addEventListener('submit',(e)=>{
    e.preventDefault();
    let textUser =  input.value;
    bubbleUser(textUser);
    document.querySelector(`.blocUser:last-child`).scrollIntoView();
    bubblePapyBotLoading();
    document.querySelector(`.blocPapy:last-child`).scrollIntoView();
     postData('/ajax', new FormData(formulaire))
    .then(response =>{
        if (response.papybot_answer.extract){
            wait(1500);
            bubblePapyBot(response);
            initMap(response);
            document.querySelector(`.blocPapy:last-child`).scrollIntoView();
        }else{
            wait(1500);
            bubblePapyBot(response);
            document.querySelector(`.blocPapy:last-child`).scrollIntoView();
        }
    });
     input.value="";
});

//Event that displays the send button when the user types on the keyboard
input.addEventListener('keyup',() =>{

    if (input.value != ""){
        btn.style.display = 'block';
        input.style.width='90%'
    }else{
        btn.style.display ='none';
        input.style.width='100%'
    }

});



