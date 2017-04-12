function notify(text){
    $('.notification').slideDown(1000).append("<span>"+text+"</span><a id='close' onclick='close_notify()'>[close]</a>");
}

function close_notify(){
    $('.notification').slideUp(500);
}

function is_user_logged_in(){
    if(is_loggedin.includes('False'))return false;
    else return true;
}

function get_exerpt_without_image(htmlCOntent){
    $('.hidden-').html(htmlCOntent);
    return $('.hidden-').text().substring(0, 100);
}

function convertdatetoword(value){
    var date = value.split("-");
    var month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    var new_date = date[2] + ' ' + month[parseInt(date[1]) - 1] + ', ' + date[0];
    return new_date
}

function show_hide_search_bar(){
    $('.search-addition').slideToggle(300);
    $('.search-input').focus();
}

function answerWriterAndHeader(answer){
    if(answer.anonymous == true) return "<div class='row'>\
                    <div class='col-lg-1'>\
                        <img src='"+default_profile_picture+"' alt='onsd' style='float: left' class='commenter-dp'>\
                    </div>\
                    <div class='col-lg-11' style='line-height: 25px;'>\
                        <span class='commenter-name'>Anonymous</span><br>\
                        <span class='bio'>" + convertdatetoword(answer.date_written) + ", " + answer.time_written + "<span><br>\
                    </div>\
                </div>";
    else return "<div class='row'>\
                    <div class='col-lg-1'>\
                        <img src='"+answer.writer.display_picture+"' alt='onsd' style='float: left' class='commenter-dp'>\
                    </div>\
                    <div class='col-lg-11' style='line-height: 25px;'>\
                    <a href='/profile/"+answer.writer.user.username+"'>\
                        <span class='commenter-name'>" + answer.writer.user.first_name + " " + answer.writer.user.last_name + ", </span></a> <span class='bio'>" + getBio(answer.writer) + "</span>\
                        <span class='pull-right badge'>" + answer.writer.profile_no_of_views + "</span><br>\
                        <span class='bio'>" + convertdatetoword(answer.date_written) + ", " + answer.time_written + "<span><br>\
                    </div>\
                </div>";
}

//Answers tab in profile

function commentsAndVotesInfoLine(value){
    if(value.no_of_comments == 0 && value.no_of_upvotes == 0) return '';
    else if(value.no_of_upvotes != 0 || value.no_of_comments != 0) return "<small><a class='comment-link' onclick='open_upvoters_modal("+value.id+")'>"+value.no_of_upvotes + pluralize(value.no_of_upvotes, 'upvote')+"</a>  &bullet; <a class='comment-link'onclick='showComments("+value.id+")'>" +value.no_of_comments + pluralize(value.no_of_comments, 'comment')+"</a></small>";
}

function pluralize(integer, string){
    if (integer > 1) return ' '+string+'s';
    else return ' '+string;
}

function answer(value){
    return "<div class='card answer-"+value.id+" answer-box-"+value.id+"' style='width: 100%; padding: 15px; background-color: #FFFFFF;'> \
                                <div class='answer-content'>\
                                <span class='question-title'><a href='/questions/"+value.question.slug+"'>"+value.question.title+"</a></span>\
                                <hr/>\
                                "+value.body+"\
                                </div>\
                                <p>\
                                 "+commentsAndVotesInfoLine(value)+"\
                                 </p>\
                                <p class='answer-toolbar-desktop'>\
                                "+check_logged_perm(value)+"\
                                </p>\
                                <span class='answer-toolbar-mobile'>\
                                "+check_logged_perm2(value)+"\
                                </span>\
                            </div>"
}

function new_answer(value){
    return " <li class='list-group-item answer-"+value.id+" trending-answer-"+value.id+" feed-answer-item'>\
                    <span class='small wrote-an-answer-to'>Damilola wrote an answer to What is your worst experience</span>\
                    <h5 class='answer-question'><a href='/questions/"+value.question.slug+"'>"+value.question.title+"</a></h5>\
                    <div class='writer-div'>\
                        <img class='related-user-thumbnail' src='http://127.0.0.1:8000/media/dps/SI_20150706_222145.jpg' alt='Damilola'>\
                        <a class='list-group-item-heading' target='_blank' href='/profile/damey2011'>Damilola Adeyemi,</a>\
                        <span class='small'>Software Architect</span>\
                        <p class='small'>Answer written 13 Mar, 2017, 17:56:00</p>\
                    </div>\
                    <div class='list-group-item-text feed-answer-text feed-answer-text-"+value.id+"'>\
                       "+value.body+"\
                    <br>\
                        <div class='read-more-container read-more-container-47'>\
                            <a href='#' class='feed-read-more-btn feed-read-more-btn-"+value.id+"' onclick='read_more("+value.id+")'>Continue Reading</a>\
                        </div>\
                    </div>\
                    <div class='answer-toolbar'>\
                        <p class='answer-toolbar-desktop'>\
                            "+check_logged_perm(value)+"\
                        </p>\
                        <span class='answer-toolbar-mobile'>\
                            "+check_logged_perm2(value)+"\
                        </span>\
                    </div>\
                </li>"
}

function read_more(answer){
    $('.feed-answer-text-'+answer).addClass('feed-answer-content-full');
    $('.read-more-container-'+answer).fadeOut();
    addAnswerView(answer);
}

function addAnswerView(answer_id){
    $.ajax({
        url: '/answers/add_view/?answer='+answer_id,
        data: {'csrfmiddlewaretoken': csrftoken},
        success: function(){
            console.log('Answer view added')
        }
    })
}

var answer_page = 1;

function loadAnswers(){
    $('.load-more-inner').html('<span class="ion-android-alarm-clock"></span> a sec');
    $.ajax({
        url: '/answers/'+req_user+'/?page='+answer_page,
        dataType: 'html',
        data: {'data': req_user, 'csrfmiddlewaretoken': csrftoken},
        success: function(data){
            if(data.length < 5) $('.post').append('<h4>No Answers written yet</h4>');
            else{
                $('.post').append(data);
            }
        },
        error: function(){
            console.log('Failed')
        },
        complete: function(){
            answer_page += 1;
            if($('#next_page').length != 0){
                $('.feed-load-more-btn').hide();
            }
            else{

            }
            $('.load-more-inner').html('<span class="ion-android-arrow-down"></span> Load More');
        }
    });
}

function check_logged_perm(value){
    if(user !=  'AnonymousUser' && user != value.writer.user.username){
        return "    "+check_if_answer_already_upvoted(false, value)+"\
                            "+check_if_answer_already_downvoted(false, value)+"\
                            &middot; <a class='comment-link comment' onclick='openAnswerCommentBox("+value.id+")'> add comment</a>\
                            &middot; <a href='/report/?type=A&type_id="+value.id+"&next="+window.location.href+"'> report</a>\
                            &middot; "+check_if_already_thanked(false, value)+"\
                            &middot; "+check_if_edits_suggested(false, value)+"\
                            "+check_if_bookmarked(false, value)+"";
    }
    else if(user=='AnonymousUser'){
        return "<span class='fa fa-thumbs-o-up'></span>  "+value.no_of_upvotes+"<span style='margin-right: 10px;'></span>\
                        <span class='fa fa-thumbs-o-down'></span>  "+value.no_of_downvotes+"<span style='margin-right: 10px;'></span>";
    }
    else if(user == value.writer.user.username){
        return "<span class='fa fa-thumbs-o-up'></span>  "+value.no_of_upvotes+"<span style='margin-right: 10px;'></span>\
                        <span class='fa fa-thumbs-o-down'></span>  "+value.no_of_downvotes+"<span style='margin-right: 10px;'></span>\
            <a href='/answers/edit/?answer="+value.id+"'>edit</a> &middot;\
            <a onclick='delete_answer("+value.id+")' class='comment-link' >delete</a>";
    }
}
function check_logged_perm2(value){
    if(user !=  'AnonymousUser' && user != value.writer.user.username){
        return "    "+check_if_answer_already_upvoted(true, value)+"\
            &middot; <a class='comment-link comment' onclick='openAnswerCommentBox("+value.id+")'> add comment</a>\
            <div class='dropup more-options-dropdown pull-right'>\
            <span class='ion-ios-more-outline answer-more-options-btn' type='button' id='dropdownMenu1' data-toggle='dropdown'></span>\
                <ul class='dropdown-menu answer-dropdown-options' role='menu' aria-labelledby='dropdownMenu1'>\
            <li role='presentation' class='dropdown-header'>User Actions</li>\
            "+check_if_answer_already_downvoted(true,value)+"\
            "+check_if_bookmarked(true, value)+"\
            "+check_if_already_thanked(true, value)+"\
            "+check_if_edits_suggested(true, value)+"\
            <li role='presentation'><a role='menuitem' tabindex='-1' href='/report/?type=Q&type_id="+value.id+"&next="+window.location.href+"'>Report</a></li>\
        </ul>\
        </div>\
        ";
    }
    else if(user==='AnonymousUser'){
        return "<span class='fa fa-thumbs-o-up'></span>  "+value.no_of_upvotes+"<span style='margin-right: 10px;'></span>\
                        <span class='fa fa-thumbs-o-down'></span>  "+value.no_of_downvotes+"<span style='margin-right: 10px;'></span>";
    }
    else if(user == value.writer.user.username){
        return "<span class='fa fa-thumbs-o-up'></span>  "+value.no_of_upvotes+"<span style='margin-right: 10px;'></span>\
                        <span class='fa fa-thumbs-o-down'></span>  "+value.no_of_downvotes+"<span style='margin-right: 10px;'></span>\
            <a href='/answers/edit/?answer="+value.id+"'>edit</a> &middot;\
            <a onclick='delete_answer("+value.id+")' class='comment-link'>delete</a>";
    }
}
function check_if_bookmarked(mobile, value){
    if(!mobile){
        if(value.archived){
            return "<button class='btn btn-primary clicked btn-sm archive-"+value.id+"' style='float: right;' onclick='unBookmarkAnswer("+value.id+")'><span class='fa fa-bookmark'></span> archived</button>"
        }
        else{
            return "<button class='btn btn-primary btn-sm archive-"+value.id+"' style='float: right;' onclick='bookmarkAnswer("+value.id+")'><span class='fa fa-bookmark'></span> archive</button>"
        }
    }
    else{
        if(value.archived){
            return "<li role='presentation'><a role='menuitem' onclick='unBookmarkAnswer("+value.id+")' tabindex='-1' class='comment-link archive-"+value.id+" clicked'>Archived</a></li>";
        }
        else{
            return "<li role='presentation'><a role='menuitem' onclick='bookmarkAnswer("+value.id+")' tabindex='-1' class='comment-link archive-"+value.id+"'>Archive</a></li>";
        }
    }

}

function check_if_answer_already_upvoted(mobile, value){
    if(!mobile){
        if(!value.upvoted) {
            return "<button class='btn btn-default btn-sm upvote-"+value.id+"' onclick='upvote("+value.id+")'><span class='fa fa-thumbs-o-up'></span>  upvote</button>";
        }
        else{
            return "<button class='btn btn-default clicked btn-sm upvote-"+value.id+"' onclick='r_upvote("+value.id+")'><span class='fa fa-thumbs-o-up'></span> upvoted</button>";
        }
    }
    else{
        if(!value.upvoted) {
            return "<button class='btn btn-default btn-sm upvote-"+value.id+"' onclick='upvote("+value.id+")'><span class='fa fa-thumbs-o-up'></span>  upvote</button>";
        }
        else{
            return "<button class='btn btn-default clicked btn-sm upvote-"+value.id+"' onclick='r_upvote("+value.id+")'><span class='fa fa-thumbs-o-up'></span> upvoted</button>";
        }
    }
}


function check_if_answer_already_downvoted(mobile, value){
    if(!mobile){
        if(!value.downvoted) {
            return "<a class='dwnv downvote-"+value.id+"' onclick='downvote("+value.id+")' href='#'> Downvote </a>";
        }
        else{
            $('.upvote-'+value.id).addClass('disabled');
            return "<a class='dwnv clicked downvote-"+value.id+"' onclick='r_downvote("+value.id+")' href='#'> Downvoted</a>";
        }
    }
    else{
        if(value.downvoted){
            return "<li role='presentation'><a role='menuitem' onclick='r_downvote("+value.id+")' href='#' tabindex='-1' class='comment-link clicked downvote-"+value.id+"'>Downvoted</a></li>";
        }
        else{
            return "<li role='presentation'><a role='menuitem' onclick='downvote("+value.id+")' href='#' tabindex='-1' class='comment-link downvote-"+value.id+"'>Downvote</a></li>";
        }
    }
}

function check_if_already_thanked(mobile, value){
    if(!mobile){
        if(!value.thanked) {
            return "<a class='comment-link thnk thank-"+value.id+"' onclick='thank("+value.id+")' href='#'> Gratify </a>";
        }
        else{
            return "<a class='thnk clicked thank-"+value.id+"' href='#'> Gratified </a>";
        }
    }
    else{
        if(value.thanked){
            return "<li role='presentation'><a role='menuitem' tabindex='-1' class='comment-link thank-"+value.id+"'>Gratified</a></li>";
        }
        else{
            return "<li role='presentation'><a role='menuitem' onclick='thank("+value.id+")' tabindex='-1' href='#' class='comment-link thank-"+value.id+"'>Gratify</a></li>";
        }
    }
}

function check_if_edits_suggested(mobile, value){
    if(!mobile){
        if(!value.edit_suggested) {
            return "<a class='editsug comment-link editsug-"+value.id+"' onclick='suggest_edit("+value.id+")' href='#'> Suggest Edits </a>";
        }
        else{
            return "<a class='editsug clicked editsug-"+value.id+"'> Suggestion Sent</a>";
        }
    }
    else{
        if(value.edit_suggested){
            return "<li role='presentation'><a role='menuitem' tabindex='-1' class='clicked editsug-"+value.id+"'>Suggestion Sent</a></li>";
        }
        else{
            return "<li role='presentation'><a role='menuitem' onclick='suggest_edit("+value.id+")' href='#' tabindex='-1' class='comment-link editsug-"+value.id+"'>Suggest Edits</a></li>";
        }
    }
}
//END OF INFO FOR ANSWER TAB


function upvote(answer_id) {
    $.post('/answers/upvote/?answer=' + answer_id + '&action=upvote', {
        'action': 'upvote',
        'csrfmiddlewaretoken': csrftoken
    }, function (data) {
        if (data == true) {
            $('.upvote-' + answer_id).html("<span class='fa fa-thumbs-o-up'></span> Upvoted").attr('onclick', 'r_upvote(' + answer_id + ')').addClass('clicked');
            $('.downvote-' + answer_id).attr('disabled', 'true');
            $.toast('Answer was upvoted', {'duration': 1000, 'align': 'top'});
        }
    });
}

function r_upvote(answer_id) {
    $.post('/answers/upvote/?answer=' + answer_id + '&action=r_upvote', {
        'action': 'r_upvote',
        'csrfmiddlewaretoken': csrftoken
    }, function (data) {
        if (data == true) {
            $('.upvote-' + answer_id).html("<span class='fa fa-thumbs-o-up'></span> Upvote").attr('onclick', 'upvote(' + answer_id + ')').removeClass('clicked');
            $('.downvote-' + answer_id).removeAttr('disabled');
            $.toast('You un-upvoted this answer', {'duration': 1000, 'align': 'top'});
        }
    });
}

function downvote(answer_id) {
    $.post('/answers/downvote/?answer=' + answer_id + '&action=downvote', {'csrfmiddlewaretoken': csrftoken}, function (data) {
        if (data == true) {
            $('.downvote-' + answer_id).html('Downvoted').attr('onclick', 'r_downvote(' + answer_id + ')').addClass('clicked');
            $('.upvote-' + answer_id).attr('disabled', 'true');
            $.toast('Answer was downvoted<br><i>Note: downvotes bring down writer and answer reputation</i>', {'duration': 1000, 'align': 'top'});
        }
    });
}

function r_downvote(answer_id) {
    $.post('/answers/downvote/?answer=' + answer_id + '&action=r_downvote', {'csrfmiddlewaretoken': csrftoken}, function (data) {
        if (data == true) {
            $('.downvote-' + answer_id).html('Downvote').attr('onclick', 'downvote(' + answer_id + ')').removeClass('clicked');
            $('.upvote-' + answer_id).removeAttr('disabled');
            $.toast('You un-downvoted this answer', {'duration': 1000, 'align': 'top'});
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
                $('.bookmark').removeAttr('onclick').attr('onclick', 'unBookmarkAnswer('+answer_id+')').html('Archived').addClass('clicked');
                $('.archive-'+answer_id).removeAttr('onclick').attr('onclick', 'unBookmarkAnswer('+answer_id+')').html('Archived').addClass('clicked')
            }
            $.toast('Answer has been added to your archive', {'duration': 1000, 'align': 'top'});

        },
        error: function () {
            //notify('An error occured');
        }
    })
}

function unBookmarkAnswer(answer_id) {
    $.ajax({
        url: '/answers/un_bookmark_answer/?answer=' + answer_id,
        type: 'post',
        data: {'csrfmiddlewaretoken': csrftoken},
        success: function (data) {
            if (data == true){
                $('.bookmark').removeAttr('onclick').attr('onclick', 'bookmarkAnswer('+answer_id+')').html('Archive').removeClass('clicked');
                $('.archive-'+answer_id).removeAttr('onclick').attr('onclick', 'bookmarkAnswer('+answer_id+')').html('Archive').removeClass('clicked');
                $.toast('Answer has been removed from your archive', {'duration': 1000, 'align': 'top'});
            }

        },
        error: function () {
            //notify('An error occured');
        }
    })
}

function thank(answer_id){
    $.ajax({
        url: '/answers/thank/?answer='+answer_id,
        type: 'POST',
        data: {'csrfmiddlewaretoken':csrftoken},
        success: function (data) {
            if(data) {
                $('.thank-'+answer_id).addClass('clicked').removeClass('comment-link').removeAttr('onclick').html('Gratified');
                $.toast('Gratification Sent', {'duration': 1000, 'align': 'top'})
            }
        },
        error: function(data){

        }
    })
}

function suggest_edit(answer_id){
    $.ajax({
        url: '/answers/suggest_edit/?answer='+answer_id,
        type: 'POST',
        data: {'csrfmiddlewaretoken':csrftoken},
        success: function (data) {
            if(data) {
                $('.editsug-'+answer_id).addClass('clicked').removeClass('comment-link').removeAttr('onclick').html('Edit Suggested');
                $.toast('Gratification Sent', {'duration': 1000, 'align': 'top'})
            }
        },
        error: function(data){

        }
    })
}

function follow(follows){
    $.ajax({
        url: '/follow/?follows='+follows,
        type: 'POST',
        data: {'user': user, 'follows':follows, 'csrfmiddlewaretoken': csrftoken},
        success: function(data){
            if(data == true){
                $('.follow').html('- unfollow').attr('onclick', 'unfollow('+follows+')').addClass('clicked');
                $('.related-user-'+follows).hide();
                $.toast('User has been followed', {'duration': 500, 'align': 'top'});
            }
        },
        error: function(){
            //notify('An error occurred');
            $.toast('An error has occured', {'duration': 1000, 'align': 'top'});
        }
    })
}

function unfollow(follows){
    $.ajax({
        url: '/unfollow/?follows='+follows,
        type: 'POST',
        data: {'csrfmiddlewaretoken': csrftoken},
        success: function(data){
            if(data == true){
                $('.follow').html(' + follow').attr('onclick', 'follow('+follows+')').removeClass('clicked');
                $.toast('User has been unfollowed', {'duration': 500, 'align': 'top'});
            }
        },
        error: function(){
            $.toast('An error has occured', {'duration': 1000, 'align': 'top'});
        }
    })
}

//Questions page

function loadQuestionAnswers() {
    $.ajax({
        url: '/questions/' + question_id + '/answers/',
        success: function (data) {
            $('.answers').append(data);
        },
        error: function () {
            $.toast('An error has occured, please reload the page', {'duration': 30000, 'align': 'top'});
        }
    })
}

$('.tile').mouseenter(function () {
    $(this).css('margin-left', '2px').css('margin-top', '2px');
});

$('.tile').mouseleave(function () {
    $(this).css('margin-left', '0px').css('margin-top', '0px');
});

function is_user_logged_in(){
    if(is_loggedin.includes('False'))return false;
    else return true;
}

function answer_question() {
    $('#answerModal').modal();
    $('.trumbowyg-editor').focus();
}

function delete_answer(answer_id) {
    $.ajax({
        url: '/answers/delete/?answer=' + answer_id,
        type: 'post',
        data: {'csrfmiddlewaretoken': csrftoken, 'answer': answer_id},
        success: function (data) {
            $.toast('Answer has been deleted', {'duration': 1000, 'align': 'top'});
            if (data == true) window.location.reload(true);
        },
        error: function () {
            $.toast('Answer couldnt be deleted', {'duration': 2000, 'align': 'top'});
        }
    })
}



function agree_with_this_answer(uv) {
    if (uv != 0) return uv + " people agree with this answer";
    else return ""
}

function getBio(value) {
    if (value.bio != null) return value.bio;
    else return ''
}


function openAnswerCommentBox(answer_id){
    $('.comment-div-'+answer_id).css('display', 'none');

    if ($('.comment-div-'+answer_id).length){
        $('.comment-div-'+answer_id).css('display', 'block');
    }
    else{
        $('.answer-'+answer_id).append("<br><div class='comment-div-"+answer_id+"'>\
            <label for='comment'>Your Comment:</label><a onclick='close_comment_box("+answer_id+")' class='comment-link comment-box-close-btn'>[X]</a>\
            <textarea name='comment' id='answer-comment-"+answer_id+"' cols='30' rows='4' class='form-control answer-comment comment-"+answer_id+"'></textarea>\
            <br>\
            <button class='btn btn-default' onclick='SubmitComment(1, "+answer_id+")'>Comment</button>\
        </div>");
    }

    $('#answer-comment-'+answer_id).focus();
}

function openCommentCommentBox(comment_id){
    $('.reply-link-'+comment_id).css('display', 'none');
    if ($('.comment-div-'+comment_id).length){
        $('.comment-div-'+comment_id).css('display', 'block');
    }
    else{
        $('.comment-'+comment_id).append("<br><div class='comment-div-"+comment_id+"'>\
            <label for='comment'>Your Comment:</label><a onclick='close_comment_box("+comment_id+")' class='comment-link comment-box-close-btn'>[X]</a>\
            <textarea name='comment' id='comment-comment-"+comment_id+"' cols='30' rows='4' class='form-control comment-comment comment-"+comment_id+"'></textarea>\
            <br>\
            <button class='btn btn-default' onclick='SubmitComment(2, "+comment_id+")'>Comment</button>\
        </div>");
    }

    $('#comment-comment-'+comment_id).focus();
}


function close_comment_box(parent_id){
    $('.comment-div-'+parent_id).css('display', 'none');
    $('.reply-link-'+parent_id).css('display', 'block');
}

function SubmitComment(commentType, parent_id){
    var answer_comment_content = $('#answer-comment-'+parent_id).val();
    switch(commentType){
        case 1:
            $.ajax({
                url: '/comments/post/',
                method: 'POST',
                data: {'csrfmiddlewaretoken': csrftoken, 'comment_content': answer_comment_content, 'parent_id': parent_id,
                    'parent_type': 1},
                success: function(data){
                    $.toast('Comment was Added', {'duration': 2000, 'align': 'top'});
                    window.location.reload(true);
                },
                error:function(data){
                    $.toast('Sorry, an error has occured', {'duration': 2000, 'align': 'top'});
                }

            });
            break;
        case 2:
            var comment_comment_content = $('#comment-comment-'+parent_id).val();
            $.ajax({
                url: '/comments/post/',
                method: 'POST',
                data: {'csrfmiddlewaretoken': csrftoken, 'comment_content': comment_comment_content, 'parent_id': parent_id,
                    'parent_type': 2},
                success: function(data){
                    $.toast('Comment was Added', {'duration': 2000, 'align': 'top'});
                    window.location.reload(true);
                },
                error:function(data){
                    $.toast('Sorry, an error has occured, please reload page', {'duration': 30000, 'align': 'top'});
                }
            })
    }
}


function showComments(answer_id){
    $('#commentsModal').modal();
    loadComments(answer_id);

}

function loadComments(answer_id){
    $.ajax({
        url: '/comments/?answer='+answer_id,
        data: {'csrfmiddlewaretoken': csrftoken},
        success: function(data){
            console.log(data);
            if(data.results.length == 0){
                $('.comment-modal-body').html('<h4>No Comment Under This Answer This Yet!!</h4>');
                $('.answer-comments').html('<h4>No Comment Under This Answer This Yet!!</h4>');
            }
            else{
                $('.comment-modal-body').html('');

                $('.comment-modal-header').html("<blockquote class='custom-bq'>\
                        <span class='comment-writer'><a href='#'>"+data.results[0].parent_answer.writer.user.first_name+" " +data.results[0].parent_answer.writer.user.last_name+"</a>, "+data.results[0].parent_answer.writer.bio+"</span>\
                        <div class='quoted-answer small'>"+get_exerpt_without_image(data.results[0].parent_answer.body)+"</div>\
                    </blockquote>");

                $.each(data.results, function(key, value){
                    $('.comment-modal-body').append("<blockquote class='custom-bq comment-"+value.id+"'>\
                        <span class='comment-writer'><a href='#'>"+value.writer.user.first_name+" "+value.writer.user.last_name+"</a>, "+value.writer.bio+"</span>\
                        <div class='quoted-answer small'>"+value.body+"</div>\
                        "+if_replies_dom(value)+"\
                    </blockquote>");

                    $('.answer-comments').append("<blockquote class='custom-bq comment-"+value.id+"'>\
                        <span class='comment-writer'><a href='#'>"+value.writer.user.first_name+" "+value.writer.user.last_name+"</a>, "+value.writer.bio+"</span>\
                        <div class='quoted-answer small'>"+value.body+"</div>\
                        "+if_replies_dom(value)+"\
                    </blockquote>")
                });
            }
        },
        error: function(data){
            $.toast('Sorry, an error has occured', {'duration': 2000, 'align': 'top'});
        }
    })
}

function if_replies_dom(value){
    var lr = "<a onclick='openCommentCommentBox("+value.id+")' class='comment-link reply-link reply-link-"+value.id+"'><span class='ion-reply'></span> reply </a>";

    if(value.replies_count != 0){
        lr += "&bullet; <a class='load-rep-"+value.id+" comment-link load-replies' onclick='loadReplies("+value.id+", \""+value.replies+"\")'>load replies</a>";
    }
    return lr;
}

function loadReplies(parent_id, replies_url){
    $.ajax({
        url: replies_url,
        data: {'csrfmiddlewaretoken':csrftoken},
        success: function(data){
            if(data.length != 0){
                $.each(data, function(key, value){
                    $('.comment-'+parent_id).append("<blockquote class='custom-bq comment-"+value.id+"'>\
                        <span class='comment-writer'><a href='#'>"+value.writer.user.first_name+" "+value.writer.user.last_name+"</a>, "+value.writer.bio+"</span>\
                        <div class='quoted-answer small'>"+value.body+"</div>\
                    <p>"+if_replies_dom(value)+"</p>\
                    </blockquote>")
                });
                $('.load-rep-'+parent_id).hide();
            }
            else{
                $('.comment-'+parent_id).append("No replies to this comment");
                $('.load-rep-'+parent_id).hide()
            }
        },
        error: function(data){

        }
    })
}

//end questions page



//Profile Following tab
//var load_more = "<a href='#' onclick='load_more()' class='btn-load'><span class='fa fa-refresh'></span> Load More</a>";
var original_getfollowings_url = '/profile/'+req_user+'/followings/api';
var nextUrl = '/profile/'+req_user+'/followings/api';

function follow_item_dom(data){
    if(is_user_logged_in() && data.is_following.user.username != user){
        return "<li class='list-group-item'>\
                    <div class='list-group-item-heading'>\
                        <span class='follower-username'><a href='/profile/"+data.is_following.user.username+"'>"+data.is_following.user.first_name+" "+data.is_following.user.last_name+"</a></span>\
                        "+follow_unfollow_button(data.reverse_follows, data.is_following.user)+"\
                    </div>\
                    <div class='list-group-item-text follower-bio'>"+data.is_following.bio+"</div>\
                </li>"
    }
    else{
        return "<li class='list-group-item'>\
                    <div class='list-group-item-heading'>\
                        <span class='follower-username'><a href='/profile/"+data.is_following.user.username+"'>"+data.is_following.user.first_name+" "+data.is_following.user.last_name+"</a></span>\
                    </div>\
                    <div class='list-group-item-text follower-bio'>"+data.user.bio+"</div>\
                </li>"
    }
}

function load_following(user){
    $('.loading-1').show();
    $.ajax({
        url: nextUrl,
        data: {'csrfmiddlewaretoken': csrftoken},
        success: function(data){
            if(data.results.length == 0) $('.following-window').append('<h3>No Following</h3>');
            else{
                $.each(data.results, function(key, value){
                    $('.following-window').append(follow_item_dom(value))
                });
            }
            if(data.next!=null){
                $('.btn-load').css('display', 'block').show();
                nextUrl = data.next;
                $('.loading-1').hide();
            }
            else{
                $('.loading-1').hide();
                $('.load-btn').hide();
            }

        },
        error: function (data) {
            $('.loading-1').hide();
            $('.load-btn').hide();
            $('.following-window').append('<h3>Please Register or Login</h3>');
        }
    })
}

function follow_unfollow_button(is_following_bool, follows){
    if(is_user_logged_in() && !is_following_bool) return "<a onclick='follow_item("+follows.id+")' class='ff-list-btn follow-item-"+follows.id+"'> <span class='ion-android-person-add'></span> </a>";
    else if(is_user_logged_in() && is_following_bool) return "<a onclick='unfollow_item("+follows.id+")' class='icon-follow-clicked ff-list-btn follow-item-"+follows.id+"'><span class='ion-android-people'></span></a>";
    else return ""
}

function follow_item(follows){
    $.ajax({
        url: '/follow/?follows='+follows,
        type: 'POST',

        data: {'csrfmiddlewaretoken': csrftoken},
        success: function(data){
            if(data == true){
                $('.follow-item-'+follows).attr('onclick', 'unfollow_item('+follows+')').html("<span class='ion-android-people'></span>").addClass('icon-follow-clicked')
            }
        },
        error: function(){
            //notify('An error occurred');
        }
    })
}

function unfollow_item(follows){
    $.ajax({
        url: '/unfollow/?follows='+follows,
        type: 'POST',
        data: {'csrfmiddlewaretoken': csrftoken},
        success: function(data){
            if(data == true){
                $('.follow-item-'+follows).html("<span class='ion-android-person-add'></span>").attr('onclick', 'follow_item('+follows+')').removeClass('icon-follow-clicked');
                //notify("Unfollowed");
            }
        },
        error: function(){
            //notify('An error occurred');
        }
    })
}
//Profile FOllowing tab


//Peofile FOllowers Tab
var original_getfollowers_url = '/profile/'+req_user+'/followers/api';
var nextPage = '/profile/'+req_user+'/followers/api';

function load_followers(user){
    $('.loading-1').css('display', 'block').show();
    $.ajax({
        url: nextPage,
        data: {'csrfmiddlewaretoken': csrftoken},
        success: function(data){
            if(data.results == 0) $('.follower-window').append('<h3>No Follower</h3>');
            else{
                $.each(data.results, function(key, value){
                    $('.follower-window').append(follower_item_dom(value));
                });
            }
            if(data.next!=null){
                nextPage = data.next;
                $('.loading-1').hide();
                $('.btn-load').css('display', 'block').show();
            }
            else{
                $('.loading-1').hide();
                $('.btn-load').hide();
            }
        },
        error: function (data) {
            $('.loading-1').hide();
            $('.btn-load').hide();
            $('.follower-window').html('<h3>Please Register or Login</h3>')
        }
    })
}

function follower_item_dom(data){
    if(data.user.user.username != user){
        return "<li class='list-group-item'>\
                    <div class='list-group-item-heading'>\
                        <span class='follower-username'><a href='/profile/"+data.user.user.username+"'>"+data.user.user.first_name+" "+data.user.user.last_name+"</a></span>\
                        "+follow_unfollow_button(data.reverse_follows, data.user.user)+"\
                    </div>\
                    <div class='list-group-item-text follower-bio'>"+data.user.bio+"</div>\
                </li>"
    }
    else if(user=='AnonymousUser' || user == data.is_following.user.username){
        return "<div class='list-group-item'>\
                    <h4><a href='/profile/"+data.user.user.username+"'>"+data.user.user.first_name+" "+data.user.user.last_name+"</a></h4>\
                </div>"
    }
    else{
        return "<div class='list-group-item'>\
                    <h4><a href='/profile/"+data.user.user.username+"'>"+data.user.user.first_name+" "+data.user.user.last_name+"</a></h4>\
                </div>"
    }
}

function load_more(val){
    if(val==1)load_following(user);
    if(val==2)load_followers(user);
    if(val==3)load_questions(user);
    if(val==4)loadAnswers();
    if(val==5)loadTopicAnswers();
    if(val==6)loadExploreTopics();
    if(val==7)loadExplorePeople();
    if(val==8)loadExploreQuestions();
    if(val==9)loadTrending();
}


//Profile Questions Tab
var original_getquestions_url = '/questions/'+req_user+'/questions';
var nextQuestionPage = '/questions/'+req_user+'/questions';

function load_questions(user){
    $('.loading-1').show();
    $.ajax({
        url: nextQuestionPage,
        data: {'csrfmiddlewaretoken': csrftoken},
        success: function(data){
            if(data.length == 0){
                $('.questions-window').append("<h3>No Question Asked By User</h3>");
                $('.loading-1').hide();
            }
            else{
                $('.questions-window').append(data);
            }
            $('.loading-1').hide();
        },
        error: function (data) {
            console.log(data)
            $('.loading-1').hide();
        }
    })
}

function question_item_dom(data){
    return "<li class='list-group-item'>\
                    <pclass='small'>"+data.date_asked+"</p>\
                    <span class='list-group-item-header'><a href='/questions/"+data.slug+"'>"+data.title+"</a></span>\
                    <hr class='divider'/>\
                    <p class='list-group-item-text small'>"+data.no_following_quest+" people are following this question</p>\
                </li>"
}


function loadTopicsThatUserFollows(){
    $.ajax({
        url: '/profile/topics_followed/?req_user='+req_user+'&user='+user,
        data: {'csrfmiddlewaretoken': csrftoken},
        success: function(data){
            if(data.length==0) $('.topic-explore-list').append('<h4>No Topic Followed</h4>');
            else{
                $.each(data, function(key, value){
                    $('.topic-explore-list').append(explore_topic_dom(value));
                    if(user==req_user) $('.t-'+value.id).hide();
                });
            }
        },
        error: function (data) {
            console.log(data)
        }
    })
}


/////////////////////////END OF SCRIPT FOR PROFILE ///////////////////////////////////////

//////////////////////////////////////////////////////////////////////////////////////////
////////TOPIC/////////////////////////////////////////////////////////////////////////////

function follow_topic(topic_id){
    $.ajax({
        url: '/topics/follow/?topic='+topic_id,
        method: 'post',
        data: {'csrfmiddlewaretoken': csrftoken},
        success: function(data){
            if(data==true){
                $('.topic-follow-'+topic_id).attr('onclick', 'unfollow_topic('+topic_id+')').html('- unfollow').addClass('clicked');
                $('.t-'+topic_id).attr('onclick', 'unfollow_topic('+topic_id+')').html('- unfollow');
            }
            else{
                //do nothing
                alert(data)
            }
            $.toast('Topic was followed', {'duration': 500, 'align': 'top'});
        },
        error: function(data){

        }
    })
}

function unfollow_topic(topic_id){
    $.ajax({
        url: '/topics/unfollow/?topic='+topic_id,
        method: 'post',
        data: {'csrfmiddlewaretoken': csrftoken},
        success: function(data){
            if(data==true){
                $('.topic-follow-'+topic_id).attr('onclick', 'follow_topic('+topic_id+')').html('+ follow').removeClass('clicked');
                $('.t-'+topic_id).attr('onclick', 'follow_topic('+topic_id+')').html('+ follow');
            }
            else{
                alert(data)
            }
            $.toast('Topic was unfollowed', {'duration': 2000, 'align': 'top'});
        },
        error: function(data){
            $.toast('Sorry, an error has occured', {'duration': 2000, 'align': 'top'});
        }
    })
}

function check_if_following_topic(topic_id){
    var b = false;
    $.ajax({
        url: '/topics/iffollow/?topic='+topic_id,
        method: 'post',
        data: {'csrfmiddlewaretoken': csrftoken},
        success: function(data){
            b = data;
        },
        error: function(data){
            //alert(data)
            $.toast('Sorry, an error has occured, please reload the page', {'duration': 2000, 'align': 'top'});

        },
        async: false
    })
}

function loadTopicAnswers() {
    $.ajax({
        url: topic_load_url+'&page='+next_topic_answers_page,
        dataType: 'html',
        data: {'csrfmiddlewaretoken': csrftoken},
        success: function (data) {
            //if (!data.results) $('.post').append('<h3>No Answers written yet</h3>');
            //else {
            //    $.each(data.results, function (key, value) {
            //        $('.post').append(answer(value));
            //        $('img').addClass('img-responsive');
            //    });
            //}
            //if (data.next != null) {
            //    $('.btn-load').show();
            //    topic_load_url = data.next;
            //    $('.loading-1').hide();
            //}
            //else {
            //    $('.loading-1').hide();
            //    $('.load-btn').hide();
            //}'
            $('.post').append(data);
        },
        error: function () {
            $.toast('Sorry, an error has occured', {'duration': 2000, 'align': 'top'});
        },
        complete: function(){
            next_topic_answers_page += 1;
        }
    });
}

function loadRelatedTopics(){
    $.ajax({
        url: '/topics/related',
        data: {'csrfmiddlewaretoken': csrftoken},
        success: function (data) {
            $.each(data, function(key, value){
                if(value != undefined){
                    $('.other-topics').append(related_topic_dom(value));
                }
            });
            $('.loading-1').hide();
        },
        error: function(data){
            //alert(data);
            $.toast('Sorry, an error has occured, please reload the page', {'duration': 30000, 'align': 'top'});

        }
    })
}

function related_topic_dom(data){
    return "<li class='other-item'>\
                <img src='"+data.image_name+"' alt='"+data.title+"' class='related-topic-thumbnail'>\
                <span class='related-topic-right'>\
                    <a href='/topics/"+data.slug+"'>"+data.title+"</a>\
                    <a class='other-topic-follow-btn badge badge-follow-btn t-"+data.id+"' onclick='follow_topic("+data.id+")'>+ follow</a>\
                </span>\
                <hr class='other-topic-divisor'>\
            </li>";
}

function loadUsersWithCommonInterest(){
    $.ajax({
        url: related_users_load_url,
        data: {'csrfmiddlewaretoken': csrftoken},
        success: function (data) {
            if(data){
                $.each(data, function(key, value){
                    $('.common-user-group').append(related_user_dom(value));
                });
                $('.loading-1-users').hide();
            }
            else{
                $('.common-user-group').append('<h6>No User currently following this topic that you are not following</h6>');
                $('.loading-1-users').hide();
            }
        },
        error: function(data){
            //alert(data);
            $.toast('Sorry, an error has occured, please reload the page', {'duration': 30000, 'align': 'top'});
        }
    })
}

function related_user_dom(user){
    return "<li class='list-group-item related-user-"+user.user.id+"'>\
        <img class='related-user-thumbnail' src='"+user.display_picture+"' alt='"+user.user.first_name+"'>\
        <a class='badge badge-follow-btn' onclick='follow("+user.user.id+")'>Follow</a>\
        <h5 class='list-group-item-heading'><a href='/profile/"+user.user.username+"'>"+user.user.first_name+" "+user.user.last_name+"</a></h5>\
        <p class='list-group-item-text'>"+user.bio+"</p>\
    </li>"
}


//EXPLORE
//////
//IN TOPIC/EXPLORE.HTML
/////


function loadExploreTopics(){
    $.ajax({
        url: next_explore_topic_url,
        data: {'csrfmiddlewaretoken': csrftoken},
        success: function(data){
            if(data.results){
                $.each(data.results, function (key, value) {
                    $('.topic-explore-list').append(explore_topic_dom(value))
                });
                next_explore_topic_url = data.next;
            }
            else{
                $('.topic-explore-list').append('<h3>Heyo, No new topic for you at the moment <br></h3>')
            }


            if(data.next!=null){
                $('.loading-1').hide();
                $('.btn-load').css('display', 'block').show();
            }
            else{
                $('.loading-1').hide();
                $('.btn-load').hide();
            }
        },
        error: function(data){
            $('.loading-1').hide();
            $('.btn-load').hide();
        }
    })
}

function explore_topic_dom(topic){
    return "<li class='list-group-item'>\
        <img class='related-user-thumbnail' src='"+topic.image_name+"' alt='"+topic.title+"'>\
        <a class='badge badge-follow-btn t-"+topic.id+"' onclick='follow_topic("+topic.id+")' target='_blank'>follow</a>\
        <h5 class='list-group-item-heading'><a href='/topics/"+topic.slug+"'>"+topic.title+"</a></h5>\
        <p class='list-group-item-text'>"+topic.desc+"</p>\
    </li>"
}

function loadExplorePeople(){
    $.ajax({
        url: next_explore_people_url,
        data: {'csrfmiddlewaretoken': csrftoken},
        success: function(data){
            if(data.results){
                $.each(data.results, function (key, value) {
                    $('.people-explore-list').append(explore_people_dom(value, true))
                });
                next_explore_people_url = data.next;
            }
            else{
                $('.people-explore-list').append('<h3>Heyo, No new user for you at the moment <br></h3>')
            }


            if(data.next!=null){
                $('.loading-1').hide();
                $('.btn-load').css('display', 'block').show();
            }
            else{
                $('.loading-1').hide();
                $('.btn-load').hide();
            }
        },
        error: function(data){
            $('.loading-1').hide();
            $('.btn-load').hide();
            $.toast('Sorry, an error has occured, please reload the page', {'duration': 30000, 'align': 'top'});
        }
    })
}

function explore_people_dom(user, need_follow_button){
    return "<li class='list-group-item related-user-"+user.user.id+"'>\
        <img class='related-user-thumbnail' src='"+user.display_picture+"' alt='"+user.user.first_name+"'>\
        "+explore_people_follow_btn(user, need_follow_button)+"\
        <h5 class='list-group-item-heading'><a href='/profile/"+user.user.username+"'>"+user.user.first_name+" "+user.user.last_name+"</a></h5>\
      <p class='list-group-item-text'>"+user.bio+"</p>\
    </li>"
}

function explore_people_follow_btn(user, need_follow_btn){
    if(need_follow_btn) return "<a class='badge badge-follow-btn' onclick='follow("+user.user.id+")' target='_blank'>+ follow</a>";
    else return "";
}



//Question explore
function loadExploreQuestions(){
    $.ajax({
        url: next_explore_questions_url,
        data: {'csrfmiddlewaretoken': csrftoken},
        success: function(data){

            if(data.results){
                $.each(data.results, function (key, value) {
                    $('.question-explore-list').append(explore_questions_dom(value))
                });
                next_explore_questions_url = data.next;
            }
            else{
                $('.question-explore-list').append('<h3>Heyo, No recent questions <br></h3>')
            }


            if(data.next!=null){
                $('.loading-1').hide();
                $('.btn-load').css('display', 'block').show();
            }
            else{
                $('.loading-1').hide();
                $('.btn-load').hide();
            }
        },
        error: function(data){
            console.log(data);
            $('.question-explore-list').append('<h3>Heyo, Please Register or Login<br></h3>');
            $('.loading-1').hide();
            $('.btn-load').hide();
        }
    })
}

function explore_questions_dom(question){
    return "<li class='list-group-item'>\
        <a class='badge badge-follow-btn' target='_blank' href='/questions/"+question.slug+"/answerit' _blank><span class='fa fa-pencil'> answer</span></a>\
        <h5 class='list-group-item-heading'><a href='/questions/"+question.slug+"'>"+question.title+"</a></h5>\
        <p class='list-group-item-text small'>"+get_exerpt_without_image(question.question_details)+"</p>\
        <hr style='margin-bottom: 3px;'>\
        <small>"+question.no_of_answers+" answers &bullet; "+question_follow_btn_dom(question.id)+" "+people_following_question(question.no_following_quest)+"</small>  \
    </li>"
}

function people_following_question(no_of_followers){
    if(no_of_followers == 0){
        return ""
    }
    else if(no_of_followers == 1){
        return "&middot; 1 person following this question"
    }
    else{
        return "&middot; "+no_of_followers+" people are following this question";
    }
}


function question_follow_btn_dom(question){
    if (is_following_question(question)) return "<a class='question-follow following-q question-follow-"+question+"' onclick='unfollow_question("+question+")'><span class='ion-reply'></span> Unfollow</a>";
    else return "<a class='question-follow question-follow-"+question+"' onclick='follow_question("+question+")'><span class='ion-reply'></span> Follow</a>"
}

function is_following_question(question){
    var bool_ = false;
    $.ajax({
        url: '/questions/is_following/?question='+question,
        data: {'csrfmiddlewaretoken': csrftoken},
        success: function (data) {
            console.log(data);
            bool_ = data
        },
        error: function(data) {
            bool_ = data;
            $.toast('Sorry, an error has occured, please reload the page', {'duration': 30000, 'align': 'top'});
        },
        async:false
    });
    return bool_;
}

function follow_question(question){
    $.ajax({
        url: '/questions/follow/?question='+question+'',
        data: {'csrfmiddlewaretoken': csrftoken},
        success: function (data) {
            $('.question-follow-'+question).html("<span class='ion-reply'></span> Unfollow").attr('onclick', 'unfollow_question('+question+')').addClass('following-q');
            $.toast('Question was followed', {'duration': 800, 'align': 'top'});
        },
        error: function(data) {
            $.toast('Sorry, an error has occured, please reload the page', {'duration': 5000, 'align': 'top'});
        }
    });
}

function unfollow_question(question){
    $.ajax({
        url: '/questions/unfollow/?question='+question+'',
        data: {'csrfmiddlewaretoken': csrftoken},
        success: function (data) {
            $('.question-follow-'+question).html("<span class='ion-reply'></span> Follow").attr('onclick', 'follow_question('+question+')').removeClass('following-q');
            $.toast('Question was unfollowed', {'duration': 800, 'align': 'top'});
        },
        error: function(data) {
            $.toast('Sorry, an error has occured, please reload the page', {'duration': 30000, 'align': 'top'});
        }
    });
}

function loadTrending(){
    $.ajax({
        url: next_trending_url,
        data: {'csrfmiddlewaretoken': csrftoken},
        success: function(data){
            if(data.results){
                $.each(data.results, function (key, value) {
                    $('.trending-list').append(trending_dom(value));
                    //$('.trending-list').append("<hr class='divider'>")
                });
                next_trending_url = data.next;
            }
            else{
                $('.trending-list').append('<h3>Heyo, No Posts Yet <br></h3>')
            }


            if(data.next!=null){
                $('.loading-1').hide();
                $('.btn-load').css('display', 'block').show();
            }
            else{
                $('.loading-1').hide();
                $('.btn-load').hide();
            }
        },
        error: function(data){
            $('.question-explore-list').append('<h3>Heyo, Please Register or Login<br></h3>');
            $('.loading-1').hide();
            $('.btn-load').hide();
        }
    })
}


function trending_dom(answer){
    return "<li class='list-group-item answer-"+answer.id+" trending-answer-"+answer.id+"'>\
        <span class='small wrote-an-answer-to'>&middot; "+answer.writer.user.first_name+" wrote an answer to "+answer.question.title+"</span>\
        <h5><a href='/questions/"+answer.question.slug+"' target='_blank'>"+answer.question.title+"</a></h5>\
        <img class='related-user-thumbnail' src='"+answer.writer.display_picture+"' alt='"+answer.writer.user.first_name+"'>\
        <a class='list-group-item-heading' target='_blank' href='/profile/"+answer.writer.user.username+"'>"+answer.writer.user.first_name+" "+answer.writer.user.last_name+",</a>\
        <span class='small'>"+answer.writer.bio+"</span>\
        <p class='small'>Answer written on "+convertdatetoword(answer.date_written)+", "+answer.time_written+"</p>\
        <p class='list-group-item-text trending-answer-text'>"+get_exerpt_without_image(answer.body)+"" +
        "<br/><a href='/answers/"+answer.id+"' target='_blank'>..read more</a></p>\
        <p class='answer-toolbar-desktop'>\
        "+check_logged_perm(answer)+"\
        </p>\
        <span class='answer-toolbar-mobile'>\
        "+check_logged_perm2(answer)+"\
        </span>\
    </li>"
}

function open_upvoters_modal(answer_id){
    $('#upvotersModal').modal();
    if($('.upvoters-list').children().length != 0){
        //do nothing
    }
    else{
        show_upvoters(answer_id);
    }

}


function show_upvoters(answer_id){


    $('.loading-1-upvoters').css('display','block');
    $('.btn-load-upvoters').css('display', 'none');

    $.ajax({
        url: next_upvoters_url,
        data: {'csrfmiddlewaretoken': csrftoken},
        success: function(data){
            if (data.results.length != 0){
                $.each(data.results, function(key, value){
                    $('.upvoters-list').append(explore_people_dom(value, false))
                });
                if(data.next != null){
                    $('.loading-1-upvoters').css('display','none');
                    $('.btn-load-upvoters').css('display', 'block');
                    next_upvoters_url = data.next;
                }
                else{
                    $('.loading-1-upvoters').css('display','none');
                    $('.btn-load-upvoters').css('display', 'none');
                }
            }
        },
        error:function(data){
            $.toast('Sorry, an error has occured, please reload the page', {'duration': 4000, 'align': 'top'});
        }
    })
}

function openMessageModal(user){
    $('#messageModal').modal();
    $('.message-textfield').focus();
}

function sendMessage(receipient){
    var message = $('.message-textfield').val();
    $.ajax({
        url: '/messages/send/?user_id='+receipient,
        type: 'POST',
        data: {'csrfmiddlewaretoken': csrftoken,'message':message, 'receiver':receipient},
        success: function(data){
            if(data==true){
                $.toast('Message Sent', {'duration': 1000, 'align': 'top'});
                $('#messageModal').modal('hide');
                $('.message-textfield').val('');
            }
            else $.toast('Message Sending Failed, Please refresh', {'duration': 2000, 'align': 'top'});
        },
        error:function(data){
            $.toast('An error has occured', {'duration': 2000, 'align': 'top'});
        }
    })
}

function sendFile(file, editor, welEditable) {
    data = new FormData();
    data.append("image", file);
    $.ajax({
        data: data,
        type: "POST",
        url: "/upload",
        cache: false,
        contentType: false,
        processData: false,
        success: function(url) {
            editor.insertImage(welEditable, url);
        }
    });
}
