function hrefBack() {
    history.go(-1);
}

function decodeQuery() {
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function (result, item) {
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function () {
    //从参数中获取house_id
    var query_data = decodeQuery();
    var house_id = query_data['id'];
    // alert(house_id)


    $.get('/api/v1.0/newhouse/' + house_id, function (data) {
        // alert(222);
        if (data.errno == 0) {
            // alert(data.errmsg);
            // alert(22);
            //成功获取
            var house = data.data.house;
            //渲染页面
            //渲染图片滚动模板
            $('.swiper-wrapper').html(template('swiper_slide_temp', {images: house.image_urls}));
            var mySwiper = new Swiper('.swiper-container', {
                loop: true,
                autoplay: 2000,
                autoplayDisableOnInteraction: false,
                pagination: '.swiper-pagination',
                paginationType: 'fraction'
            });
            // 滚动条价格
            $('.house-price span').html(template('price_temp', {price: house.price}));

            // 细节详情
            $('.detail-con').html(template('detail_con_temp', {house: house}));

            //判断登录人是否是房主
            user_id = data.data.user_id;

            if (user_id === house.user_id) {
                //是房主本人
                $('.book-house').hide()

            } else {
                //不是本人

                $('.book-house').show();
                $('.book-house').attr('href', '/booking.html?hid=' + house_id);


            }
        } else {
            // 失败
            alert(data.errmsg)
        }

    });


    // $(".book-house").hide();

})