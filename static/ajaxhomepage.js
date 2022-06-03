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


              