from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)

from flaskr.db import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/apply', methods=['GET', 'POST'])
def apply_form():
    db = get_db()
    applies = db.execute(
        ' SELECT * '
        ' FROM apply_entry a '
        ' JOIN user u ON u.id = a.user_id '
        ' JOIN topic t ON t.topic_id = a.topic_id '
        ' JOIN forums f ON f.forum_id = t.forum_id '
    ).fetchall()

    # 获取每个帖子的图片路径
    apply_images = {}
    for apply in applies:
        images = db.execute(
            '''
            SELECT image_path
            FROM apply_entry_images
            WHERE apply_id = ?
            ''',
            (apply['apply_id'],)
        ).fetchall()
        apply_images[apply['apply_id']] = [image['image_path']
                                           for image in images]

    return render_template('admin/apply.html', applies=applies, apply_images=apply_images)


@bp.route('/report_entry', methods=['GET', 'POST'])
def report_entry():
    db = get_db()
    reports = db.execute(
        ' SELECT * '
        ' FROM report_entry r '
        ' JOIN user u ON u.id = r.user_id '
        ' JOIN entry e ON e.entry_id = r.entry_id '
        ' JOIN topic t ON t.topic_id = e.topic_id '
        ' JOIN forums f ON f.forum_id = t.forum_id '
    ).fetchall()
    return render_template('admin/report_entry.html', reports=reports)
    # return render_template('admin/report_entry.html', reports=reports)


@bp.route('/report_comment', methods=['GET', 'POST'])
def report_comment():
    db = get_db()
    reports = db.execute(
        ' SELECT * '
        ' FROM report_comment r '
        ' JOIN user u ON u.id = r.user_id '
        ' JOIN comment c ON c.comment_id = r.comment_id '
        ' JOIN entry e ON e.entry_id = c.entry_id '
        ' JOIN topic t ON t.topic_id = e.topic_id '
        ' JOIN forums f ON f.forum_id = t.forum_id '
    ).fetchall()
    return render_template('admin/report_comment.html', reports=reports)


@bp.route('/report_user', methods=['GET', 'POST'])
def report_user():
    db = get_db()
    reports = db.execute(
        ' SELECT * '
        ' FROM report_user r '
        ' JOIN user u ON u.id = r.user_id '
        ' JOIN user u ON u.id = r.reporter_id '
    ).fetchall()
    return render_template('admin/report_user.html', reports=reports)


@bp.route('/apply/accept/<int:apply_id>', methods=['POST'])
def accept_apply(apply_id):
    db = get_db()

    # 更新申请状态为通过
    db.execute(
        'UPDATE apply_entry SET apply_status = 1 WHERE apply_id = ?',
        (apply_id,)
    )

    # 获取当前申请条目的信息
    cur_apply = db.execute(
        '''
        SELECT * 
        FROM apply_entry a
        JOIN user u ON u.id = a.user_id
        JOIN topic t ON t.topic_id = a.topic_id
        JOIN forums f ON f.forum_id = t.forum_id
        WHERE a.apply_id = ?
        ''',
        (apply_id,)
    ).fetchone()

    # 获取申请的标签
    tags = db.execute(
        '''
        SELECT tag_id
        FROM entry_tags
        WHERE entry_id = ?
        ''',
        (apply_id,)
    ).fetchall()

    # 获取申请的图片
    images = db.execute(
        '''
        SELECT image_path
        FROM apply_entry_images
        WHERE apply_id = ?
        ''',
        (apply_id,)
    ).fetchall()

    # 插入帖子数据
    db.execute(
        'INSERT INTO entry (topic_id, title, description) VALUES (?, ?, ?)',
        (cur_apply['topic_id'], cur_apply['entry_name'],
         cur_apply['description'])
    )
    db.commit()

    # 获取新帖子的 ID
    new_entry_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]

    # 插入标签到新帖子
    db.executemany(
        'INSERT INTO entry_tags (entry_id, tag_id) VALUES (?, ?)',
        [(new_entry_id, tag['tag_id']) for tag in tags]
    )

    # 插入图片到新帖子
    db.executemany(
        'INSERT INTO entry_images (entry_id, image_path) VALUES (?, ?)',
        [(new_entry_id, image['image_path']) for image in images]
    )

    db.commit()
    flash('申请已接受')
    return redirect(url_for('admin.apply_form'))


@bp.route('/apply/reject/<int:apply_id>', methods=['POST'])
def reject_apply(apply_id):
    db = get_db()
    db.execute(
        'UPDATE apply_entry SET apply_status = 2 WHERE apply_id = ?',
        (apply_id,)
    )
    db.commit()
    flash('申请已拒绝')
    return redirect(url_for('admin.apply_form'))


@bp.route('/report_entry/accept/<int:report_id>', methods=['POST'])
def accept_report(report_id):
    db = get_db()
    db.execute(
        'UPDATE report_entry SET report_status = 1 WHERE report_id = ?',
        (report_id,)
    )
    cur_entry = db.execute(
        'SELECT * FROM report_entry r JOIN entry e ON e.entry_id = r.entry_id WHERE r.report_id = ?',
        (report_id,)
    ).fetchone()
    if cur_entry is None:
        flash('举报失败，请检查该条目是否已被删除！')
    elif cur_entry['entry_status'] != 0:
        db.execute(
            ' UPDATE entry SET entry_status = 3 WHERE entry_id = ?',
            (cur_entry['entry_id'],)
        )
        db.commit()
        flash('举报失败，请检查该条目是否已被修改！')
    else:
        db.execute(
            ' UPDATE entry SET entry_status = 1 WHERE entry_id = ?',
            (cur_entry['entry_id'],)
        )
        db.commit()
        flash('举报已接受')
    return redirect(url_for('admin.report_entry'))


@bp.route('/report_entry/reject/<int:report_id>', methods=['POST'])
def reject_report(report_id):
    db = get_db()
    db.execute(
        'UPDATE report_entry SET report_status = 2 WHERE report_id = ?',
        (report_id,)
    )
    db.commit()
    flash('举报已拒绝')
    return redirect(url_for('admin.report_entry'))


@bp.route('/report_comment/accept/<int:report_id>', methods=['POST'])
def accept_comment(report_id):
    db = get_db()
    db.execute(
        'UPDATE report_comment SET report_status = 1 WHERE report_id = ?',
        (report_id,)
    )
    cur_comment = db.execute(
        'SELECT * FROM report_comment r JOIN comment c ON c.comment_id = r.comment_id WHERE r.report_id = ?',
        (report_id,)
    ).fetchone()
    if cur_comment is None:
        flash('举报失败，请检查该评论是否已被删除！')
    elif cur_comment['comment_status'] != 0:
        db.execute(
            ' UPDATE comment SET comment_status = 3 WHERE comment_id = ?',
            (cur_comment['comment_id'],)
        )
        db.commit()
        flash('举报失败，请检查该评论是否已被修改！')
    else:
        db.execute(
            ' UPDATE comment SET comment_status = 1 WHERE comment_id = ?',
            (cur_comment['comment_id'],)
        )
        db.commit()
        flash('举报已接受')
    return redirect(url_for('admin.report_comment'))


@bp.route('/report_comment/reject/<int:report_id>', methods=['POST'])
def reject_comment(report_id):
    db = get_db()
    db.execute(
        'UPDATE report_comment SET report_status = 2 WHERE report_id = ?',
        (report_id,)
    )
    db.commit()
    flash('举报已拒绝')
    return redirect(url_for('admin.report_comment'))


@bp.route('/report_user/accept/<int:report_id>', methods=['POST'])
def accept_user(report_id):
    db = get_db()
    db.execute(
        'UPDATE report_user SET report_status = 1 WHERE report_id = ?',
        (report_id,)
    )
    cur_comment = db.execute(
        'SELECT * FROM report_user r JOIN user u ON u.id = r.user_id WHERE r.report_id = ?',
        (report_id,)
    ).fetchone()
    if cur_comment is None:
        flash('举报失败，请检查该评论是否已被删除！')
    elif cur_comment['comment_status'] != 0:
        db.execute(
            ' UPDATE user SET user_status = 3 WHERE id = ?',
            (cur_comment['comment_id'],)
        )
        db.commit()
        flash('举报失败，请检查该评论是否已被修改！')
    else:
        db.execute(
            ' UPDATE user SET user_status = 1 WHERE id = ?',
            (cur_comment['comment_id'],)
        )
        db.commit()
        flash('举报已接受')
    return redirect(url_for('admin.report_user'))


@bp.route('/report_user/reject/<int:report_id>', methods=['POST'])
def reject_user(report_id):
    db = get_db()
    db.execute(
        'UPDATE report_user SET report_status = 2 WHERE report_id = ?',
        (report_id,)
    )
    db.commit()
    flash('举报已拒绝')
    return redirect(url_for('admin.report_user'))
