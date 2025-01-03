from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from .auth import login_required, generate_verification_code, send_verification_email
from .db import get_db
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from flask import jsonify
import os

bp = Blueprint('profile', __name__, url_prefix='/profile')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
    # 如没有user_id或id不存在，则g.user为None


@bp.route('/', methods=('GET', 'POST'))
def view_profile():
    if g.user is None:
        return url_for('auth.login')
    db = get_db()
    user_id = g.user['id']
    # 从数据库中获取用户信息
    user = db.execute(
        'SELECT * FROM user WHERE id = ?', (user_id,)
    ).fetchone()

    # 获取所有标签
    user_tags = db.execute(
        'SELECT * '
        'FROM user_tags '
        'JOIN tags ON tags.id = user_tags.tag_id '
        'WHERE user_id = ?', (user_id,)).fetchall()
    tags_data = [dict(tag) for tag in user_tags]
    '''
    history = db.execute(
        'SELECT * '
        'FROM history h '
        'JOIN entry e ON e.entry_id = h.entry_id '
        'WHERE h.user_id = ? '
        'ORDER BY h.created DESC',
        (user_id,)
    ).fetchall()
    
    u_message = db.execute(
        'SELECT * '
        'FROM u_massage u '
        'WHERE u.user_id = ? '
        'ORDER BY u.created DESC ',
        (user_id,)
    )
    s_message = db.execute(
        'SELECT * '
        'FROM s_massage u '
        'WHERE u.user_id = ? '
        'ORDER BY u.created DESC ',
        (user_id,)
    )
    '''
    return jsonify({
        'user': dict(user),
        'user_tags': tags_data,
        # 'history': history,
        # 'u_message': u_message,
        # 'm_message': s_message
    })


@bp.route('/upload_avatar', methods=('POST',))
@login_required
def upload_avatar():
    user_id = g.user['id']
    if 'avatar' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['avatar']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = secure_filename(file.filename)
        avatar_path = os.path.join('uploads', 'avatars', filename)
        avatar_path = avatar_path.replace('\\', '/')  # 替换反斜杠为正斜杠
        file.save(os.path.join(current_app.static_folder, avatar_path))
        print(f"Static folder: {current_app.static_folder}")
        print(f"Saving file to: {os.path.join(
            current_app.static_folder, avatar_path)}")
        db = get_db()
        db.execute('UPDATE user SET avatar = ? WHERE id = ?',
                   (avatar_path, user_id))
        db.commit()

        return jsonify({"message": "Avatar updated successfully!"}), 200

    return jsonify({"error": "Failed to update avatar"}), 400


@bp.route('/update_username', methods=('POST',))
@login_required
def update_username():
    new_username = request.json['new_username']
    user_id = g.user['id']
    db = get_db()

    # 检查新用户名是否已存在
    existing_user = db.execute(
        'SELECT id FROM user WHERE username = ?', (new_username, )
    ).fetchone()
    if existing_user is not None:
        if existing_user['id'] == user_id:
            return jsonify({"error": "Username remains the same."}), 400
        else:
            return jsonify({"error": "Username already taken."}), 400

    # 更新用户名
    db.execute(
        'UPDATE user SET username = ? WHERE id = ?', (new_username, user_id)
    )
    db.commit()
    # 更新 session 中的用户名
    session['user_username'] = new_username

    return jsonify({"message": "Username updated successfully!"}), 200


@bp.route('/update_email', methods=('POST',))
@login_required
def update_email():
    user_id = g.user['id']
    db = get_db()
    new_email = request.json['new_email']

    # 获取当前用户的旧邮箱
    current_email = db.execute(
        'SELECT email FROM user WHERE id = ?', (user_id,)
    ).fetchone()

    if current_email is None:
        return jsonify({"error": "User not found."}), 404

    current_email = current_email['email']

    # 检查新邮箱是否已被使用
    existing_email = db.execute(
        'SELECT id FROM user WHERE email = ?', (new_email,)
    ).fetchone()
    if existing_email:
        if existing_email['id'] == user_id:
            return jsonify({"error": "Email remains the same."}), 400
        return jsonify({"error": "Email already taken."}), 400

    # 生成验证码
    verification_code = generate_verification_code()
    new_verification_code = generate_verification_code()

    # 向新邮箱和旧邮箱发送验证码
    send_verification_email(new_email, new_verification_code)
    send_verification_email(current_email, verification_code)

    # 将新邮箱和验证码存储到 session
    session['new_email'] = new_email
    session['verification_code'] = verification_code
    session['new_verification_code'] = new_verification_code

    return jsonify({
        "message": "Verification codes have been sent to your current and new email addresses."
    }), 200


@bp.route('/verify_email_codes', methods=('POST',))
@login_required
def verify_email_codes():
    user_id = g.user['id']
    db = get_db()

    # 从请求中获取验证码
    data = request.json
    old_verification_code = data.get('old_verification_code')
    new_verification_code = data.get('new_verification_code')

    # 从 session 获取存储的验证码和新邮箱
    session_old_code = session.get('verification_code')
    session_new_code = session.get('new_verification_code')
    new_email = session.get('new_email')

    if not (session_old_code and session_new_code and new_email):
        return jsonify({"error": "Verification codes or new email are missing."}), 400

    # 验证旧邮箱验证码
    if old_verification_code != session_old_code:
        return jsonify({"error": "Invalid verification code for the current email."}), 400

    # 验证新邮箱验证码
    if new_verification_code != session_new_code:
        return jsonify({"error": "Invalid verification code for the new email."}), 400

    # 更新数据库中的邮箱
    db.execute(
        'UPDATE user SET email = ? WHERE id = ?',
        (new_email, user_id)
    )
    db.commit()

    # 清除 session 中的验证码和新邮箱
    session.pop('verification_code', None)
    session.pop('new_verification_code', None)
    session.pop('new_email', None)

    return jsonify({"message": "Email address updated successfully."}), 200


@bp.route('/get_tags', methods=['GET'])
def get_tags():
    db = get_db()
    tags = db.execute('SELECT id, name FROM tags').fetchall()
    return jsonify({'tags': [dict(tag) for tag in tags]})


@bp.route('/update_tags', methods=['POST'])
@login_required
def update_tags():
    user_id = g.user['id']
    selected_tags = request.json.get('selected_tags')

    db = get_db()
    # 删除用户的所有旧标签
    db.execute('DELETE FROM user_tags WHERE user_id = ?', (user_id, ))
    # 添加用户新选择的标签
    db.executemany(
        'INSERT INTO user_tags (user_id, tag_id) VALUES (?, ?)',
        [(user_id, tag_id) for tag_id in selected_tags]
    )
    db.commit()

    return jsonify({"message": "Tags updated successfully!"}), 200


# 请求验证码
@bp.route('/request_verification_code', methods=['POST'])
@login_required
def request_verification_code():
    # 获取用户的邮箱
    email = g.user['email']

    # 生成验证码
    verification_code_for_psw = generate_verification_code()

    # 存储验证码到 session
    session['verification_code_for_psw'] = verification_code_for_psw
    session['email'] = email

    # 发送验证码邮件
    send_verification_email(email, verification_code_for_psw)

    return jsonify({"message": "Verification code sent"}), 200


# 更新密码
@bp.route('/update_password', methods=['POST'])
@login_required
def update_password():
    db = get_db()
    user_id = g.user['id']

    # 获取请求中的新密码和验证码
    new_password = request.json.get('new_password')
    verification_code_for_psw = request.json.get('verification_code_for_psw')

    # 验证验证码
    if 'verification_code_for_psw' not in session or verification_code_for_psw != session['verification_code_for_psw']:
        return jsonify({"error": "Invalid or expired verification code"}), 400

    # 获取当前用户的邮箱
    current_email = session.get('email')

    # 确保邮箱匹配
    if current_email != g.user['email']:
        return jsonify({"error": "Email mismatch"}), 400

    # 更新密码
    hashed_password = generate_password_hash(new_password)
    db.execute('UPDATE user SET password = ? WHERE id = ?',
               (hashed_password, user_id))
    db.commit()

    # 清除 session 中存储的验证码和邮箱
    session.pop('verification_code_for_psw', None)
    session.pop('email', None)

    return jsonify({"message": "Password updated successfully"}), 200


@bp.route('/records', methods=('GET', 'POST'))
@login_required
def view_records():
    db = get_db()
    user = db.execute('SELECT * FROM user WHERE id = ?',
                      (g.user['id'],)).fetchone()
    posts = db.execute(
        'SELECT * FROM apply_entry WHERE user_id = ? LIMIT 10', (g.user['id'],)).fetchall()
    comments = db.execute(
        'SELECT * FROM comment WHERE user_id = ? LIMIT 10', (g.user['id'],)).fetchall()
    posts_data = [dict(post) for post in posts]
    comments_data = [dict(comment) for comment in comments]
    return jsonify({
        'user': dict(user),
        'posts': posts_data,
        'comments': comments_data
    })

@bp.route('/get_s_messages<user_id>', methods=['GET'])
def get_s_messages(user_id):
    db = get_db()
    print('g.user:', g.user)
    s_messages = db.execute(
        ' SELECT * '
        ' FROM s_message '
        ' JOIN user ON s_message.receiver_id = user.id '
        ' WHERE s_message.receiver_id = ?',
        (user_id,)
    )
    s_messages_list = [dict(s_message) for s_message in s_messages]
    count_read_messages = db.execute(
        'SELECT COUNT(*) FROM s_message WHERE receiver_id = ?',
        (user_id,)
    ).fetchone()[0]

    return jsonify({
        's_messages': s_messages_list,
        'read_count': count_read_messages  # 返回已读消息的个数
    })

@bp.route('/get_s_messages<user_id>_read', methods=['GET'])
def get_s_messages_read(user_id):
    db = get_db()
    print('g.user:', g.user)
    s_messages = db.execute(
        ' SELECT * '
        ' FROM s_message '
        ' JOIN user ON s_message.receiver_id = user.id '
        ' WHERE s_message.receiver_id = ? AND is_read = 1',
        (user_id,)
    )
    s_messages_list = [dict(s_message) for s_message in s_messages]
    count_read_messages = db.execute(
        'SELECT COUNT(*) FROM s_message WHERE receiver_id = ? AND is_read = 1',
        (user_id,)
    ).fetchone()[0]

    return jsonify({
        's_messages': s_messages_list,
        'read_count': count_read_messages  # 返回已读消息的个数
    })

@bp.route('/get_s_messages<user_id>_not_read', methods=['GET'])
def get_s_messages_not_read(user_id):
    db = get_db()
    print('g.user:', g.user)
    s_messages = db.execute(
        ' SELECT * '
        ' FROM s_message '
        ' JOIN user ON s_message.receiver_id = user.id '
        ' WHERE s_message.receiver_id = ? AND is_read = 0',
        (user_id,)
    )
    s_messages_list = [dict(s_message) for s_message in s_messages]
    count_read_messages = db.execute(
        'SELECT COUNT(*) FROM s_message WHERE receiver_id = ? AND is_read = 0',
        (user_id,)
    ).fetchone()[0]

    return jsonify({
        's_messages': s_messages_list,
        'read_count': count_read_messages  # 返回已读消息的个数
    })

@bp.route('/set_read_<message_id>', methods=['POST'])
def set_read_message(message_id):
    db = get_db()
    db.execute(
        ' UPDATE s_message SET is_read = 1 WHERE message_id = ?',
        (message_id,)
    )
    db.commit()
    return jsonify({
        'sucsess': True
    })
