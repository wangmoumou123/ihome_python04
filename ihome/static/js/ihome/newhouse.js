function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');
    $.get('/api/v1.0/areas', function (ret) {
        if (ret.errno === '0') {
            //成功获取房源
            var areas_list = ret.areas;
            // for (i = 0; i < areas_list.length; i++) {
            //     area = areas_list[i]
            //     $('#area-id').append('<option value="'+area.aid+'">'+area.aname+'</option>\n')
            // }
            // 使用art-模板变量
            var html = template('area-temp', {areass: areas_list});
            $('#area-id').html(html);

        } else {
            //获取失败
            alert(ret.errmsg)
        }


    });
    $('#form-house-info').submit(function (e) {
        // 阻止默认提交
        e.preventDefault();
        // 获取表单所有数据, 用map转换为字典
        var house_info_dict = {};
        $('#form-house-info').serializeArray().map(function (x) {
            house_info_dict[x.name] = x.value;
        });
        // 生成facility的id列表
        var facility_ids_list = [];
        $(":checked[name='facility']").each(function (index, x) {
            facility_ids_list[index] = $(x).val()
        });
        // 重新设置字典中的facility
        house_info_dict.facility = facility_ids_list;
        // alert(11)
        // 发起ajax请求
        $.ajax({
            url: '/api/v1.0/newhouse',
            type: 'post',
            dataType: 'json',
            data: JSON.stringify(house_info_dict),
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': getCookie('csrf_token')
            },
            success: function (data) {
                if (data.errno === '4102') {
                    // 用户未登陆
                    location.href = '/login.html';
                } else if (data.errno === '0') {
                    // 提交信息成功
                    // 隐藏房屋信息鸟蛋， 显示上传图片表单
                    $('#form-house-info').hide();
                    $('#form-house-image').show();
                    //设置house_id
                    $('#house-id').val(data.data.house_id)

                } else {
                    // 失败
                    alert(data.errmsg)
                }

            }
        })
    });
    $('#form-house-image').submit(function (e) {
        e.preventDefault();
        $(this).ajaxSubmit({
            url: '/api/v1.0/newhouse_image',
            type: 'post',
            dataType: 'json',
            headers: {
                'X-CSRFToken': getCookie('csrf_token')
            },
            success: function (data) {
                if (data.errno === '4102') {
                    location.href = '/login.html'
                } else if (data.errno === '0') {
                    //成功
                    $('.house-image-cons').append('<img src="'+data.data.image_url+'">')
                }

            }
        })

    })

});