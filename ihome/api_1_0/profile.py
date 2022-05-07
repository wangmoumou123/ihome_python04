# coding:utf-8

from . import api
from ihome import db, constants
from flask import current_app, jsonify, g, request, session
from ihome.utils.commons import login_required
from ihome.utils.image_storage import storage
from ihome.utils.captcha.response_code import RET
from ihome.models import User
import datetime


# 上传以及修改头像接口
@api.route('/upload_pict', methods=['POST'])
@login_required
def upload_pict():
    """
    上传头像到七牛
    :return:
    """
    # 接收参数 id pict
    # 从g变量取出user_id
    user_id = g.user_id
    pic_name_time = datetime.datetime.now().strftime("%Y-%m-%d%I:%M:%S%p")

    pict = request.files.get('avatar')
    # 检验
    # 检验pict是否存在
    if pict is None:
        return jsonify(errno=RET.NODATA, errmsg='没有上传头像文件')
    # 处理
    # 上传到七牛
    pict_data = pict.read()
    # print pict


    try:
        p_url = storage(pict_data, pic_name_time)
    except Exception as ret:
        current_app.logger.error(ret)
        return jsonify(errno=RET.THIRDERR, errmsg='第三方错误')

    # 查询user并更新url
    try:
        User.query.filter_by(id=user_id).update({'avatar_url': p_url})
        db.session.commit()
    except Exception as ret:
        # 失败 数据库回滚
        db.session.rollback()
        current_app.logger.error(ret)
        return jsonify(errno=RET.DBERR, errmsg='数据库错误')
    # 返回头像url
    avatar_url = constants.QINIU_ADDRESS + p_url
    return jsonify(errno=RET.OK, errmsg='上床头像成功', data={'avatar_url': avatar_url})


# 修改用户名
@api.route('/update_username', methods=['POST'])
@login_required
def update_username():
    # 获取参数
    # 从g变量获取user_id
    user_id = g.user_id
    # 获取new_username
    req_dict = request.get_json()
    new_username = req_dict.get('username')
    print (new_username)
    # 检验username是否存在
    if new_username is None:
        return jsonify(errno=RET.NODATA, errmsg='没有输入新的用户名')
    # 查找user并更新username
    try:
        user_instance = User.query.filter_by(name=new_username).first()
        if user_instance is not None:
            return jsonify(errno=RET.DATAERR, errmsg='用户名已存在')
        else:
            user = User.query.filter_by(id=user_id).first()
            user.name = new_username
            # User.query.filter_by(id=user_id).update({'name': new_username})
            db.session.commit()
    except Exception as ret:
        # 异常回退
        db.session.rollback()
        current_app.logger.error(ret)
        return jsonify(errno=RET.DBERR, errmsg='设置用户名失败')

    # 保存登录session
    session['name'] = user.name
    session['mobile'] = user.mobile
    session['user_id'] = user.id

    # 成功设置 返回
    return jsonify(errno=RET.OK, errmsg='设置用户名成功')


# my.html接口
@api.route('/my')
@login_required
def my():
    # 接收参数
    user_id = g.user_id
    user = User.query.filter_by(id=user_id).first()
    name = user.name
    mobile = user.mobile
    user_avatar = constants.QINIU_ADDRESS + user.avatar_url if user.avatar_url else ''
    return jsonify(errno=RET.OK, errmsg='已经登录', data={'name': name, 'mobile': mobile, 'avatar': user_avatar})


# 实名认证接口
@api.route('/real_authentication', methods=['POST'])
@login_required
def real_authentication():
    # 获取参数
    user_id = g.user_id
    # 查询是否已经实名认证
    try:
        user = User.query.filter_by(id=user_id).first()
    except Exception as ret:
        current_app.logger.error(ret)
    else:
        # 判断是否认证过
        # 已经实名认证
        if user.real_name and user.id_card is not None:
            return jsonify(errno=RET.OK, errmsg='已经实名认证',
                           data={'real_name': user.real_name, 'id_card': user.id_card})
        else:

            # 接受实名认证参数
            req_dict = request.get_json()
            real_name = req_dict.get('realname')
            id_card = req_dict.get('idcard')
            # 判断参数是否完全
            if not all([real_name, id_card]):
                return jsonify(errno=RET.NODATA, errmsg='请完善信息')
            # 进一步检验pass

            # 进行实名认证
            try:
                user.real_name = real_name
                user.id_card = id_card
                db.session.commit()
            except Exception as ret:
                db.session.rollback()
                current_app.logger.error(ret)
                return jsonify(errno=RET.DBERR, errmsg='认证失败')
        return jsonify(errno=RET.OK, errmsg='认证成功',
                       data={'real_name': user.real_name, 'id_card': user.id_card})


# 检测实名认证接口
# 实名认证接口
@api.route('/check_real_authentication', methods=['GET'])
@login_required
def check_real_authentication():
    # 获取参数
    user_id = g.user_id
    # 查询是否已经实名认证
    try:
        user = User.query.filter_by(id=user_id).first()
    except Exception as ret:
        current_app.logger.error(ret)
    else:
        # 判断是否认证过
        # 已经实名认证
        if user.real_name and user.id_card is not None:
            return jsonify(errno=RET.OK, errmsg='已经实名认证',
                           data={'real_name': user.real_name, 'id_card': user.id_card})
        else:
            return jsonify(errno=RET.ROLEERR, errmsg='没有实名认证')
