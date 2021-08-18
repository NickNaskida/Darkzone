var newPostButt = document.getElementById("new_post_butt")
var addPostForm = document.getElementById("add_post_form")

// Post add form appear on button click

newPostButt.addEventListener("click", function () {
        newPostButt.style.display = "none";
        addPostForm.style.display = "block";  
   	});