let btn = document.querySelector("button");
let formulaire = document.querySelector("form");
let input = document.querySelector("input");
let darkBtn = document.querySelector('.btn-dark-mode');


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

    let answers = [`Ahhhh ${response.position.town}, quel endroit magnifique. En y réfléchissant j'ai une
    petite anecdote à te raconter sur ${response.position.town}. Est ce que je t'ai déjà parlé de
    ${response.papybot_answer.title}?<br>
    Alors voilà :<br>
    ${response.papybot_answer.extract}<br>
    Ca te plaît? Alors mets un pouce bleu, non je rigole t'es pas sur Youtube.<br>
    Retrouve cet article sur ce joli petit lien =>
    <a href="${response.papybot_answer.wiki_url}" target="_blank">Petit lien</a> qui ne contient aucun virus`,
    `J'aime vraiment beaucoup la ville de ${response.position.town} en ${response.position.department}.<br> Et si je te
     racontais l'histoire sur : ${response.papybot_answer.title}<br>
    ${response.papybot_answer.extract}
    Tu peux retrouver la suite de cette histoire en allant sur le lien de la bulle du dessous.`]

    balise.innerHTML = randomChoice(answers)

}

//Function that creates the tags necessary for loading animation
function loadingAnswer(balise){
   balise.innerHTML = "<div class=\"loader\">\n" +
        "  <div class=\"duo duo1\">\n" +
        "    <div class=\"dot dot-a\"></div>\n" +
        "    <div class=\"dot dot-b\"></div>\n" +
        "  </div>\n" +
        "  <div class=\"duo duo2\">\n" +
        "    <div class=\"dot dot-a\"></div>\n" +
        "    <div class=\"dot dot-b\"></div>\n" +
        "  </div>\n" +
        "</div>";
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
        wait(2000);
        document.querySelector(`.blocPapy:last-child`).scrollIntoView();
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

