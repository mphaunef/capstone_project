const genre_buttons = document.querySelectorAll('#genre-buttons');

let last_click = 0;

for (const button of genre_buttons){
    button.addEventListener('click', (evt) => {
        const id = evt.target.value
        if (document.getElementById(id).classList.contains('hidden')){
            document.getElementById(id).classList.remove('hidden');
    }   else {
        document.getElementById(id).classList.add('hidden');
    }

        if (last_click !== 0 && last_click !== id){ 
            document.getElementById(last_click).classList.add('hidden')
        }
        last_click = id
    })};


