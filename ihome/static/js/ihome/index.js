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

function setStartDate() {
    var startDate = $("#start-date-input").val();
    if (startDate) {
        $(".search-btn").attr("start-date", startDate);
        $("#start-date-btn").html(startDate);
        $("#end-date").datepicker("destroy");
        $("#end-date-btn").html("离开日期");
        $("#end-date-input").val("");
        $(".search-btn").attr("end-date", "");
        $("#end-date").datepicker({
            language: "zh-CN",
            keyboardNavigation: false,
            startDate: startDate,
            format: "yyyy-mm-dd"
        });
        $("#end-date").on("changeDate", function () {
            $("#end-date-input").val(
                $(this).datepicker("getFormattedDate")
            );
        });
        $(".end-date").show();
    }
    $("#start-date-modal").modal("hide");
}

function setEndDate() {
    var endDate = $("#end-date-input").val();
    if (endDate) {
        $(".search-btn").attr("end-date", endDate);
        $("#end-date-btn").html(endDate);
    }
    $("#end-date-modal").modal("hide");
}

function goToSearchPage(th) {
    var url = "/search.html?";
    url += ("aid=" + $(th).attr("area-id"));
    url += "&";
    var areaName = $(th).attr("area-name");
    if (undefined == areaName) areaName = "";
    url += ("aname=" + areaName);
    url += "&";
    url += ("st=" + $(th).attr("start-date"));
    url += "&";
    url += ("et=" + $(th).attr("end-date"));
    location.href = url;
}

$(document).ready(function () {
    $.get('/api/v1.0/check_login', function (data) {
        if (data.errno === '0') {
            //已经登录
            $('.top-bar .user-info .user-name').text(data.data.name);
            $(".top-bar>.user-info").show();
        } else {
            $(".top-bar>.register-login").show();

        }

    });
    $.get('/api/v1.0/index_image', function (data) {
        if (data.errno === '0') {
            //成功
            var houses = data.data;
            // 渲染模板
            $('.swiper-wrapper').html(template('swiper_wrapper_temp', {houses: houses}))
            var mySwiper = new Swiper('.swiper-container', {
                loop: true,
                autoplay: 2000,
                autoplayDisableOnInteraction: false,
                pagination: '.swiper-pagination',
                paginationClickable: true
            });
        } else {
            // 失败
            alert(data.errmsg)
        }

    });
    // 获取城区列表
    $.get('/api/v1.0/areas', function (data) {
        if (data.errno === '0') {
            // 成功
            areas = data.areas;
            for (i = 0; i < areas.length; i++) {
                area_id = areas[i].aid;
                area_name = areas[i].aname;
                $('.area-list').append(' <a href="#" area-id="' + area_id + '">' + area_name + '</a>')
                // 点击事件

                $(".area-list a").click(function (e) {
                    $("#area-btn").html($(this).html());
                    $(".search-btn").attr("area-id", $(this).attr("area-id"));
                    $(".search-btn").attr("area-name", $(this).html());
                    $("#area-modal").modal("hide");
                });
            }
        } else {
            //失败
            alert(data.errmsg)
        }

    });

    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);               //当窗口大小变化的时候
    $("#start-date").datepicker({
        language: "zh-CN",
        keyboardNavigation: false,
        startDate: "today",
        format: "yyyy-mm-dd"
    });
    $("#start-date").on("changeDate", function () {
        var date = $(this).datepicker("getFormattedDate");
        $("#start-date-input").val(date);
    });
})