


////Fixed Sticky
//window.onscroll = function() {scrollFunction()};
//
//function scrollFunction() {
//  var scrollingElement = document.getElementById("nav-div");
//  // Distance from the top of the document to the top of the scrolling element
//  var elementOffset = scrollingElement.offsetTop;
//  // Viewport (window) top position
//  var windowTop = window.pageYOffset || document.documentElement.scrollTop;
//
//  if (windowTop > elementOffset) {
//    scrollingElement.style.position = "fixed";
//    scrollingElement.style.top = "0";
//  } else {
//    scrollingElement.style.position = "relative";
//  }
//}


function openAuthWindow() {
  // Open Google OAuth in a new tab/window
  const authUrl = '/login'; // Your Flask route for Google OAuth
  const authWindow = window.open(authUrl, 'authWindow', 'width=300,height=600');

 // Check if the window was blocked or opened in the same WebView
 if (!authWindow || authWindow.closed || typeof authWindow.closed === 'undefined') {
  // If the window was blocked or not opened externally, prompt the user to open the link manually
  const openExternally = confirm('Please open this link in an external browser: ' + authUrl);
  if (openExternally) {
      // Redirect the user to the URL (they can copy and paste it into an external browser)
      window.location.href = authUrl;
  }
} else {
  // Listen for messages from the authentication window
  window.addEventListener('message', (event) => {
      if (event.data === 'auth_complete') {
          alert('Authentication successful!');
          window.location.reload(); // Reload the parent window
      }
  });
}
}

var userName = document.querySelector("#navlink");
var trimmed  = userName.textContent.substring(0,7);
userName.textContent  = trimmed+"..";


function sideNavFunc(event){
  console.log("Side Nav");
  let sideNavBg = document.querySelector('#side-navig-bg');
  let sideNavCont = document.querySelector("#side-navig-cont");
  sideNavBg.classList.toggle("show-popup");
  sideNavCont.classList.toggle("show-menu");
  };

function closeSideNavFunc(){
  console.log("Side Nav1");
  let sideNavBg = document.querySelector('#side-navig-bg');
  let sideNavCont = document.querySelector("#side-navig-cont");

      sideNavBg.classList.remove("show-popup");
      sideNavCont.classList.remove("show-menu");

  };


var navParent = document.querySelectorAll(".saas-nav-item");
navParent.forEach(nav => {
    nav.addEventListener('click', function(){
        console.log("Nav item clicked");

        // First, hide all child elements
        navParent.forEach(item => {
            var childNav = document.querySelector("#nav-chld-" + item.id.split('-')[1]);
            if (childNav) {
                childNav.classList.remove('reveal');
            }
        });

        // Show the specific child nav for the clicked item
        if (nav.id === "nav-1"){
            var navOneChild = document.querySelector("#nav-chld-1");
            navOneChild.classList.toggle('reveal'); // Use toggle to show/hide
        }else if(nav.id === "nav-2"){
            var navOneChild = document.querySelector("#nav-chld-2");
            navOneChild.classList.toggle('reveal');
        }else if(nav.id === "nav-3"){
            var navOneChild = document.querySelector("#nav-chld-3");
            navOneChild.classList.toggle('reveal');
        }else if(nav.id === "nav-4"){
            var navOneChild = document.querySelector("#nav-chld-4");
            navOneChild.classList.toggle('reveal');
        }else if(nav.id === "nav-5"){
            var navOneChild = document.querySelector("#nav-chld-5");
            navOneChild.classList.toggle('reveal');
        }else if(nav.id === "nav-6"){
            var navOneChild = document.querySelector("#nav-chld-6");
            navOneChild.classList.toggle('reveal');
        }else if(nav.id === "nav-7"){
            var navOneChild = document.querySelector("#nav-chld-7");
            navOneChild.classList.toggle('reveal');
        }else if(nav.id === "nav-8"){
            var navOneChild = document.querySelector("#nav-chld-8");
            navOneChild.classList.toggle('reveal');
        }
    });
});

//Navigation Dropdown
const navSlide = () => {
  const burger = document.querySelector(".burger");
  const nav = document.querySelector(".nav-links");
  const navLinks = document.querySelectorAll(".nav-links a");

if( nav && burger && navLinks.length > 0){
  burger.addEventListener("click", () => {
    nav.classList.toggle("nav-active");

    navLinks.forEach((link, index) => {
      if (link.style.animation) {
        link.style.animation = "";
      } else {
        link.style.animation = `navLinkFade 0.5s ease forwards ${
          index / 7 + 0.5
        }s `;
      }
    });
    burger.classList.toggle("toggle");
  });
  //
};
}
navSlide();


function calculateDays() {
    var adJob = document.querySelectorAll("#deadline-div");
    var adDeadline = document.querySelectorAll("#deadline");
    var daysLeft = document.querySelectorAll("#days_left");


    var date = new Date();
    var today = date.getTime(); // Get today's date in milliseconds to compare with deadlines
    if( adJob.length > 1 ){
        for(var i = 0; i < adDeadline.length; i++) {
            // Get each ad's deadline
            var targetedAd = adDeadline[i];
            // Get the targeted ad's date tag and convert it to a Date object
            var deadline = new Date(targetedAd.innerText);
    //        console.log(deadline);

            // Calculate the days between today's date and the deadline
            var difference = Math.floor((deadline.getTime() - today) / (1000 * 60 * 60 * 24)); // Convert the time difference to days
    //        console.log("There are still plenty of time: ",difference);

            if (difference > 10) {
                adJob[i].classList.toggle("deadline-is-far");
                daysLeft[i].innerText = difference + " Days Left";
    //            console.log("There are still plenty of time");

            } else if (difference <= 10 && difference > 0) {
                adJob[i].classList.toggle("deadline-is-close");
                daysLeft[i].innerText = difference + " Days Left";
    //            console.log("We are getting closer to the deadline");

            } else if (difference <= 3 && difference >= 0) {
                adJob[i].classList.toggle("deadline-is-today");
                daysLeft[i].innerText = difference + " Days Left";
    //            console.log("Deadline is today");

            } else if (difference < 0) {
                adJob[i].classList.toggle("deadline-is-over");
                daysLeft[i].innerText = "Closed";
            }
        }
    };

}

calculateDays();




// Function to handle the scroll event
function handleScroll() {

//      console.log("Scroll Called1");
      // Get the navigation menu element
      const navigation = document.getElementById('nav-div-cont');

      // Store the last known scroll position
      let lastScrollTop = 0;

      // Get the height of the window
      const windowHeight = window.innerHeight;

      // Get the current scroll position
      const currentScroll = window.pageYOffset || document.documentElement.scrollTop;

      // Determine the scroll direction
      const scrollDirection = currentScroll > lastScrollTop ? 'down' : 'up';


       if (window.innerWidth <= 768){
          // If the user is scrolling down and the navigation is not already at the bottom
          if (scrollDirection === 'down' && (windowHeight + currentScroll) >= document.body.offsetHeight-4000) {
            console.log("Scroll Called",currentScroll,scrollDirection);
            navigation.style.position = 'fixed';
            navigation.style.bottom = '0';
          } else {
            navigation.style.position = 'static';
          }

          // Update the known scroll position
          lastScrollTop = currentScroll <= 0 ? 0 : currentScroll;

    }else{

      var scrollingElement = document.getElementById("nav-div");
      // Distance from the top of the document to the top of the scrolling element
      var elementOffset = scrollingElement.offsetTop;
      // Viewport (window) top position
      var windowTop = window.pageYOffset || document.documentElement.scrollTop;

      if (windowTop > elementOffset) {
        scrollingElement.style.position = "fixed";
        scrollingElement.style.top = "0";
      } else {
        scrollingElement.style.position = "relative";
      }


    }
}
window.onscroll = function() {handleScroll()};
// Add the scroll event listener
//window.addEventListener('scroll', handleScroll);




// Get references to the login button and the 2FA checkbox
let loginButton = document.getElementById("login_btn");
let twoFactorAuthCheckbox = document.getElementById("2fa_check_box");

// Event listener for the login button click
//loginButton.addEventListener('click', function() {
//    console.log("Login Submitted"); // Corrected typo: Changed 'log' to 'console'
//    if (twoFactorAuthCheckbox.checked) {
//        startOTPTimer();
//    }
//});
//
//// Event listener for the 2FA checkbox change
//twoFactorAuthCheckbox.addEventListener('change', function() {
//    console.log("2 Factor Checked"); // Corrected typo: Changed 'log' to 'console'
//    if (this.checked && loginButton.clicked) {
//        startOTPTimer();
//    }
//});



var blogContent = document.getElementsByClassName("text-limit");

for(var i=0; i<blogContent.length; i++){
    if (blogContent[i].textContent.length > 100) {

            blogContent[i].textContent = blogContent[i].textContent.substring(0,100) + "[...]";
        }
    }






//function checkDate(){
//
//    var applyBtn = document.querySelector(".jb-viewed-card-body a");
//    var appDeadline = document.querySelector("#deadline");
//
//    var date = new Date();
//    var today = date.getTime(); // Get today's date in milliseconds to compare with deadlines
//
//    var deadline = new Date(appDeadline.innerText);
//
//    console.log("Clicked!!",deadline.getTime());
//
//    // Calculate the days between today's date and the deadline
//    var differenceDate = (deadline.getTime() - today) / (1000 * 60 * 60 * 24);
//
//    if (differenceDate < 0) {
//            applyBtn.style.visibility="hidden";
//            console.log("Clicked!!",difference);
//    }
//}

//Dashboard
const navSideSlide = () => {
  const dashboardBtn = document.querySelector("#dashboard-btn");
  const nav = document.querySelector(".sidebar-main");
  const navLinks = document.querySelectorAll(".sidebar-main a");

if( dashboardBtn && nav && navLinks.length > 0){
  dashboardBtn.addEventListener("click", () => {
    nav.classList.toggle("nav-active-drw");

    navLinks.forEach((link, index) => {
      if (link.style.animation) {
        link.style.animation = "";
      } else {
        link.style.animation = `navLinkFade 0.5s ease forwards ${
          index / 7 + 0.5
        }s `;
      }
    });
    dashboardBtn.classList.toggle("toggle");
  });
  //
};
}
navSideSlide();


