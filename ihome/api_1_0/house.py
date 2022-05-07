# coding:utf-8

from . import api
from flask import jsonify, current_app, request, g, session
from ihome.models import Area, House, Facility, HouseImage, User, Order
from ihome.utils.commons import login_required
from ihome.utils.captcha.response_code import RET
from ihome import redis_store, constants, db
from ihome.utils.image_storage import storage
from datetime import datetime
import json


# 地区接口
@api.route('/areas', methods=['GET'])
def areas():
    """
    地区接口
    :return:地区id名字列表
    """
    # 尝试从redis中取出areas_info 等同与 resp_json
    try:
        areas_info = redis_store.get('areas_info')
    except Exception as ret:
        current_app.logger.error(ret)
    else:
        if areas_info is not None:
            # 从redis取出了地区
            current_app.logger.info('hit redis')
            return areas_info, 200, {'Content-Type': 'application/json'}
    # 没有命中redis
    try:
        areas_list = Area.query.all()
    except Exception as ret:
        current_app.logger.error(ret)
        return jsonify(errno=RET.DBERR, errmsg='数据库查询错误')
    # 创建地址字典列表
    areas_dict_list = list()
    for area in areas_list:
        areas_dict_list.append(area.to_dict())

    resp_dict = dict(errno=RET.OK, errmsg='获取地区成功', areas=areas_dict_list)
    # 转换为str
    resp_json = json.dumps(resp_dict)
    # 保存redis
    try:
        redis_store.setex('areas_info', constants.AREAS_REDIS_SAVE_TIME, resp_json)
    except Exception as ret:
        current_app.logger.error(ret)

    return resp_json, 200, {'Content-Type': 'application/json'}


# 发布新房源接口
@api.route('/newhouse', methods=['POST'])
@login_required
def newhouses():
    # 接收参数
    user_id = g.user_id
    house_data = request.get_json()
    title = house_data.get("title")  # 房屋名称标题
    price = house_data.get("price")  # 房屋单价
    area_id = house_data.get("area_id")  # 房屋所属城区的编号
    address = house_data.get("address")  # 房屋地址
    room_count = house_data.get("room_count")  # 房屋包含的房间数目
    acreage = house_data.get("acreage")  # 房屋面积
    unit = house_data.get("unit")  # 房屋布局(几室几厅)
    capacity = house_data.get("capacity")  # 房屋容纳人数
    beds = house_data.get("beds")  # 房屋卧床数目
    deposit = house_data.get("deposit")  # 押金
    min_days = house_data.get("min_days")  # 最小入住天数
    max_days = house_data.get("max_days")  # 最大入住天数

    # 验证参数是否完全
    if not all(
            [title, price, area_id, address, room_count, acreage, unit, capacity, beds, deposit, min_days, max_days]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数缺失')
    # 检验价格和押金
    try:
        price = int(float(price) * 100)
        deposit = int(float(deposit) * 100)
    except Exception as ret:
        current_app.logger.error(ret)
        return jsonify(errno=RET.DATAERR, errmsg='数据错误')

    # 检验房屋所属城区的编号
    try:
        area = Area.query.filter_by(id=area_id).first()
    except Exception as ret:
        current_app.logger.error(ret)
        return jsonify(errno=RET.DBERR, errmsg='数据库查询错误')

    # 创建房屋对象
    house = House(
        user_id=user_id,
        title=title,
        price=price,
        area_id=area_id,
        address=address,
        room_count=room_count,
        acreage=acreage,
        unit=unit,
        capacity=capacity,
        beds=beds,
        deposit=deposit,
        min_days=min_days,
        max_days=max_days
    )
    # 检验facility
    # 取出facility
    facility_ids = house_data.get('facility')
    if facility_ids:
        try:
            # 从Facility取出所有符合条件的
            facilities = Facility.query.filter(Facility.id.in_(facility_ids)).all()
        except Exception as ret:
            current_app.logger.error(ret)
            return jsonify(errno=RET.DBERR, errmsg='设施查询错误')
        else:
            if facilities:
                house.facilities = facilities
    # 保存数据库
    try:
        db.session.add(house)
        db.session.commit()
    except Exception as ret:
        # 回滚
        db.session.rollback()
        current_app.logger.error(ret)
        return jsonify(errno=RET.DBERR, errmsg='保存错误')
    # 成功 返回ok和 house_id
    return jsonify(errno=RET.OK, errmsg='成功', data={'house_id': house.id})


# new_house图片接口
@api.route('/newhouse_image', methods=['POST'])
@login_required
def newhouse_image():
    # 获取参数
    house_id = request.form.get('house_id')
    house_image = request.files.get('house_image')
    pic_name_time = datetime.now().strftime("%Y-%m-%d%I:%M:%S%p")
    # 判断参数是否完整
    if not all([house_id, house_image]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')
    # 判断house_id是否合法
    try:
        house = House.query.filter_by(id=house_id).first()
    except Exception as ret:
        current_app.logger.error(ret)
        return jsonify(errno=RET.DBERR, errmsg='数据库查询错误')
    if house is None:
        return jsonify(errno=RET.NODATA, errmsg='没有房屋')
    # 保存图片到七牛
    image_data = house_image.read()
    try:
        image_url = storage(image_data, pic_name_time)
    except Exception as ret:
        current_app.logger.error(ret)
        return jsonify(errno=RET.THIRDERR, errmsg='第三方错误')
    # 保存image_url到houseImage
    house_image = HouseImage(house_id=house_id, url=image_url)
    db.session.add(house_image)
    # 设置第一图片为house的index_image
    if not house.index_image_url:
        house.index_image_url = image_url
        db.session.add(house)

    # 提交
    try:
        db.session.commit()
    except Exception as ret:
        current_app.logger.error(ret)
        return jsonify(errno=RET.DBERR, errmsg='数据库保存失败')
    # 成功 返回url
    image_url = constants.QINIU_ADDRESS + image_url
    return jsonify(errno=RET.OK, errmsg='发布成功', data={'image_url': image_url})


# 我的房源接口
@api.route('/my_house', methods=['GET'])
@login_required
def my_house():
    # 接受user_id
    user_id = g.user_id
    # 查询数据库
    try:
        user = User.query.filter_by(id=user_id).first()
        houses = user.houses
    except Exception as ret:
        current_app.logger.error(ret)
        return jsonify(errno=RET.DBERR, errmsg='数据库查询错误')
    else:
        house_list = list()
        if houses:
            for house in houses:
                house_list.append(house.to_basic_dict())
        return jsonify(errno=RET.OK, errmsg='成功', data={'houses': house_list})


# index_image 接口
@api.route('/index_image', methods=['GET'])
def index_image():
    # 尝试取缓存
    try:
        houses_list_json = redis_store.get('index_images')
    except Exception as ret:
        current_app.logger.error(ret)
        houses_list_json = None
    # 取出缓存
    if houses_list_json:
        return '{"errno":"0","errmsg":"success","data":%s }' % houses_list_json, 200, {
            'Content-Type': 'application/json'}
    # 没有缓存
    else:
        # 取出数据
        try:
            houses = House.query.order_by(House.order_count.desc()).limit(constants.INDEX_HOME_PAGES_NUM)
        except Exception as ret:
            current_app.logger.error(ret)
            return jsonify(errno=RET.DBERR, errmsg='数据库错误')
        else:
            houses_list = list()
            if houses is not None:
                for house in houses:
                    # 如果未设置 跳过
                    if not house.index_image_url:
                        continue
                    houses_list.append(house.to_basic_dict())
            # 转换字符串
            houses_list_json = json.dumps(houses_list)
            # 保存redis
            redis_store.setex('index_images', constants.INDEX_REDIS_SAVE_TIME, houses_list_json)
            # 返回值
            return '{"errno":"0","errmsg":"success","data":%s }' % houses_list_json, 200, {
                'Content-Type': 'application/json'}


# 房屋详情接口
@api.route('/newhouse/<int:house_id>', methods=['GET'])
def newhousedetail(house_id):
    # 接收参数
    user_id = session.get('user_id', '-1')
    # 尝试从缓存读出数据
    try:
        house_info_json = redis_store.get('house_detail_info%s' % house_id)
    except Exception as ret:
        current_app.logger.error(ret)
        house_info_json = None
    if house_info_json:
        resp = '{"errno": 0, "errmsg": "success", "data":{"user_id":%s,"house":%s}}' % (user_id, house_info_json) \
            , 200, {'Content-Type': 'application/json'}
        return resp
    else:

        # 查询对应的房屋信息
        try:
            house = House.query.filter_by(id=house_id).first()
        except Exception as ret:
            current_app.logger.error(ret)
            return jsonify(errno=RET.DBERR, errmsg='数据库查询失败')
        # 该房屋信息转化为字典
        try:
            house_info_dict = house.to_full_dict()
        except Exception as ret:
            current_app.logger.error(ret)
            return jsonify(errno=RET.DBERR, errmsg='未查数据异常')
        # 转换json字符串
        house_info_json = json.dumps(house_info_dict)
        # 保存redis
        try:
            redis_store.setex('house_detail_info%s' % house_id, constants.INDEX_REDIS_SAVE_TIME, house_info_json)
        except Exception as ret:
            current_app.logger.error(ret)
            return jsonify(errno=RET.DBERR, errmsg='redis保存错误')
        # 返回值
        resp = '{"errno": 0, "errmsg": "success", "data":{"user_id":%s,"house":%s}}' % (user_id, house_info_json) \
            , 200, {'Content-Type': 'application/json'}
        return resp


# house_search接口
# GET: /api/v1.0/search_house?st=2020-2-6&et=2020-2-7&aid=2&sk=xx&p=5
@api.route('/house_search', methods=['GET'])
def house_search():
    # 接收参数
    start_time = request.args.get('st', '')
    end_time = request.args.get('et', '')
    area_id = request.args.get('aid', '')
    sort_key = request.args.get('sk', 'new')
    page = request.args.get('p')

    # 检验参数
    # 检验时间
    try:
        if start_time:
            start_time = datetime.strptime(start_time, '%Y-%m-%d')
        if end_time:
            end_time = datetime.strptime(end_time, '%Y-%m-%d')
        if start_time and end_time:
            assert start_time <= end_time
    except Exception as ret:
        current_app.logger.error(ret)
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完全')

    # 检验地区
    try:
        area = Area.query.filter_by(id=area_id).first()
    except Exception as ret:
        current_app.logger.error(ret)
        return jsonify(errno=RET.DBERR, errmsg='地区查询错误')

    # 检验页码
    if page:
        try:
            page = int(page)
        except Exception as ret:
            current_app.logger.error(ret)
            page = 1
    else:
        page = 1
    # 尝试从redis缓存中命中搜索
    try:
        keys = 'search_%s %s %s %s' % (start_time, end_time, area_id, sort_key)
        resp_json = redis_store.hget(keys, page)
    except Exception as ret:
        current_app.logger.error(ret)
    else:
        if resp_json:
            # redis 缓存命中
            return resp_json, 200, {'Content-Type': 'application/json'}

    # 初始化不符合订单
    orders = None
    # 初始化查询集
    filter_pattern = []

    # 先查询在冲突时间范围的house_id
    # 如果两个时间都传了
    try:
        if start_time and end_time:
            orders = Order.query.filter(Order.begin_date <= end_time, Order.end_date >= start_time).all()
        # 只传一个时间
        elif start_time:
            orders = Order.query.filter(Order.end_date >= start_time).all()
        elif end_time:
            orders = Order.query.filter(Order.begin_date <= end_time).all()
    except Exception as ret:
        current_app.logger.error(ret)
        return jsonify(errno=RET.DBERR, errmsg='数据库查询错误')

    # 创建查询条件集
    if orders:
        # 获取不符合的house_id
        un_houses_id = [order.house_id for order in orders]

        # 如果 un_houses_id不为空
        if un_houses_id:
            # 向查询集添加查询条件
            filter_pattern.append(House.id.notin_(un_houses_id))

    # 判断地区area_id
    if area_id:
        filter_pattern.append(House.area_id == area_id)

    # 检验排序方式
    if sort_key == 'booking':
        # 传入查询条件集和排序方式
        houses = House.query.filter(*filter_pattern).order_by(House.order_count.desc())
    elif sort_key == 'price-inc':
        houses = House.query.filter(*filter_pattern).order_by(House.price.asc())
    elif sort_key == 'price-des':
        houses = House.query.filter(*filter_pattern).order_by(House.price.desc())
    else:
        houses = House.query.filter(*filter_pattern).order_by(House.create_time.desc())

    try:
        # 处理分页
        houses = houses.paginate(page=page, per_page=constants.PER_PAGE_DATA, error_out=False)
    except Exception as ret:
        current_app.logger.error(ret)
        return jsonify(errno=RET.DBERR, errmsg='数据库查询错误')

    # 每页内容
    houses_per_page = houses.items
    # 转化为字典列表
    house_li = list()
    for house in houses_per_page:
        house_li.append(house.to_basic_dict())
    # 总页数
    houses_pages = houses.pages

    # 转换字典
    resp_dict = dict(errno=RET.OK, errmsg='success',
                     data={'house_li': house_li, 'houses_pages': houses_pages, 'current_page': page})
    # 转换json字符串
    resp_json = json.dumps(resp_dict)
    # 保存redis缓存
    try:
        keys = 'search_%s %s %s %s' % (start_time, end_time, area_id, sort_key)

        redis_store.hset(keys, page, resp_json)
        redis_store.expire(keys, constants.REDIS_SEARCH_CACHE_SAVE_TIME)
        # 使用redis.pipeline一次执行多条语句
        # pipeline = redis_store.pipeline
        # 开启多个语句
        # pipeline.multi()
        # pipeline.hset(keys, page, resp_json)
        # pipeline.expire(keys, constants.REDIS_SEARCH_CACHE_SAVE_TIME)
        # 执行语句
        # pipeline.execute()
    except Exception as ret:
        current_app.logger.error(ret)
        # return jsonify(errno=RET.DBERR, errmsg='缓存设置失败')

    # 返回数据
    return resp_json, 200, {'Content-Type': 'application/json'}
