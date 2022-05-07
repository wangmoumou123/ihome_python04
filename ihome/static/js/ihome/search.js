function decodeQuery() {
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function (result, item) {
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function updateFilterDateDisplay() {
    var startDate = $("#start-date").val();
    var endDate = $("#end-date").val();
    var $filterDateTitle = $(".filter-title-bar>.filter-title").eq(0).children("span").eq(0);
    if (startDate) {
        var text = startDate.substr(5) + "/" + endDate.substr(5);
        $filterDateTitle.html(text);
    } else {
        $filterDateTitle.html("入住日期");
    }
}

// 定义页码

var next_page = 1;
var page = 1;
var total_page = 1;
var house_data_querying = false;


// 发起ajax请求函数
function search(how, aid_b) {

    //获取参数
    st = $('#start-date').val();
    et = $('#end-date').val();
    aid = $('.filter-area li.active').attr('area-id');
    if (!aid) {
        aid = aid_b
    }
    sk = $('.filter-sort li.active').attr('sort-key');
    if (how === 'new_page') {
        next_page = 1;
    }
    pattren = {
        st: st,
        et: et,
        aid: aid,
        sk: sk,
        p: next_page,
    };
    $.get('/api/v1.0/house_search', pattren, function (data) {
        if (data.errno === '0') {
            //成功
            house_li = data.data.house_li;
            houses_pages = data.data.houses_pages;
            total_page = houses_pages;
            //渲染模板
            if (houses_pages === 0) {
                //没有查询到
                $('.house-list').html('很抱歉，没有符合条件的房间')
            } else {
                if (how === 'new_page') {
                    page = 1;
                    $('.house-list').html(template('house_list_temp', {houses_li: house_li}))
                    house_data_querying = false;

                } else {
                    $('.house-list').append(template('house_list_temp', {houses_li: house_li}));
                    page = next_page;
                    house_data_querying = false;

                }
            }
        }
    })
}

$(document).ready(function () {
    // 获取城区列表
    $.get('/api/v1.0/areas', function (data) {
        if (data.errno === '0') {
            // 成功
            areas = data.areas;
            for (i = 0; i < areas.length; i++) {
                area_id = areas[i].aid;
                area_name = areas[i].aname;
                $('.filter-area').append(' <li area-id="' + area_id + '">' + area_name + '</li>')
                // 点击事件
                // alert(area_id)
            }
        } else {
            //失败
            alert(data.errmsg)
        }

    });
    //调用search


    var queryData = decodeQuery();
    var startDate = queryData["sd"];
    var endDate = queryData["ed"];
    var aid_b = queryData['aid'];
    // alert(aid);
    // alert($('.filter-area li.active').attr('area-id'));
    $("#start-date").val(startDate);
    $("#end-date").val(endDate);
    updateFilterDateDisplay();
    var areaName = queryData["aname"];
    // $(".filter-area li[area-id='" + aid + "']").hasClass("active");
    // alert($(".filter-area li.active").attr('area-id'));
    if (!areaName) areaName = "位置区域";
    $(".filter-title-bar>.filter-title").eq(1).children("span").eq(0).html(areaName);
    //更新页面， 从第一页开始
    //传入地区new, aid_b
    search('new_page', aid_b);


    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    var $filterItem = $(".filter-item-bar>.filter-item");
    $(".filter-title-bar").on("click", ".filter-title", function (e) {
        var index = $(this).index();
        if (!$filterItem.eq(index).hasClass("active")) {
            $(this).children("span").children("i").removeClass("fa-angle-down").addClass("fa-angle-up");
            $(this).siblings(".filter-title").children("span").children("i").removeClass("fa-angle-up").addClass("fa-angle-down");
            $filterItem.eq(index).addClass("active").siblings(".filter-item").removeClass("active");
            $(".display-mask").show();
        } else {
            $(this).children("span").children("i").removeClass("fa-angle-up").addClass("fa-angle-down");
            $filterItem.eq(index).removeClass('active');
            $(".display-mask").hide();
            updateFilterDateDisplay();
        }
    });
    $(".display-mask").on("click", function (e) {
        $(this).hide();
        $filterItem.removeClass('active');
        updateFilterDateDisplay();
        //修改筛选条件调用search
        search('new_page');


    });
    $(".filter-item-bar>.filter-area").on("click", "li", function (e) {
        if (!$(this).hasClass("active")) {
            $(this).addClass("active");
            $(this).siblings("li").removeClass("active");
            $(".filter-title-bar>.filter-title").eq(1).children("span").eq(0).html($(this).html());
        } else {
            $(this).removeClass("active");
            $(".filter-title-bar>.filter-title").eq(1).children("span").eq(0).html("位置区域");
        }
    });
    $(".filter-item-bar>.filter-sort").on("click", "li", function (e) {
        if (!$(this).hasClass("active")) {
            $(this).addClass("active");
            $(this).siblings("li").removeClass("active");
            $(".filter-title-bar>.filter-title").eq(2).children("span").eq(0).html($(this).html());
        }
    });

    // var windowHeight = $(window).height();
    // 为窗口的滚动添加事件函数
    // window.onscroll = function () {
    //     // var a = document.documentElement.scrollTop==0? document.body.clientHeight : document.documentElement.clientHeight;
    //     var b = document.documentElement.scrollTop == 0 ? document.body.scrollTop : document.documentElement.scrollTop;
    //     var c = document.documentElement.scrollTop == 0 ? document.body.scrollHeight : document.documentElement.scrollHeight;
    //     // 如果滚动到接近窗口底部
    //     if (c - b < windowHeight + 50) {
    //         // 如果没有正在向后端发送查询房屋列表信息的请求
    //         if (!house_data_querying) {
    //             // 将正在向后端查询房屋列表信息的标志设置为真
    //             house_data_querying = true;
    //             // 如果当前页面数还没到达总页数
    //             if (page <= total_page) {
    //                 // 将要查询的页数设置为当前页数加1
    //                 next_page = page + 1;
    //                 // 向后端发送请求，查询下一页房屋数据// 向后端发送请求，查询下一页房屋数据
    //                 search();
    //             } else {
    //                 house_data_querying = false;
    //             }
    //         }
    //     }
    // }


    $(window).scroll(function () {
        var scrollTop = $(this).scrollTop();
        var scrollHeight = $(document).height();
        var windowHeight = $(this).height();
        if (scrollHeight - scrollTop - windowHeight <= 50) {
            if (!house_data_querying) {
                // 将正在向后端查询房屋列表信息的标志设置为真
                house_data_querying = true;
                // alert(page);
                // 如果当前页面数还没到达总页数
                if (page < total_page) {
                    // 将要查询的页数设置为当前页数加1
                    next_page = page + 1;
                    // 向后端发送请求，查询下一页房屋数据// 向后端发送请求，查询下一页房屋数据
                    search();
                    // alert(total_page);
                    // alert(next_page)

                } else {
                    house_data_querying = true;
                    $('.end_search').show()
                }
            }
            //当滚动条滚动到距离底部还有50px的时候加载类容
        }
        // });


    });
})