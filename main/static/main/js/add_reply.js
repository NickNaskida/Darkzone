var addReplyButt = document.getElementById("add_reply_butt")
var addReplyForm = document.getElementById("add_reply_form")

// Post add form appear on button click

addReplyButt.addEventListener("click", function () {
        addReplyButt.style.display = "none";
        addReplyForm.style.display = "block";  
   	});