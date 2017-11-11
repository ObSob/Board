from flask_admin.contrib import sqla
from flask_admin import BaseView, expose
from flask import session as s, url_for
from app.models import User, Message
from config import Config
import os


class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')

    @expose('/admin/', methods=['GET', 'POST'])
    def check(self, name):
        if self.is_admin(name):
            return self.render('admin/index.html')
        else:
            pass

    def is_admin(self, name):
        return name == os.environ['ADMIN']


class UserView(sqla.ModelView):
    # Disable model creation
    can_create = False

    column_list = ('id', 'username', 'email')

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(UserView, self).__init__(User, session, **kwargs)

    def is_accessible(self):
        if s.get('known'):
            name = s.get('username')
            if name == Config.ADMIN:
                return True
            else:
                return False
        return False


class MessageView(sqla.ModelView):
    can_create = False

    column_list = ('id', 'title', 'text', 'pub_date', 'user_id')

    column_searchable_list = ('id', 'title', 'text', 'pub_date', 'user_id')

    def __init__(self, session, **kwargs):
        super(MessageView, self).__init__(Message, session, **kwargs)

    def is_accessible(self):
        if s.get('known'):
            name = s.get('username')
            if name == Config.ADMIN:
                return True
            else:
                return False
        return False
