let btn = document.querySelector("button");
let formulaire = document.querySelector("form");
let input = document.querySelector("input");
let darkBtn = document.querySelector('.btn-dark-mode');



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
   
    Ca te plaît? Alors mets un pouce bleu, non je rigole t'es pas sur Youtube.<br>`,
    `J'aime vraiment la ville de <strong>${response.position.town}</strong>. Et si je te
     racontais une histoire sur : <strong>${response.papybot_answer.title}</strong><br>
    ${response.papybot_answer.extract}
    Tu peux retrouver la suite de cette histoire en allant sur le lien de la bulle du dessous.<br>`];

    balise.innerHTML = randomChoice(answers);

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
    papyAnswer(response,messagePapy);
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
        bubblePapyBot(response);
        initMap(response);
        document.querySelector(`.blocPapy:last-child`).scrollIntoView();
        wait(1500);

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



