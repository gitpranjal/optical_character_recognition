
var div = document.querySelector('#div'), x1 = 0, y1 = 0, x2 = 0, y2 = 0;

div.style.border = "5px solid lime"
div.style.position ="absolute"

// var pdf_div = document.querySelector("#pdf")
// pdf_div.appendChild(div)
function reCalc() { //This will restyle the div
    var x3 = Math.min(x1,x2); //Smaller X
    var x4 = Math.max(x1,x2); //Larger X
    var y3 = Math.min(y1,y2); //Smaller Y
    var y4 = Math.max(y1,y2); //Larger Y
    div.style.left = x3 + 'px';
    div.style.top = y3 + 'px';
    div.style.width = x4 - x3 + 'px';
    div.style.height = y4 - y3 + 'px';
}
onmousedown = function(e) {
    div.hidden = 0; //Unhide the div
    x1 = e.clientX; //Set the initial X
    y1 = e.clientY; //Set the initial Y
    reCalc();
};
onmousemove = function(e) {
    x2 = e.clientX; //Update the current position X
    y2 = e.clientY; //Update the current position Y
    reCalc();
};
onmouseup = function(e) {
    
    var box_information={
    	"startx": div.style.left,
    	"starty": div.style.top,
    	"width" : div.style.width,
    	"height": div.style.height
    }
    var information_label = prompt("What kind of information is contained in the box?");
    box_information["information_label"] = information_label;
//    console.log(box_information)
    send_information(box_information)
    
    div.hidden = 1; //Hide the div
};

function send_information(data)
{
  fetch('/', {
  method: 'POST', // or 'PUT'
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(data),
})
.then((response) => response.json())
.then((data) => {
  console.log('Success:', data);
})
.catch((error) => {
  console.error('Error:', error);
});
}
