const get_recommendation_form = document.querySelector('#genre-form')

get_recommendation_form.addEventListener('submit', (evt) => {
        evt.preventDefault()

        fetch('/homepage', {
                method: 'POST',
                body: JSON.stringify(document.getElementById('genre_selection').value),
                credentials: 'same-origin',
                headers: {
                        'Content-Type': 'application/json',
                      },
        })
        .then((response) => response.json())
        .then((responseJson) => {
                document.querySelector("#embed-iframe").insertAdjacentHTML('afterbegin', `<iframe style="border-radius:12px" src="https://open.spotify.com/embed/track/${responseJson}" width="100%" height="380" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>`)
                console.log(responseJson)
        })
        })




// When the user scrolls the page, execute myFunction
window.onscroll = function() {myFunction()};

// Get the navbar
var navbar = document.getElementById("navbar");

// Get the offset position of the navbar
var sticky = navbar.offsetTop;

// Add the sticky class to the navbar when you reach its scroll position. Remove "sticky" when you leave the scroll position
function myFunction() {
  if (window.pageYOffset >= sticky) {
    navbar.classList.add("sticky")
  } else {
    navbar.classList.remove("sticky");
  }
} 
              