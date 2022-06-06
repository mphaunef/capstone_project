var go_button_clicked = false;

const get_recommendation_form = document.querySelector('#genre-form')

get_recommendation_form.addEventListener('submit', (evt) => {
        evt.preventDefault()
        
        fetch('/home', {
                method: 'POST',
                body: JSON.stringify(document.getElementById('genre_selection').value),
                credentials: 'same-origin',
                headers: {
                        'Content-Type': 'application/json',
                      },
        })
        .then((response) => response.json())
        .then((responseJson) => {
                document.querySelector("#embed-iframe").insertAdjacentHTML('afterbegin', `<button class="favorite-button" value="${responseJson}">Favorite <i class="fa fa-heart"></i> </button> <iframe style="border-radius:12px" src="https://open.spotify.com/embed/track/${responseJson}" width="100%" height="380" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>`)
                console.log(responseJson)
                go_button_clicked = true
        if (go_button_clicked === true) {
        
        const favorite_buttons = document.querySelectorAll('.favorite-button')
        console.log(favorite_buttons)
        for (const favorite_button of favorite_buttons){

                favorite_button.addEventListener('click', (evt) =>{
                        console.log('i have been clicked')
                        const id = evt.target.value
                        if(confirm('Are you sure you want to add to favorites?'))
                        fetch(`/${id}/favorites`) 
                        .then((response) => response.json())
                        .then((favoriteResponse) =>{
                                console.log('successful like')
                        })
                        
})}
}})
        
})



              