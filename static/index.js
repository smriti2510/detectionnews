var a = false;

$("#button").click(function(event){
//$('#display').html(data);
  var news =  document.getElementById("TEXT").value;
  console.log(news.length, news);
  if (a){
       $.get( "./predict",
          { news },
          function(data) {
             document.getElementById('display').innerText=data;
          }
       );}
       else{
         document.getElementById('display').innerText="Please Regiter";
       }
    });
$("#regBut").click(function(event){
    console.log("clicked")
       $.get( 
          "./register",
          { "name": document.getElementById("name").value,
          "age": document.getElementById("age").value,
          "gender": document.querySelector('input[name=gender]:checked').value,
          "username": document.getElementById("Username").value,
          "password": document.getElementById("Password").value,
          "email": document.getElementById("email").value,
         },
          function(data) {
             if(data[0] == 'R'){
                a=true;
             }
             console.log(data);
          }
       );
    });

$("#signBut").click(function(event){
   var u = document.getElementById("username").value
   console.log("clicked",u)
   
         $.get( 
            "./signup",
            { 
            "username":u ,
            "password": document.getElementById("password").value,
            
           },
            function(data) {
               if(data[0] == 'S'){
                  a= true;
                  
               }
               document.getElementById("output").innerText  = data;
               console.log(data);
            }
         );
      });

      function openRegister(){
         document.getElementById("PredBox").style.display = "none";
         document.getElementById("SignBox").style.display = "none";
         document.getElementById("RegBox").style.display = "inline-block";
      }

      function openSignup(){
         document.getElementById("PredBox").style.display = "none";
         document.getElementById("SignBox").style.display = "inline-block";
         document.getElementById("RegBox").style.display = "none";
      }

      function openPrediction(){
         document.getElementById("PredBox").style.display = "inline-block";
         document.getElementById("SignBox").style.display = "none";
         document.getElementById("RegBox").style.display = "none";
      }