import { csrftoken } from "./csrf_token.js";

const articles = document.querySelectorAll('.articles');
            
articles.forEach(article => {
    const likeButton = article.querySelector(".like-button");
    const likeCount = article.querySelector('.like-count');
    
    likeButton.addEventListener("click", () => {
        const articleId = article.getAttribute("data-article-id");
        let like_icon = article.querySelector('.liked');

        likePost(articleId, likeCount, like_icon);
    });
});


function likePost(articleId, likeCount, like_icon) {
    var url = window.location.href;
    var index = url.indexOf("home/");
    url = url.slice(0, index+5)  + "like/" + articleId + "/";

    fetch(url, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrftoken,
            "Content-Type": "application/json",
        },
    })
    .then((response) => response.json())
    .then((data) => {
        likeCount.textContent = data["likes"].toString();
        
        if(data['checked'] == 1){
            like_icon.classList.remove('fa-regular');
            like_icon.classList.add('fa-solid');
        } else if(data['checked'] == 0){
            like_icon.classList.remove('fa-solid');
            like_icon.classList.add('fa-regular');
        }
    })
}

