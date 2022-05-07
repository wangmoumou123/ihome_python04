function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function logout() {
    $.ajax({
        url: '/api/v1.0/logout',
        method: 'delete',
        dataType: 'json',
        contentType: 'application/json',
        headers: {
            'X-CSRFToken': getCookie('csrf_token')
        },
        success: function (data) {
            if (data.errno === '0') {
                //ok
                location.href = '/index.html';
                location.href = '/index.html'

            }

        }
    })
}

$(document).ready(function () {
    $.get('/api/v1.0/my', function (data) {
        if (data.errno === '0') {
            //成功
            user_name = data.data.name;
            mobile = data.data.mobile;
            $('#user-name').html(user_name);
            $('#user-mobile').html(mobile);
            $('#user-avatar').attr('src', data.data.avatar)
        }
    })
})