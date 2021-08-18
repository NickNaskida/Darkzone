
var scrollToTopBtn = document.getElementById("goup")
var rootElement = document.documentElement

// Scroll to top button logic

window.onscroll = function() {scrollFunction()};
function scrollFunction() {
  	if (document.body.scrollTop > 70 || document.documentElement.scrollTop > 70) {
    	scrollToTopBtn.style.display = "flex";
  	} else {
    	scrollToTopBtn.style.display = "none";
  	}
}

function scrollToTop() {
  	rootElement.scrollTo({
    	top: 0,
    	behavior: "smooth"
  	})
}
scrollToTopBtn.addEventListener("click", scrollToTop)


// Profile upload form

$("#upload_butt").on( "click", function() {
  	$("#upload_form").toggle()
});


// Side nav appear

var burger = document.getElementById("burger")
var mobileNav = document.getElementById("mobile_nav")
var closeMobileNav = document.getElementById("close-mobile-nav")

function ShowMobileNav() {
    mobileNav.style.width = "280px";
}

function HideMobileNav() {
    mobileNav.style.width = "0px";
}

burger.addEventListener("click", ShowMobileNav)
closeMobileNav.addEventListener("click", HideMobileNav)

