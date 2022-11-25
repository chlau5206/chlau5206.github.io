function WriteCookie() {
    var now = new Date();
    now.setMonth( now.getMonth() + 1 );
    //cookievalue = escape(document.myform.customer.value) + ";"
    cookievalue = "Jimmy";
    
    document.cookie = "name=" + cookievalue;
    document.cookie = "browser" + navigator.userAgent
    document.cookie = "expires=" + now.toUTCString() + ";"
    document.write ("Setting Cookies : " + "name=" + cookievalue );
 }

 function ReadCookie() {
    var allcookies = document.cookie;
    document.write ("All Cookies : " + allcookies );
    
    // Get all the cookies pairs in an array
    cookiearray = allcookies.split(';');
    
    // Now take key value pair out of this array
    for(var i=0; i<cookiearray.length; i++) {
       name = cookiearray[i].split('=')[0];
       value = cookiearray[i].split('=')[1];
       document.write ("Key is : " + name + " and Value is : " + value);
    }
 }

 function getValue() {
   var retVal = prompt("Enter file name : ", "File name here");
   //document.write("You have entered : " + retVal);
   printJSON(retVal);
}

function printValues(obj) {
   for(var k in obj) {
       if(obj[k] instanceof Object) {
           printValues(obj[k]);
       } else {
           document.write(obj[k] + "<br>");
       };
   }
};

function printExchangeRates(){
   // var Json = '{"success":true,"timestamp":1669218303,"base":"EUR","date":"2022-11-23","rates":{"EUR":1,"USD":1.037716,"GBP":0.860173,"JPY":145.172309,"CNY":7.438137,"AUD":1.545881,"HKD":8.112929,"IDR":16194.38492,"MXN":20.088001,"SGD":1.431098,"KRW":1393.693444,"THB":37.420139,"TWD":32.294543}}';
   var fileName = "ExchangeRates.json";

   // Requiring fs module in which 
   // readFile function is defined.
   const fs = require('fs');
   
   // fs.readFile(fileName, (err, Json) => {
   //    if (err) throw err;
   // })

   var fr=new FileReader();
   fr.onload= fileName;
   
   function(){
       document.getElementById('output')
               .textContent=fr.result;
   }
     
   fr.readAsText(this.files[0]);

   var obj = JSON.parse(Json);
   var breakLine = "<br />";

   document.write("<hr>");

   //document.write(json + breakLine);
   // Printing a single value
   document.write("Time taken:" + obj["date"] + breakLine);  // Prints: J. K. Rowling
  
   for (country in obj["rates"]){
      document.write(symbol2country(country) + ': \u0009' + obj["rates"][country] + breakLine);   
   }

  
  
   // document.write(symbol2country('CNY') + ': \t' + obj["rates"]["CNY"] + breakLine);  // Prints: Harry Potter
   // document.write(symbol2country("USD") + ': \t' + obj["rates"]["USD"] + breakLine);  // Prints: $20.32

}

function symbol2country(symbol){
   var SC = '{"CAN":"CANADIAN DOLLAR","GBP": "BRITISH POUND","EUR": "EURO", "JPY": "JAPANESE YEN","CNY": "CHINESE YUAN","AUD": "AUSTRALIAN DOLLAR", "HKD": "HONG KONG DOLLAR","IDR": "INDONESIAN RUPIAH","MXN": "MEXICAN PESO","SGD": "SINGAPORE DOLLAR","KRW": "SOUTH KOREAN WON","THB": "THAI BAHT","TWD": "NEW TAIWAN DOLLAR","USD": "US DOLLAR"}'
   var oSC = JSON.parse(SC);

   return oSC[symbol];
}

function readTextFile(){
   
}

import {readFileSync, promises as fsPromises} from 'fs';
const {readFileSync, promises: fsPromises} = require('fs');
async function asyncReadFile(filename) {
   try {
     const contents = await fsPromises.readFile(filename, 'utf-8');
 
   //   const arr = contents.split(/\r?\n/);
 
   //   console.log(arr); // 👉️ ['One', 'Two', 'Three', 'Four']
 
     return arr;
   } catch (err) {
     console.log(err);
   }
 }
 