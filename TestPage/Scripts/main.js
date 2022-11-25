// Main script --- 10:38 AM 7/22/2022
function checkHTML5Support() {
	if (!document.createElement('canvas').getContext)
		alert("Browser does not support HTML5")
}
