//模态框居中的控制
function centerModals() {
    $('.modal').each(function (i) {   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top - 30);  //修正原先已经有的30个像素
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
};


$(document).ready(function () {


    pattern = {'role': 'master'};
    $.get('api/v1.0/my_order', pattern, function (data) {
        if (data.errno === '0') {
            //成功
            //渲染模板
            // alert(32)
            // alert(data.data.orders[0].status)
            $('.orders-list').html(template('orders-list-tmpl', {orders: data.data.orders}))


            $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
            $(window).on('resize', centerModals);


            $(".order-accept").click(function () {
                var orderId = $(this).parents('li').attr("order-id");
                $(".modal-accept").attr("order-id", orderId);
            });
            // $('.orders-list li').each(function () {
            //     if ($(this).find('.the_status').html() != '待支付') {
            //         $("ul.orders-list>li[order-id=" + order_id + "]>div.order-title>div.order-operate").hide();
            //         // 3. 隐藏弹出的框
            //         $("#accept-modal").modal("hide");
            //     }
            //
            // })

            $(".modal-accept").on("click", function () {
                // 点击确定接单
                var order_id = $(this).attr("order-id");
                // action = 'accept';
                partten = {'action': 'accept'};
                $.ajax({
                    url: '/api/v1.0/reject_accept_order/' + order_id,
                    type: 'PUT',
                    dataType: 'json',
                    data: JSON.stringify(partten),
                    contentType: 'application/json',
                    headers: {
                        'X-CSRFTOKEN': getCookie('csrf_token')
                    },
                    success: function (data) {
                        if (data.errno === '0') {
                            // 1. 设置订单状态的html
                            $(".orders-list>li[order-id=" + order_id + "]>div.order-content>div.order-text>ul li:eq(4)>span").html("待支付");
                            // 2. 隐藏接单和拒单操作
                            $("ul.orders-list>li[order-id=" + order_id + "]>div.order-title>div.order-operate").hide();
                            // 3. 隐藏弹出的框
                            $("#accept-modal").modal("hide");
                        } else {
                            //失败
                            alert(data.errmsg)
                        }

                    }
                })
            });

            $(".order-reject").on("click", function () {
                var orderId = $(this).parents("li").attr("order-id");
                $(".modal-reject").attr("order-id", orderId);
            });

            //拒单
            $(".modal-reject").on("click", function () {
                // 点击确定接单
                var order_id = $(this).attr("order-id");
                // action = 'accept';
                var reason = $("#reject-reason").val()

                partten = {'action': 'reject', 'reason': reason};
                $.ajax({
                    url: '/api/v1.0/reject_accept_order/' + order_id,
                    type: 'PUT',
                    dataType: 'json',
                    data: JSON.stringify(partten),
                    contentType: 'application/json',
                    headers: {
                        'X-CSRFTOKEN': getCookie('csrf_token')
                    },
                    success: function (data) {
                        if (data.errno === '0') {
                            // 1. 设置订单状态的html
                            $(".orders-list>li[order-id=" + order_id + "]>div.order-content>div.order-text>ul li:eq(4)>span").html("已拒单");
                            // 2. 隐藏接单和拒单操作
                            $("ul.orders-list>li[order-id=" + order_id + "]>div.order-title>div.order-operate").hide();
                            // 3. 隐藏弹出的框
                            $("#reject-modal").modal("hide");
                            // 拒单原因
                            $(".orders-list>li[order-id=" + order_id + "]>div.order-content>div.order-text>ul").append('<li>拒单原因：' + reason + '</li>');

                        } else {
                            //失败
                            alert(data.errmsg)
                        }

                    }
                })
            });


        } else if (data.errno === '4102') {
            alert(data.errmsg);
            location.href = '/login.html'

        } else if (data.errno === '4001') {
            $('.orders-list').html('<h1>没有客户订单</h1>');

        } else {
            // 出错
            alert(data.errmsg)
        }

    });


});