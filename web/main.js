function f1(link) {

    console.log('exec: f1')

    fetch(link).then(data => {
      console.log(data)
      //jsonresponse = JSON.parse(response);
    }).catch(error => {
      console.log(error)
    });
  
}

(function m(){console.log()})()

// (function main() {
//     console.log('entrou main')
//     let link1 = "https://raw.githubusercontent.com/jhoonb/folhams/master/web/situacao_por_mes.json"
//     f1(link1)
// })()
