#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/6/24 9:37
"""
定义所有需要用到的表结构
"""
from datetime import datetime

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from passlib.apps import custom_app_context

db = SQLAlchemy()


class User(db.Model):
    """
    用户表结构
    """
    __tablename__ = 'iy_user'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, comment='主键')
    username = db.Column(db.String(64), index=True, unique=True, comment='用户名')
    name = db.Column(db.String(64), comment='真实姓名')
    password = db.Column(db.String(128), comment='密码，加密保存')
    email = db.Column(db.String(120), index=True, unique=True, comment='注册邮箱')
    location = db.Column(db.String(64), comment='居住地')
    about_me = db.Column(db.Text(), comment='关于')
    create_date = db.Column(db.DateTime(), default=datetime.utcnow, comment='用户创建时间')
    last_login = db.Column(db.DateTime(), default=datetime.utcnow, comment='最近登录时间')
    confirmed = db.Column(db.Boolean, default=False, comment='注册确认')
    avatar_hash = db.Column(db.String(32), comment='头像')

    def __repr__(self):
        return '<User %r>' % self.username

    def hash_password(self, password):
        """
        密码加密
        :param password:原始密码
        :return:
        """
        self.password = custom_app_context.encrypt(password)
        return self.password

    def verify_password(self, password):
        """
        验证密码
        :param password:str,原始密码
        :return:bool
        """
        return custom_app_context.verify(password, self.password)

    def generate_auth_token(self, expiration=6000):
        """
        获取token，有效时间10min
        :param expiration:
        :return:
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        """
        使用token方式认证，解析token，确认登录的用户身份
        :param token:
        :return:
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        # 根据id查询，查到则认证通过，否则校验失败
        user = User.query.get(data['id'])
        print('-----verify_auth_token------',user)
        return user