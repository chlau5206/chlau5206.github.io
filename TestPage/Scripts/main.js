// Main script --- 10:38 AM 7/22/2022
function checkCanvas() {
	
	if (document.createElement('canvas').getContext)
		isSupported = true;
	else
		isSupported = false;
	
	document.querySelector('.output').textContent
			= isSupported;
}

function subtraction(a,b){
	var c;
	c = a-b;
	return c;
}
var z = subtraction(10, 7);
// document.write("after subtraction, the different is " + z);
// alert("Welcome to Chlau 5206 - 10:43 AM 7/22/2022");

if (!document.createElement('canvas').getContext)
	alert("Browser does not support HTML5")
	
