function showSuccessMsg() {
    $('.save_success').fadeIn('fast', function() {
        setTimeout(function(){
            $('.save_success').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    //上传头像
    $("#form-avatar").submit(function(e){
        e.preventDefault();
        $('.image_uploading').fadeIn('fast');
        var options = {
            url:"/api/profile/avatar",
            type:"POST",
            headers:{
                "X-XSRFTOKEN":getCookie("_xsrf"),
            },
            success: function(data){
                if ("0" == data.errno) {
                    $('.image_uploading').fadeOut('fast');
                    $("#user-avatar").attr("src", data.url);
                }
            }
        };
        $(this).ajaxSubmit(options);
    });
    // update user_name
    $("#form-name").submit(function(e){
        e.preventDefault();
        // $('.image_uploading').fadeIn('fast');
        var options = {
            url:"/api/profile/username",
            type:"POST",
            headers:{
                "X-XSRFTOKEN":getCookie("_xsrf"),
            },
            success: function(data){
                if ("0" == data.errno) {
                    // $('.image_uploading').fadeOut('fast');
                    $('save_success').fadeIn('fast');
                    location.href = "/my.html";
                }
                else {
                    $('.error-msg').show();
                }
            }
        };
        $(this).ajaxSubmit(options);
        $('#user-name').focus(function(){
            $('.error-msg').hide();
        });
    });   
})