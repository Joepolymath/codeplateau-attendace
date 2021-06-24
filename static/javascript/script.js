
// const dateQuery = () => {
//     alert("HEre we are")
// }

document.getElementById("date").addEventListener('change', (e) => {
    e.preventDefault()
    // console.log("I am here")
    // window.location.replace("/views");

    function loadDoc() {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
          if (this.readyState == 4 && this.status == 200) {
            console.log("Hello here")
          }
        };
        xhttp.open("POST.html", "/views", true);
        xhttp.send();
      }
});

// alert("Hey")