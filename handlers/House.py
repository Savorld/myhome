import logging

from BaseHandler import BaseHandler
from utils.common import require_logined
from utils.response_code import RET


class MyHouseHandler(BaseHandler):
    '''处理房屋信息'''
    @require_logined
    def get(self):
        user_id = self.session.data['user_id']
        sql = 'select up_real_name, up_id_card from ih_user_profile where up_user_id=%s'
        try:
            ret = self.db.execute(sql, user_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR, errmsg='数据查询出错！'))
        if not(ret['up_real_name'] and ret['up_id_card']:
            return self.write(dict(errno=RET.NODATA, errmsg='没有查到数据'))
        return self.write(dict(errno=RET.OK), errmsg='用户已通过实名认证')
