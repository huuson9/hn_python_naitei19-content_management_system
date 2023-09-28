$(document).ready(function () {
  $('.star').on('click', function () {
    var rating = parseInt($(this).data('rating'));
    var articleId = $(this).data('article-id');

    rate(rating, articleId);
  });

  function rate(rating, post_id) {
    var substr = "article/" + post_id + "/";
    var url = window.location.href.replace(substr, 'rate/') + post_id + "/" + rating + "/";
    
    $.ajax({
      url: url,
      type: 'GET',
      contentType: 'application/json',
      success: function () {
        window.location.reload();
      },
      error: function () {
        window.location.href = '/accounts/login/?next=/home/article/' + post_id + '/';
      }
    });
  }
});
