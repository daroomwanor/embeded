var index = 1;
var poll = "false";
var time = 1;
var display = 1;

function showTime(){
	var date = new Date();
	var h = date.getHours(); // 0 - 23
	var m = date.getMinutes(); // 0 - 59
	var s = date.getSeconds(); // 0 - 59
	var session = "AM";
	
	if(h == 0){
		h = 12;
	}

	if(h == 12){
		session = "PM";
	}
	
	if(h > 12){
		h = h - 12;
		session = "PM";
	}
	
	h = (h < 10) ? "0" + h : h;
	m = (m < 10) ? "0" + m : m;
	s = (s < 10) ? "0" + s : s;
	
	var time = h + ":" + m + ":" + s + " " + session;
	document.getElementById("MyClockDisplay").innerText = time;
	document.getElementById("MyClockDisplay").textContent = time;
	
	setTimeout(showTime, 1000);			
}
setInterval(next, 20000);
function next(){
	if(poll == "false"){
		setSlides();
	}else{
		if(time >= display){
			poll = "false";
			time=1;
		}else{
			time = time+1;
		}
	}
}

function setSlides() {
	var slides = document.getElementsByClassName("slide");
	for(var x = 0; x<slides.length; x++){
		slides[x].style.display = "None";
	}
	let screen_width = screen.width-(screen.width/3.5);
	let screen_height = screen.height-20;
	let margin_left = (screen.width/3.5)+5; 
	try{
		document.getElementById(index).style.display = "Block";
		document.getElementById(index).style.width = screen_width+"px";
		document.getElementById(index).style.height = screen_height+"px";
		document.getElementById(index).style.margin = "-2px 0px 0px "+margin_left+"px";
		poll = document.getElementById(index).getAttribute("data-record");
		display = document.getElementById(index).getAttribute("display");
	}finally{
		if (index == slides.length){
			index = 1;
		}else{
			index = index+1;
		}
	}
}



function mobileDisplay(){
	document.getElementById("qrCode").style.display = "None";
	let screen_height = screen.height/3.5;
	let screen_width  = screen.width/3.5;
	var displayTime = 10000;
	const xhttp = new XMLHttpRequest();
	xhttp.onload = function() {
		 if (this.readyState == 4 && this.status == 200) {
			 document.getElementById("qrCode").innerHTML = this.responseText;
			 document.getElementById("1_displayImg").style.width = screen_width+"px";
			 document.getElementById("1_displayImg").style.height = 75+screen_height+"px";
			 document.getElementById("2_displayImg").style.width = screen_width+"px";
			 document.getElementById("2_displayImg").style.height = screen_height+"px";
			 document.getElementById("qrCode").style.display = "Block";
			 displayTime = document.getElementById("displayTime").value;
			 setTimeout(mobileDisplay, displayTime);	 
		 }
	}
	xhttp.open("GET", "/mobileDisplayAd");
	xhttp.send();	
}