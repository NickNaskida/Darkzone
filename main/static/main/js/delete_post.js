var deleteButt = document.getElementById("delete_post_butt")
var cancelButt = document.getElementById("cancel_post_delete_butt")
var deleteForm = document.getElementById("delete_post_form")

deleteButt.addEventListener("click", function () {
        deleteButt.style.display = "none";
        cancelButt.style.display = "block";
        deleteForm.style.display = "flex";  
   	});


cancelButt.addEventListener("click", function () {
        deleteButt.style.display = "block";
        cancelButt.style.display = "none";
        deleteForm.style.display = "none";   
   	});