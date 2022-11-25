function printExchangeRates(){
	var Json = '{"success":true,"timestamp":1669218303,"base":"EUR","date":"2022-11-23","rates":{"EUR":1,"USD":1.037716,"GBP":0.860173,"JPY":145.172309,"CNY":7.438137,"AUD":1.545881,"HKD":8.112929,"IDR":16194.38492,"MXN":20.088001,"SGD":1.431098,"KRW":1393.693444,"THB":37.420139,"TWD":32.294543}}';
	var obj = JSON.parse(Json);
	var breakLine = "<br />";
	
	document.write("<hr>");
	
	//document.write(json + breakLine);
	// Printing a single value
	document.write("Time taken:" + obj["date"] + breakLine);  // Prints: J. K. Rowling
	
	for (country in obj["rates"]){
		document.write(symbol2country(country) + ':     ' + obj["rates"][country] + breakLine);   
	}
	
	// document.write(symbol2country('CNY') + ': \t' + obj["rates"]["CNY"] + breakLine); // single rate
}
	
function symbol2country(symbol){
	var SC = '{"CAN":"CANADIAN DOLLAR","GBP": "BRITISH POUND","EUR": "EURO", "JPY": "JAPANESE YEN","CNY": "CHINESE YUAN","AUD": "AUSTRALIAN DOLLAR", "HKD": "HONG KONG DOLLAR","IDR": "INDONESIAN RUPIAH","MXN": "MEXICAN PESO","SGD": "SINGAPORE DOLLAR","KRW": "SOUTH KOREAN WON","THB": "THAI BAHT","TWD": "NEW TAIWAN DOLLAR","USD": "US DOLLAR"}'
	var oSC = JSON.parse(SC);
	
	return oSC[symbol];
}