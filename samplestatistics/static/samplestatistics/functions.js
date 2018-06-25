


// This stops the Enter Key from working

function submitOnEnter(evt) { 
  var evt = (evt) ? evt : ((event) ? event : null); 
  var node = (evt.target) ? evt.target : ((evt.srcElement) ? evt.srcElement : null); 
  if ((evt.keyCode == 13))  { testResults(); return false; } 
} 

document.onkeypress = submitOnEnter; 




// OLD toggle functions
/* Keep these for now */
/* Remove all traces later */
function toggleFormula() {}


function toggleSolution() {}


function toggleR() { }


function toggleExcel() { }




// NEW toggle functions
/* Hide these for now */

$(document).ready(function(){
$("#showFormula").click( function(){
  $("#showFormula").toggle("slow");
  $("#hideFormula").toggle("slow");
  } );
} );

$(document).ready(function(){
$("#hideFormula").click( function(){
  $("#showFormula").toggle("slow");
  $("#hideFormula").toggle("slow");
  } );
} );


$(document).ready(function(){
$("#showSolution").click( function(){
  $("#showSolution").toggle("slow");
  $("#hideSolution").toggle("slow");
  } );
} );

$(document).ready(function(){
$("#hideSolution").click( function(){
  $("#showSolution").toggle("slow");
  $("#hideSolution").toggle("slow");
  } );
} );


$(document).ready(function(){
$("#showR").click( function(){
  $("#showR").toggle("slow");
  $("#hideR").toggle("slow");
  } );
} );

$(document).ready(function(){
$("#hideR").click( function(){
  $("#showR").toggle("slow");
  $("#hideR").toggle("slow");
  } );
} );


$(document).ready(function(){
$("#showExcel").click( function(){
  $("#showExcel").toggle("slow");
  $("#hideExcel").toggle("slow");
  } );
} );

$(document).ready(function(){
$("#hideExcel").click( function(){
  $("#showExcel").toggle("slow");
  $("#hideExcel").toggle("slow");
  } );
} );


$(document).ready(function(){
$("#showSAS").click( function(){
  $("#showSAS").toggle("slow");
  $("#hideSAS").toggle("slow");
  } );
} );

$(document).ready(function(){
$("#hideSAS").click( function(){
  $("#showSAS").toggle("slow");
  $("#hideSAS").toggle("slow");
  } );
} );


/* */ 




