$(document).ready(function(){
    loadPost();
    loadComment();
    loadRelated();
    $('img').addClass('img-responsive').css('position', 'relative').css('overflow', 'hidden').css('max-width', '100%');
});

function answer(value){
    return "<div class='card answer-box' style='width: 100%; padding: 15px;'> \
                    <img src='asset/images/img6.jpg' alt='onsd' style='float: left' class='commenter-dp'>\
                    <span class='commenter-name'>"+value.name+", </span> <span class='bio'>Works at Ericsson Group of Companies</span>\
                    <br>\
                    <span class='total-answer-views'>4.3k</span> views\
                    <br>\
                    <div class='answer-content'>\
                    "+value.body+"\
                    </div>\
                    <br>\
                    <p>\
                        <button class='btn btn-default btn-xs'><span class='glyphicon glyphicon-thumbs-up'></span>  121</button>\
                        <button class='btn btn-default btn-xs'><span class='glyphicon glyphicon-thumbs-down'></span>  11</button>\
                        <button class='btn btn-primary btn-xs'><span class='glyphicon glyphicon-comment'></span>  4</button>\
                        <button class='btn btn-primary btn-xs' style='float: right;'><span class='glyphicon glyphicon-bookmark'></span> Bookmark</button>\
                    </p>\
                </div>";
    }


    function loadPost(){
        $.getJSON((window.location).toString().concat('answers'), function(data){
            $.each(data, function(key, value){
                $('.post').append();
            })
        })
    }

    function loadComment(){
        $.getJSON("asset/data/comments.json", function(data){
            $.each(data, function(key, value){
                $('.answers').append(answer(value));
            });
        });
    }

    function loadRelated(){
        $.getJSON("asset/data/posts.json", function(data){
            $.each(data, function(key, value){
                $('.related-posts-list').append("<a href='/topics/"+value.id+"'><li style='margin-bottom: 12px;'>"+value.title+"</li></a>")
            })
        })
    };

    $('.tile').mouseenter(function(){
        $(this).css('margin-left', '2px').css('margin-top', '2px');
    })

    $('.tile').mouseleave(function(){
        $(this).css('margin-left', '0px').css('margin-top', '0px');
    })