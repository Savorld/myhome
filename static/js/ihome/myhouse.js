$(document).ready(function() {
    $(".auth-warn").show();
    $.get('/api/house/my', function(data) {
        if ('4101' == data.errno) {
            location.href = '/login.html';
        } else if ('0' == data.errno) {
            $('.auth-warn').hide();
            $('#houses-list').hide();

        } else {
            $('.auth-warn').show();
            $('#houses-list').hide();
        }

    });
});
