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

function authen1() {


    var realname = $('#real-name').val();
    var idcard = $('#id-card').val();
    partten = {realname: realname, idcard: idcard};
    partten = JSON.stringify(partten);

    $.ajax({
        url: '/api/v1.0/real_authentication',
        type: 'post',
        dataType: 'json',
        data: partten,
        contentType: 'application/json',
        headers: {
            'X-CSRFToken': getCookie('csrf_token')
        },
        success: function (ret) {
            if (ret.errno === '0' | ret.errno === '4003') {
                //认证成功
                // alert(ret.data.real_name)
                $('#real-name').val(ret.data.real_name);
                $('#id-card').val(ret.data.id_card);
                $('#real-name').attr('disabled', 'disabled');
                $('#id-card').attr('disabled', 'disabled');
                $('.btn-success').hide()

            }
        }

    })


};

function authen2() {


    var realname = $('#real-name').val();
    var idcard = $('#id-card').val();
    partten = {realname: realname, idcard: idcard};
    partten = JSON.stringify(partten);

    $.ajax({
        url: '/api/v1.0/real_authentication',
        type: 'post',
        dataType: 'json',
        data: partten,
        contentType: 'application/json',
        headers: {
            'X-CSRFToken': getCookie('csrf_token')
        },
        success: function (ret) {
            if (ret.errno === '0') {
                //认证成功
                $('#real-name').val(ret.data.real_name);
                $('#id-card').val(ret.data.id_card);
                $('#real-name').attr('disabled', 'disabled');
                $('#id-card').attr('disabled', 'disabled');
                $('.btn-success').hide()
            } else {
                //认证失败
                alert(ret.errmsg)
            }

        }

    })


};


$(document).ready(function () {
    authen1();
    // $('.btn-success').click(function () {
    //     authen();

    // })
    $('#form-auth').submit(function (e) {
        e.preventDefault();
        authen2()

    })


});