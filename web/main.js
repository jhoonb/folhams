var myHeading = document.querySelector("h1");

var json = require('./resultados/maiores_salarios.json'); //(with path)

if(myHeading) {
    myHeading.textContent = 'opa'
    console.log(json)
}
else {
    alert("erro")
}