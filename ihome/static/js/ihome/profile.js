function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function () {
        setTimeout(function () {
            $('.popup_con').fadeOut('fast', function () {
            });
        }, 1000)
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {
    $('#form-avatar').submit(function (e) {
        e.preventDefault();
        $(this).ajaxSubmit({
                url: '/api/v1.0/upload_pict',
                type: 'post',
                dataType: 'json',
                headers: {
                    'X-CSRFToken': getCookie('csrf_token')
                },
                success: function (ret) {
                    if (ret.errno === '0') {
                        //成功
                        var pict_url = ret.data.avatar_url;
                        $('#user-avatar').attr('src', pict_url)
                    } else if (ret.errno === '4102') {
                        alert(ret.errmsg);
                        location.href = '/login.html'

                    } else {
                        //失败
                        alert(ret.errmsg)
                    }

                }

            }
        )
    });
    $('#form-name').submit(function (e) {
        e.preventDefault();
        username = $('#user-name').val();
        pattern = {username: username};
        pattern = JSON.stringify(pattern);
        $.ajax({
            url: '/api/v1.0/update_username',
            method: 'post',
            dataType: 'json',
            data: pattern,
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': getCookie('csrf_token')
            },
            success: function (ret) {
                if (ret.errno === '0') {
                    //成功更改
                    location.href = '/my.html'
                } else {
                    alert(ret.errmsg)
                }

            }
        })

    })
});
