function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function() {
            $('.popup_con').fadeOut('fast', function() {});
        }, 1000)
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(function() {
    $.get('/api/profile/auth', function(data) {
        if ('4101' == data.errno) {
            location.href = '/login.html';
        } else if ('0' == data.errno && data.data.real_name && data.data.id_card) {
            $('#real-name').val(data.data.real_name).prop('disabled', true);
            $('#id-card').val(data.data.id_card).prop('disabled', true);
            $('.btn-success').hide();
        }
    });

    $('#form-auth').submit(function(e) {
        e.preventDefault();
        if ($('#real_name').val() == '' || $('#id_card').val() == '') {
            $('.error-msg').show();
        }
        var data = {};
        $(this).serializeArray().map(function(x) {
            data[x.name] = x.value;
        });
        var jsonData = JSON.stringify(data);
        $.ajax({
            url: '/api/profile/auth',
            type: 'POST',
            data: jsonData,
            contentType: 'application/json',
            dataType: 'json',
            headers: {
                "X-XSRFTOKEN": getCookie("_xsrf"),
            },
            success: function(data) {
                if ('0' == data.errno) {
                    $('.error-msg').hide();
                    showSuccessMsg();
                    $('#real_name').prop('disable', true);
                    $('#id_card').prop('disable', true);
                    $('.btn-success').hide();
                }
            }
        });

    });
})
