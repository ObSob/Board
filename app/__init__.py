from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib import sqla
import config


app = Flask(__name__)
app.config.from_object(config.Config)
db = SQLAlchemy(app)
admin = Admin(app, name='Admin', template_mode='bootstrap3')


# 一定要放在后面，不然会（循环引入？！）
from app import views
from app import models
from app import administer

# admin.add_view(administer.MyView(name='hello'))
admin.add_view(administer.UserView(db.session, name='User'))
admin.add_view(administer.MessageView(db.session, name='Message'))
