const spotifyAuthButton = document.querySelector('#spotify-auth-button')


const client_id =  '0ea9b00b04ac407bbb6cd462f139b996'
const spotify_authorize_endpoint = 'https://accounts.spotify.com/authorize'
const redirect_after_login = 'http://localhost:5000/auth'
// const scopes = ['playlist-read-private', 'user-read-private']

spotifyAuthButton.addEventListener('click', (evt) => {
        evt.preventDefault()
        window.open(`${spotify_authorize_endpoint}?client_id=${client_id}&redirect_uri=${redirect_after_login}&scope=playlist-read-private%20user-read-private&response_type=code&show_dialog=true`, '_self')
})