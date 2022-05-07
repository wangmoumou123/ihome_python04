$(document).ready(function () {
    //判断用户是否登录
    // 判断是否是经认证过
    $.get('/api/v1.0/check_real_authentication', function (data) {
        if (data.errno === '4102') {
            //未登录
            location.href = '/login.html'
        } else if (data.errno === '0') {
            //已经认证过
            $('.new-house a').attr('src', '/newhouse.html');
            // 请求之前发布的房源信息
            $.get('api/v1.0/my_house', function (data) {
                if (data.errno === '0') {
                    //请求成功
                    // alert(111)
                    var houses = data.data.houses;
                    // alert(houses[0].title)
                    $('#houses-list').html(template('house_list_temp', {houses: houses}))

                } else {
                    //请求失败
                    $('#houses-list').html(template('house_list_temp', {houses: ''}));

                    alert(data.errmsg)
                }

            })
        } else {
            //没有实名认证
            $(".auth-warn").show();

        }

    })
});

