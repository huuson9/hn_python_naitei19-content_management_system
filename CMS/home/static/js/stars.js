// script.js

const stars = document.querySelectorAll('.star');

stars.forEach(star => {
    star.addEventListener('click', () => {
        const rating = parseInt(star.getAttribute('data-rating'));
        const articleId = star.getAttribute('data-article-id');
        
        rate(rating, articleId);
    });
});


function rate(rating, post_id) {
    const substr = "article/" + post_id + "/";
    const url = window.location.href.replace(substr, 'rate/') + post_id + "/" + rating + "/";
    fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => {
        window.location.reload();
    });
}
  

  