# 认证蓝图：注册新用户、登录和注销视图

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app, jsonify, make_response
)

from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db
from itsdangerous import URLSafeTimedSerializer
import smtplib
import random

bp = Blueprint('auth', __name__, url_prefix='/auth')


def generate_verification_code():
    return str(random.randint(100000, 999999))


def send_verification_email(email, code):
    # verification_token = generate_verification_token(email)
    # verification_link = url_for('auth.verify_email', token=verification_token, _external=True)

    subject = "Your Verification Code"
    message = f"Your verification code is: {code}"
    with smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT']) as server:
        server.starttls()
        server.login(current_app.config['MAIL_USERNAME'],
                     current_app.config['MAIL_PASSWORD'])
        server.sendmail(current_app.config['MAIL_USERNAME'], email, f"Subject: {
                        subject}\n\n{message}")


# 注册视图
# 填写注册内容的表单页面
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('regUsername')
        password = data.get('regPwd')
        confirm_password = data.get('regRePwd')
        email = data.get('email')
        verification_code = data.get('verification_code')  # 用户输入的验证码
        sent_verification_code = data.get('sent_verification_code')  # 发送的验证码

        db = get_db()
        error = None

        # 验证必填字段
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not confirm_password:
            error = 'Password confirmation is required.'
        elif password != confirm_password:
            error = 'Passwords do not match.'
        elif not email:
            error = 'Email is required.'
        elif not verification_code:
            error = 'Verification code is required.'

        # 验证验证码是否正确
        if verification_code != sent_verification_code:
            error = 'Invalid verification code.'

        if error:
            return jsonify({"status": "error", "message": error}), 400

        # 检查用户名或邮箱是否已存在
        user_exists = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()
        email_exists = db.execute(
            "SELECT * FROM user WHERE email = ?", (email,)
        ).fetchone()

        if user_exists:
            error = f"Username {username} is already registered."
        elif email_exists:
            error = f"Email {email} is already registered."

        if error is None:
            try:
                # 将密码加密
                hashed_password = generate_password_hash(password)
                # 插入用户数据到数据库
                db.execute(
                    "INSERT INTO user (username, email, password, is_verified) VALUES (?, ?, ?, ?)",
                    (username, email, hashed_password, 1)  # 默认已验证
                )
                db.commit()

                return jsonify({"status": "success", "message": "Registration successful! Please verify your email."}), 200
            except db.IntegrityError:
                error = "An unexpected error occurred."

        return jsonify({"status": "error", "message": error}), 400


# 忘记密码视图
@bp.route('/forgot_password', methods=('GET', 'POST'))
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        db = get_db()
        user = db.execute(
            'SELECT * FROM user WHERE username = ? AND email = ?', (username, email)).fetchone()

        if user:
            # 用户名和邮箱验证通过，保存邮箱信息用于后续验证
            session['user_email'] = email
            # 跳转到验证码验证页面
            return redirect(url_for('auth.verify_forgot_password'))
        else:
            flash('Invalid username or email.')

    return render_template('auth/forgot_password.html')


@bp.route('/verify_forgot_password', methods=('GET', 'POST'))
def verify_forgot_password():
    if 'user_email' not in session:
        flash('Session expired. Please try again.')
        return redirect(url_for('auth.forgot_password'))

    # 当用户首次访问该页面时，生成并发送验证码
    if request.method == 'GET':
        verification_code = generate_verification_code()  # 生成六位验证码
        session['verification_code'] = verification_code
        send_verification_email(
            session['user_email'], verification_code)  # 发送验证码
        flash('A verification code has been sent to your email.')
    if request.method == 'POST':
        entered_code = request.form['verification_code']
        if entered_code == session.get('verification_code'):
            session.pop('verification_code', None)  # 验证成功后清除验证码
            return redirect(url_for('auth.reset_password'))  # 验证通过，跳转到修改密码页面
        else:
            flash('Invalid verification code. Please try again.')

    return render_template('auth/verify_registration.html')


# 在每个视图中都可以完成的
# 登陆后，可进行创建、编辑和删除博客和帖子
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:  # 当前没有处于登录状态的用户，则要求登录
            return redirect(url_for('auth.login'))
        return view(**kwargs)  # 调用原始视图函数view，并返回视图的结果

    return wrapped_view  # 返回经过包装的视图函数


# 修改密码视图
@bp.route('/reset_password', methods=('GET', 'POST'))
def reset_password():
    if request.method == 'POST':
        new_password = request.form['new_password']
        new_password_check = request.form['new_password_check']
        if new_password_check == new_password:
            email = session.get('user_email')
            db = get_db()
            db.execute('UPDATE user SET password = ? WHERE email = ?',
                       (generate_password_hash(new_password), email))
            db.commit()
            flash('Your password has been reset successfully!')
            # 如果用户已登录，跳转到主页，否则跳转到登录页面
            if g.user:
                return redirect(url_for('index'))
            else:
                return redirect(url_for('auth.login'))
        else:
            flash('Inconsistent passwords. Please set again.')

    return render_template('auth/reset_password.html')


@bp.route('/send_verification_code', methods=['POST'])
def send_verification_code():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"status": "error", "message": "Email is required."}), 400

    # 生成并发送验证码
    verification_code = generate_verification_code()
    send_verification_email(email, verification_code)

    # 在响应中返回验证码作为 URL 参数
    return jsonify({
        "status": "success",
        "message": "Verification email sent.",
        "verification_code": verification_code  # 返回验证码
    }), 200


'''
@bp.route('/verify_registration', methods=('POST',))
def verify_registration():
    data = request.get_json()  # 从前端接收 JSON 数据
    email = data.get('email')
    verification_code = data.get('verification_code')

    # 验证必填字段是否存在
    if not all([email, verification_code]):
        return jsonify({"status": "error", "message": "Email and verification code are required."}), 400

    # 检查验证码是否正确
    if verification_code == session.get('verification_code'):
        # 清除会话中的验证码信息
        session.pop('verification_code', None)
        return jsonify({"status": "success", "message": "Verification successful!"}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid verification code."}), 400
'''


@bp.route('/login', methods=('POST',))
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        # 初始化响应对象
        response = {}

        db = get_db()
        error = None
        # 检查用户是否是普通用户
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()  # 根据查询返回一个记录行

        if user is None:  # 如果普通用户不存在，检查管理员
            admin = db.execute(
                'SELECT * FROM admin WHERE username = ?', (username,)
            ).fetchone()
            if admin is None:  # 管理员也不存在
                error = 'Incorrect username.'
            elif not check_password_hash(admin['password'], password):  # 管理员密码错误
                error = 'Incorrect password.'
            else:
                # 管理员登录成功，存储管理员的会话信息
                session.clear()
                session['admin_id'] = admin['id']
                response = {"status": "success", "role": "admin",
                            "message": "Admin logged in successfully"}
                return jsonify(response), 200
        else:
            # 普通用户登录
            if not check_password_hash(user['password'], password):  # 匹配密码
                error = 'Incorrect password.'
            elif not user['is_verified']:  # 检查用户是否验证
                error = 'Please verify your email address before logging in.'
            else:
                # 用户登录成功
                session.clear()
                session['user_id'] = user['id']
                response = {"status": "success", "role": "user",
                            "message": "User logged in successfully"}
                return jsonify(response), 200

        # 登录失败返回错误信息
        response['status'] = 'error'
        response['message'] = error
        return jsonify(response), 400


# 加载已登录的用户
# 在视图函数（不论其对应的url）之前运行的函数，用于检查用户id是否已经存储在session中，并从数据库中获取用户数据，存储在g.user中。
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    print(f"Session user_id: {user_id}")
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
    # 如没有user_id或id不存在，则g.user为None


# 注销
# 将某已登录的用户id从session中移除
@bp.route('/logout', methods=('POST',))
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200


# 管理员视图,确保只有管理员用户才能访问 admin_dashboard 页面。
@bp.route('/admin_dashboard', methods=['GET'])
def admin_dashboard():
    '''
    if 'admin_id' not in session:
        return redirect(url_for('auth.login'))
    '''
    # 管理员的其他页面逻辑
    return render_template('admin/dashboard.html')
