document.getElementById('search-input').addEventListener('keyup', (event) => {
    let query = event.target.value;
    let xhr = new XMLHttpRequest();
    xhr.open('GET', `/ajax/search/?q=${query}`, true);
    xhr.onload = function() {
        if (xhr.status === 200) {
            let data = JSON.parse(xhr.responseText);
            let resultList = document.getElementById('film-list');
            resultList.innerHTML = '';
            data.forEach(film => {
                let listItem = document.createElement('li');
                listItem.textContent = `${film.title} - ${film.director}`;
                resultList.appendChild(listItem);
            });
        }
    };
    xhr.send();
});