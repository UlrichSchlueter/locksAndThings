var lockHttp = new XMLHttpRequest();
var unlockHttp = new XMLHttpRequest();

function logger(actionType,dataObj)
{
    var d = Date(Date.now()); 
    var table =document.getElementById("logger");
    var row = table.insertRow(-1);
    var cell1 = row.insertCell(0);
    cell1.innerHTML= d.toString() 
    var cell2 = row.insertCell(1);
    cell2.innerHTML=actionType
    var cell3 = row.insertCell(2);
    cell3.innerHTML=dataObj.sessionID
    var cell4= row.insertCell(3);
    cell4.innerHTML=dataObj.locked
    var cell5 = row.insertCell(4);
    cell5.innerHTML=dataObj.lockField
    var cell6 = row.insertCell(5);
    cell6.innerHTML=dataObj.error

   
   
}

function lockButton()
{     

    requestString='/lock/'+document.getElementById("LockField").value;
    lockHttp.open("GET", requestString, true);
    lockHttp.send();
      
    
    lockHttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
         var myObj = JSON.parse(this.responseText);
         document.getElementById("SessionField").value = myObj.sessionID;
         document.getElementById("IsLocked").value = myObj.locked;
         document.getElementById("LockField").value = myObj.lockField;

         logger ("lock", myObj);

        } };
    }
    function lockMultipleButton()
    {     
    
        requestString='/lockMultiple/'+document.getElementById("LockFieldMultiple").value;
        lockHttp.open("GET", requestString, true);
        lockHttp.send();
          

        lockHttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
             var myObj = JSON.parse(this.responseText);
             document.getElementById("SessionField").value = myObj.sessionID;
             document.getElementById("IsLockedMultiple").value = myObj.locked;
             document.getElementById("LockFieldMultiple").value = myObj.lockField;

             logger ("lockMultiple", myObj);
    
            
    
            } };
        }

function unlockButton()
{
   
    requestString='/unlock/'+document.getElementById("LockField").value+'?SessionID='+document.getElementById("SessionField").value;
    unlockHttp.open("GET", requestString, true);
    unlockHttp.send();
    
    unlockHttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
         var myObj = JSON.parse(this.responseText);
         document.getElementById("SessionField").value = myObj.sessionID;
         document.getElementById("IsLocked").value = myObj.locked;
         document.getElementById("LockField").value = myObj.lockField;
         logger ("unlock", myObj);
         
        } };
}


function unlockMultipleButton()
{
   
    requestString='/unlockMultiple/'+document.getElementById("LockFieldMultiple").value+'?SessionID='+document.getElementById("SessionField").value;
    unlockHttp.open("GET", requestString, true);
    unlockHttp.send();
    
    unlockHttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
         var myObj = JSON.parse(this.responseText);
         document.getElementById("SessionField").value = myObj.sessionID;
         document.getElementById("IsLockedMultiple").value = myObj.locked;
         document.getElementById("LockFieldMultiple").value = myObj.lockField;
         logger ("unlockMultiple", myObj);
        
        } };
}
