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
}

$(document).ready(function () {
    $.get('api/v1.0/user_pay_check', function (data) {
        if (data.errno === '0') {
            $.get('api/v1.0/my_order', function (data) {
                if (data.errno === '0') {
                    //成功
                    //渲染模板
                    // alert(data.data.orders[0].status)
                    $('.orders-list').html(template('orders-list-tmpl', {orders: data.data.orders}))
                    // 模板渲染完毕 进行评论
                    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
                    $(window).on('resize', centerModals);
                    $(".order-comment").on("click", function () {
                        var orderId = $(this).parents("li").attr("order-id");
                        $(".modal-comment").attr("order-id", orderId);
                    });

                    //发起ajax请求
                    $(".modal-comment").on("click", function () {
                        // 点击确定接单
                        var order_id = $(this).attr("order-id");
                        // action = 'accept';
                        var comment = $("#comment").val();

                        partten = {'action': 'comment', 'comment': comment};
                        $.ajax({
                            url: '/api/v1.0/comment_order/' + order_id,
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
                                    $(".orders-list>li[order-id=" + order_id + "]>div.order-content>div.order-text>ul li:eq(4)>span").html("已完成");
                                    // 2. 隐藏接单和拒单操作
                                    $("ul.orders-list>li[order-id=" + order_id + "]>div.order-title>div.order-operate").hide();
                                    // 3. 隐藏弹出的框
                                    $("#comment-modal").modal("hide");
                                    // 拒单原因
                                    $(".orders-list>li[order-id=" + order_id + "]>div.order-content>div.order-text>ul").append('<li>我的评价：' + comment + '</li>');

                                } else {
                                    //失败
                                    alert(data.errmsg)
                                }

                            }
                        })
                    });

                    // 发起支付请求
                    $('.order-payment').click(function () {
                        // 获取orders_id
                        order_id = $(this).parents('li').attr('order-id');
                        // alert(order_id);
                        $.ajax({
                            url: '/api/v1.0/order_pay/' + order_id,
                            type: 'post',
                            dataType: 'json',
                            headers: {
                                'X-CSRFToken': getCookie('csrf_token')
                            },
                            success: function (data) {
                                if (data.errno === '0') {
                                    //成功
                                    location.href = data.data.order_pay_url;

                                } else if (data.errno === '4102') {
                                    alert(data.errmsg);
                                    location.href = '/login.html'

                                } else {
                                    //失败
                                    alert(data.errmsg)
                                }

                            }

                        })

                    })


                } else if (data.errno === '4001') {
                    $('.orders-list').html('暂时没有订单')

                } else {
                    alert(data.errmsg)

                }

            })
        }

    });


});