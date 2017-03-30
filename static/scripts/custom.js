function upvote(answer_id) {
    $.post('/answers/upvote/?answer=' + answer_id + '&action=upvote', {
        'action': 'upvote',
        'csrfmiddlewaretoken': csrftoken
    }, function (data) {
        if (data == true) {
            $('.upvote-' + answer_id).html("<span class='fa fa-chevron-down'></span> Upvoted").attr('onclick', 'r_upvote(' + answer_id + ')')
            $('.downvote-' + answer_id).attr('disabled', 'true');
        }
    });
}

function r_upvote(answer_id) {
    $.post('/answers/upvote/?answer=' + answer_id + '&action=r_upvote', {
        'action': 'r_upvote',
        'csrfmiddlewaretoken': csrftoken
    }, function (data) {
        if (data == true) {
            $('.upvote-' + answer_id).html("<span class='fa fa-chevron-up'></span> Upvote").attr('onclick', 'upvote(' + answer_id + ')')
            $('.downvote-' + answer_id).removeAttr('disabled');
        }
    });
}

function downvote(answer_id) {
    $.post('/answers/downvote/?answer=' + answer_id + '&action=downvote', {'csrfmiddlewaretoken': csrftoken}, function (data) {
        if (data == true) {
            $('.downvote-' + answer_id).html('Downvoted').attr('onclick', 'r_downvote(' + answer_id + ')')
            $('.upvote-' + answer_id).attr('disabled', 'true');
        }
    });
}

function r_downvote(answer_id) {
    $.post('/answers/downvote/?answer=' + answer_id + '&action=r_downvote', {'csrfmiddlewaretoken': csrftoken}, function (data) {
        if (data == true) {
            $('.downvote-' + answer_id).html('Downvote').attr('onclick', 'downvote(' + answer_id + ')')
            $('.upvote-' + answer_id).removeAttr('disabled');
        }
    });
}

function bookmarkAnswer(answer_id) {
    $.ajax({
        url: '/answers/bookmark_answer/?answer=' + answer_id,
        type: 'post',
        data: {'csrfmiddlewaretoken': csrftoken},
        success: function (data) {
            if (data == true) {
                $('.bookmark').removeAttr('onclick').attr('onclick', 'unBookmarkAnswer('+answer_id+')').html('archived')
            }
        },
        error: function () {
            alert('An error occured');
        }
    })
}

function unBookmarkAnswer(answer_id) {
    $.ajax({
        url: '/answers/un_bookmark_answer/?answer=' + answer_id,
        type: 'post',
        data: {'csrfmiddlewaretoken': csrftoken},
        success: function (data) {
            if (data == true)$('.bookmark').removeAttr('onclick').attr('onclick', 'bookmarkAnswer('+answer_id+')').html('archive')
        },
        error: function () {
            alert('An error occured');
        }
    })
}


function follow(user, follows){
    $.ajax({
        url: '/follow/',
        type: 'POST',
        data: {'user': user, 'follows':follows, 'csrfmiddlewaretoken': csrftoken},
        success: function(data){
            console.log(data);
            if(data == true){
                $('.follow').html('- unfollow').attr('onclick', 'unfollow('+user+', '+follows+')');
            }
        },
        error: function(){
            alert('An error occurred');
        }
    })
}

function unfollow(user, follows){
    $.ajax({
        url: '/unfollow/',
        type: 'POST',
        data: {'user': user, 'follows':follows, 'csrfmiddlewaretoken': csrftoken},
        success: function(data){
            console.log(data);
            if(data == true){
                $('.follow').html(' + follow').attr('onclick', 'follow('+user+', '+follows+')');
            }
        },
        error: function(){
            alert('An error occurred');
        }
    })
}