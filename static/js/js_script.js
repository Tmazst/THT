


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

// Function to handle the intersection event
function handleIntersection(entries, observer) {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      console.log('Element has entered the viewport:', entry.target);
      entry.target.classList.add("rescaler");
      // You can add your logic here, for example:
      // entry.target.classList.add('visible'); // Modify the element's class
      // observer.unobserve(entry.target); // Stop observing if you only want to detect once
    }
  });
}

// Create an Intersection Observer instance
const observer = new IntersectionObserver(handleIntersection, {
  root: null, // Use the viewport as the root
  rootMargin: '0px', // No margin
  threshold: 0.8 // Trigger when 10% of the element is in the viewport
});

// Select the target element(s) you want to observe
const targetElements = document.querySelectorAll('.big-btns'); // Adjust the selector as needed

// Start observing each target element
targetElements.forEach(el => {
  observer.observe(el);
});

const targetFeatured = document.querySelectorAll('.job-cont-cont'); // Adjust the selector as needed

// Start observing each target element
targetFeatured.forEach(el => {
  observer.observe(el);
});



document.addEventListener('DOMContentLoaded', function() {
  const myDiv = document.querySelectorAll('.welcome-advert');
  const slides = document.querySelectorAll('.adv-cont');
  var toggleButton = document.querySelector('#close-button');
  let currentSlide = 2;

  // if (window.innerWidth =< 700){}
  // Show first slide immediately
  slides[currentSlide].classList.add('display');

  function nextSlide() {

      slides.forEach(slide => {
            slide.classList.remove("display");
      });
      
      // Move to next slide (loop if at end)
      currentSlide = (currentSlide + 1) % slides.length;
      slides[currentSlide].classList.add("display");
      
      // Fade in next slide after a delay
      setTimeout(nextSlide, 5000); // Match this delay to CSS transition time
  }

  nextSlide();

   // Event listener to close the div when clicking outside of it
   document.addEventListener('click', (event) => {
    if (!myDiv.contains(event.target) && event.target !== toggleButton) {
            myDiv.style.display = 'none';
        }
    });

  // Auto-advance every 5 seconds (adjust timing)
  // setInterval(nextSlide, 5000);
});

function closeAdverts(){
  document.querySelector(".welcome-advert").style.display = "none";
}


function openAuthWindow(){
    // Open Google OAuth in a new tab/window
    // if (window.innerWidth <= 768){
    sessionStorage.setItem('authPopup', 'true');
    const authUrl = '/login'; // Your Flask route for Google OAuth
    window.open(authUrl, 'authWindow', 'width=350,height=600');

    // Listen for messages from the authentication window
    window.addEventListener('message', (event) => {
      // Make sure to check origin in a production environment
      if (event.origin === 'https://jobs.techxolutions.com' && event.data === 'auth_complete') {
          alert('Authentication successful!');
          window.location.reload(); // Reload the parent window
      }
  }); 
      // }else{
      //   window.location.href = "/google_login?nopopup=true'";
      // }
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


