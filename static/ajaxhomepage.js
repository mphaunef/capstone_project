const get_recommendation_form = document.querySelector('#genre-form')

get_recommendation_form.addEventListener('submit', (evt) => {
        evt.preventDefault()

        fetch('/homepage', {
                method: 'POST',
                // body: JSON.stringify(???),
                credentials: 'same-origin',
                headers: {
                        'Content-Type': 'application/json',
                      },
        })
        .then((reponse) => Response.json())
        .then((responseJson) => {
                console.log(responseJson)
        })
        })