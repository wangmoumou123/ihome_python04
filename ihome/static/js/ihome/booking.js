function hrefBack() {
    history.go(-1);
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function decodeQuery() {
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function (result, item) {
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function showErrorMsg() {
    $('.popup_con').fadeIn('fast', function () {
        setTimeout(function () {
            $('.popup_con').fadeOut('fast', function () {
            });
        }, 1000)
    });
}

$(document).ready(function () {
    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    $(".input-daterange").on("changeDate", function () {
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();

        if (startDate && endDate && startDate > endDate) {
            showErrorMsg();
        } else {
            var sd = new Date(startDate);
            var ed = new Date(endDate);
            days = (ed - sd) / (1000 * 3600 * 24) + 1;
            var price = $(".house-text>p>span").html();
            var amount = days * parseFloat(price);
            $(".order-amount>span").html(amount.toFixed(2) + "(共" + days + "晚)");
        }
    });
    //取出house_id
    var queryData = decodeQuery();
    var house_id = queryData['hid'];
    $.get('/api/v1.0/newhouse/' + house_id, function (data) {
        if (data.errno === 0) {
            //成功渲染模板
            $('.house-info').html(template('house_info_temp', {house: data.data.house}))
        } else {
            alert(data.errmsg)
        }

    });

    $('.submit-btn').click(function () {
        start_time = $('#start-date').val();
        end_time = $('#end-date').val();
        pattern = {house_id: house_id, start_time: start_time, end_time: end_time};
        $.ajax({
            url: '/api/v1.0/order',
            type: 'post',
            data: JSON.stringify(pattern),
            dataType: 'json',
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': getCookie('csrf_token')
            },
            success: function (data) {
                if (data.errno === '0') {
                    //成功
                    location.href = '/orders.html'
                } else if (data.errno === '4102') {
                    alert(data.errmsg);
                    location.href= '/login.html'

                } else {
                    //下单失败
                    alert(data.errmsg)
                }

            }
        })


    })
})
