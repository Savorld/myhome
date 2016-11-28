# coding:utf-8

import logging

from .BaseHandler import BaseHandler
from utils.image_storage import storage
from utils.common import require_logined
from utils.response_code import RET
from config import image_url_prefix


class AvatarHandler(BaseHandler):
    """头像"""
    @require_logined
    def post(self):
        user_id = self.session.data["user_id"]
        try:
            avatar = self.request.files["avatar"][0]["body"]
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.PARAMERR, errmsg="参数错误"))
        try:
            img_name = storage(avatar)
        except Exception as e:
            logging.error(e)
            img_name = None
        if not img_name:
            return self.write({"errno": RET.THIRDERR, "errmsg": "qiniu error"})
        try:
            ret = self.db.execute(
                "update ih_user_profile set up_avatar=%s where up_user_id=%s", img_name, user_id)
        except Exception as e:
            logging.error(e)
            return self.write({"errno": RET.DBERR, "errmsg": "upload failed"})
        img_url = image_url_prefix + img_name
        self.write({"errno": RET.OK, "errmsg": "OK", "url": img_url})


class UserNameHandler(BaseHandler):
    '''Update Username'''
    @require_logined
    def post(self):
        user_id = self.session.data["user_id"]
        print([user_id])
        user_name = self.get_argument('name')
        print('1')
        try:
            print('2')
            self.db.execute(
                "update ih_user_profile set up_name=%s where up_user_id=%s", user_name, user_id)
        except Exception as e:
            print('3')
            logging.error(e)
            return self.write({"errno": RET.DBERR, "errmsg": "upload failed"})
        print('4')
        self.write({"errno": RET.OK, "errmsg": "OK"})


class ProfileHandler(BaseHandler):
    '''get user_info'''
    @require_logined
    def get(self):
        user_id = self.session.data['user_id']
        try:
            ret = self.db.get(
                'select up_name, up_mobile, up_avatar from ih_user_profile where up_user_id=%s' % user_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR, errmsg='DB query failed'))
        if ret['up_avatar']:
            img_url = image_url_prefix + ret['up_avatar']
        else:
            img_url = None
        self.write({"errno": RET.OK, "errmsg": "OK", "data": {"name": ret[
                   'up_name'], "mobile": ret['up_mobile'], "avatar": img_url}})


class AuthHandler(BaseHandler):
    '''check real_name'''
    @require_logined
    def get(self):
        user_id = self.session.data['user_id']
        try:
            ret = self.db.get(
                'select up_real_name, up_id_card from ih_user_profile where up_user_id=%s', user_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR, errmsg='query failed'))
        if not ret:
            ret = {}
        self.write(dict(errno=RET.OK, errmsg='OK', data=dict(
            real_name=ret['up_real_name'], id_card=ret['up_id_card'])))

    @require_logined
    def post(self):
        user_id = self.session.data['user_id']
        real_name = self.json_args.get('real_name')
        id_card = self.json_args.get('id_card')
        if not real_name or not id_card:
            return self.write({"errno": RET.PARAMERR, "errmsg": "params error"})
        try:
            self.db.execute(
                'update ih_user_profile set up_real_name=%s, up_id_card=%s where up_user_id=%s', real_name, id_card, user_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR, errmsg='DB update failed'))
        self.write(dict(errno=RET.OK, errmsg='OK'))
