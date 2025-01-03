from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app, jsonify
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
import os
from .auth import login_required
from .db import get_db

bp = Blueprint('blog', __name__)  # 无urlprefix，因此用于根目录

UPLOAD_FOLDER = 'uploads/entry_images'  # 存放图片的目录
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


@bp.route('/')
def index():
    db = get_db()
    keyword = request.args.get('keyword', '').strip()
    tag_ids = request.args.getlist('tag_id')  # 获取多个标签的ID
    sort_by_hotness = request.args.get('sort_by_hotness', '0')
    params = []

    # 基础查询
    base_query = '''
        SELECT e.*, t.topic_name, f.forum_name, f.forum_id, COUNT(et.tag_id) AS common_tags_count
        FROM entry e
        JOIN topic t ON t.topic_id = e.topic_id
        JOIN forums f ON f.forum_id = t.forum_id
        LEFT JOIN entry_tags et ON e.entry_id = et.entry_id
        WHERE e.entry_status = 0
    '''

    # 如果有关键词搜索
    if keyword:
        base_query += " AND (e.title LIKE ? OR e.description LIKE ?)"
        params.extend([f'%{keyword}%', f'%{keyword}%'])

    # 如果有标签筛选
    if tag_ids:
        base_query += " AND et.tag_id IN ({})".format(
            ','.join(['?'] * len(tag_ids)))
        params.extend(tag_ids)

    # 按热度排序
    if sort_by_hotness == '1':
        base_query += " GROUP BY e.entry_id ORDER BY (0.8 * e.commented + 0.2 * e.views) DESC, common_tags_count DESC, e.updated DESC, e.entry_id DESC"
    else:
        # 默认按时间和共同标签数量排序
        base_query += " GROUP BY e.entry_id ORDER BY common_tags_count DESC, e.updated DESC, e.entry_id DESC"

    # 执行查询
    posts = db.execute(base_query, params).fetchall()

    # 获取评论信息
    comments = db.execute(
        '''
        SELECT *
        FROM comment c
        JOIN user u ON c.user_id = u.id
        JOIN entry e ON e.entry_id = c.entry_id
        WHERE e.entry_status = 0 AND c.comment_status = 0
        ORDER BY created ASC, c.comment_id ASC
        '''
    ).fetchall()

    all_tags = db.execute('SELECT * FROM tags').fetchall()

    # 获取每个帖子的标签
    entry_tags = {}
    for entry in posts:
        tags = db.execute(
            '''
            SELECT t.name
            FROM tags t
            JOIN entry_tags pt ON t.id = pt.tag_id
            WHERE pt.entry_id = ?
            ''',
            (entry['entry_id'],)
        ).fetchall()
        entry_tags[entry['entry_id']] = [tag['name'] for tag in tags]
    # 将数据格式化为字典列表
    posts_data = [dict(post) for post in posts]
    comments_data = [dict(comment) for comment in comments]

    # 返回 JSON 响应
    return jsonify({
        'posts': posts_data,
        'comments': comments_data,
        'entry_tags': entry_tags
    })
    '''
    # 获取每个帖子的图片路径
    entry_images = {}
    for entry in posts:
        images = db.execute(
            
            SELECT image_path
            FROM entry_images
            WHERE entry_id = ?
            ,
            (entry['entry_id'],)
        ).fetchall()
        entry_images[entry['entry_id']] = [image['image_path']
                                           for image in images]

    # 渲染模板
    return render_template('blog/index.html', keyword=keyword, tag_ids=tag_ids, sort_by_hotness=sort_by_hotness, posts=posts, comments=comments, tags=all_tags, entry_tags=entry_tags, entry_images=entry_images)
    '''


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_pic_topic(images, apply_entry_id, db):
    # 保存图片并记录路径
    for image in images[:9]:  # 最多处理 9 张图片
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            filepath = os.path.join(
                'uploads', 'entry_images', filename)
            filepath = filepath.replace('\\', '/')
            image.save(os.path.join(
                current_app.static_folder, filepath))
            db.execute(
                'INSERT INTO apply_entry_images (apply_id, image_path) VALUES (?, ?)',
                (apply_entry_id, filepath)
            )
    db.commit()


@bp.route('/t/<int:topic_id>', methods=['GET'])
def topic(topic_id):
    db = get_db()
    posts = db.execute(
        ' SELECT *'
        ' FROM entry e '
        ' JOIN topic t ON t.topic_id = e.topic_id '
        ' JOIN forums f ON f.forum_id = t.forum_id'
        ' WHERE t.topic_id = ? AND e.entry_status = 0 '
        ' ORDER BY updated DESC, e.entry_id DESC',
        (topic_id,)
    ).fetchall()
    comments = db.execute(
        ' SELECT * '
        ' FROM comment c '
        ' JOIN user u ON c.user_id = u.id '
        ' JOIN entry e ON e.entry_id = c.entry_id '
        ' JOIN topic t ON t.topic_id = e.topic_id '
        ' WHERE t.topic_id = ? AND e.entry_status = 0 AND c.comment_status = 0'
        ' ORDER BY created ASC, c.comment_id ASC',
        (topic_id,)
    ).fetchall()
    cur_topic = db.execute(
        ' SELECT * '
        ' FROM topic t'
        ' JOIN forums f ON f.forum_id = t.forum_id '
        ' WHERE t.topic_id = ?',
        (topic_id,)
    ).fetchone()

    # all_tags = db.execute('SELECT * FROM tags').fetchall()

    # 获取每个帖子的标签
    entry_tags = {}
    for entry in posts:
        tags = db.execute(
            '''
            SELECT t.name
            FROM tags t
            JOIN entry_tags pt ON t.id = pt.tag_id
            WHERE pt.entry_id = ?
            ''',
            (entry['entry_id'],)
        ).fetchall()
        entry_tags[entry['entry_id']] = [tag['name'] for tag in tags]
    posts_data = [dict(post) for post in posts]
    comments_data = [dict(comment) for comment in comments]
    cur_topic_data = dict(cur_topic)
    # return render_template('blog/topic.html', posts=posts, topic=cur_topic, comments=comments)
    # 返回 JSON 响应
    return jsonify({
        'posts': posts_data,
        'comments': comments_data,
        'cur_topic': cur_topic_data,
        'entry_tags': entry_tags
    })


@bp.route('/t/<int:topic_id>', methods=['POST'])
def apply_entry(topic_id):
    db = get_db()
    cur_topic = db.execute(
        ' SELECT * '
        ' FROM topic t'
        ' JOIN forums f ON f.forum_id = t.forum_id '
        ' WHERE t.topic_id = ?',
        (topic_id,)
    ).fetchone()
    data = request.get_json()  # 使用 request.get_json() 获取 JSON 数据
    if data is None:
        return jsonify({'success': False, 'message': '无效的请求格式'}), 400

    entry_name = data.get('title')
    description = data.get('body')
    selected_tags = data.get('selectedTags', [])
    user_id = data.get('id')
    if not entry_name or not description:
        return jsonify({'success': False, 'message': '条目名称或描述不能为空'}), 400
    else:
        db.execute(
            ' INSERT INTO apply_entry(user_id, topic_id, entry_name, description) VALUES (?, ?, ?, ?)',
            (user_id, cur_topic['topic_id'], entry_name, description)
        )
        db.commit()
        # 获取新创建的帖子 ID
        entry_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]
        db.executemany(
            'INSERT INTO entry_tags (entry_id, tag_id) VALUES (?, ?)',
            [(entry_id, tag_id) for tag_id in selected_tags]
        )
        db.commit()
        return jsonify({'success': True, 'message': '申请成功，请等待管理员审核'})


def get_tags_for_entry(entry_id):
    db = get_db()
    tags = db.execute(
        'SELECT tag_id FROM entry_tags WHERE entry_id = ?',
        (entry_id,)
    ).fetchall()
    return [tag['tag_id'] for tag in tags]


def get_all_tags():
    db = get_db()
    return db.execute('SELECT * FROM tags').fetchall()


@bp.route('/e/<int:entry_id>', methods=['GET'])
def entry(entry_id):
    db = get_db()
    cur_post = db.execute(
        ' SELECT *'
        ' FROM entry e '
        ' JOIN topic t ON t.topic_id = e.topic_id '
        ' JOIN forums f ON f.forum_id = t.forum_id'
        ' WHERE e.entry_id = ?'
        ' ORDER BY updated DESC, e.entry_id DESC',
        (entry_id,)
    ).fetchone()
    comments = db.execute(
        ' SELECT * '
        ' FROM comment c '
        ' JOIN user u ON c.user_id = u.id '
        ' JOIN entry e ON e.entry_id = c.entry_id '
        ' JOIN topic t ON t.topic_id = e.topic_id '
        ' WHERE e.entry_id = ? AND c.comment_status = 0 '
        ' ORDER BY created ASC, c.comment_id ASC',
        (entry_id,)
    ).fetchall()
    db.execute(
        ' UPDATE entry SET views = views + 1 WHERE entry_id = ? ',
        (entry_id,)
    )
    db.commit()
    if cur_post['entry_status'] != 0:
        return render_template('404.html'), 404
    tags = db.execute(
        '''
        SELECT *
        FROM tags t
        JOIN entry_tags pt ON t.id = pt.tag_id
        WHERE pt.entry_id = ?
        ''',
        (entry_id,)
    ).fetchall()
    if g.user is not None:
        db.execute(
            ' INSERT OR REPLACE INTO history (user_id, entry_id, created) '
            ' VALUES (?, ?, CURRENT_TIMESTAMP) ',
            (g.user['id'], entry_id)
        )
        db.commit()
    # 获取图片
    entry_images = db.execute(
        ' SELECT entry_id, image_path FROM entry_images WHERE entry_id IN '
        ' (SELECT entry_id FROM entry WHERE entry_id = ? AND entry_status = 0)',
        (entry_id,)
    ).fetchall()
    tag_data = [dict(tag) for tag in tags]
    post_data = dict(cur_post)
    comments_data = [dict(comment) for comment in comments]
    return jsonify({
        'post': post_data,
        'comments': comments_data,
        'entry_tags': tag_data
    })


# 评论功能需要登录
@bp.route('/e/<int:entry_id>', methods=['POST'])
def entry_comment(entry_id):
    db = get_db()
    cur_post = db.execute(
        'SELECT * '
        'FROM entry e '
        'JOIN topic t ON t.topic_id = e.topic_id '
        'JOIN forums f ON f.forum_id = t.forum_id '
        'WHERE e.entry_id = ?',
        (entry_id,)
    ).fetchone()

    if cur_post is None:
        return jsonify({'success': False, 'message': '帖子未找到'}), 404

    data = request.get_json()
    title = data.get('title')
    body = data.get('body')
    rate = data.get('rating')
    id = data.get('id')
    if not title:
        return jsonify({'success': False, 'message': '标题不能为空'})
    elif not body:
        return jsonify({'success': False, 'message': '评论内容不能为空'})
    elif not rate:
        return jsonify({'success': False, 'message': '评分不能为空'})
    elif rate > 10 or rate < 0:
        return jsonify({'success': False, 'message': '评分超出范围'})
    else:
        db.execute(
            'INSERT INTO comment (title,body,user_id,entry_id,rate) VALUES (?,?,?,?,?)',
            (title, body, id, cur_post["entry_id"], rate)
        )
        db.commit()
        return jsonify({'success': True, 'message': '评论已提交'})


@bp.route('/report_entry', methods=['POST'])
def report_entry():
    db = get_db()
    # 获取前端传递的数据
    data = request.get_json()
    user_id = data.get('user_id')
    entry_id = data.get('entry_id')
    reason = data.get('reason')
    print(data)
    if not user_id or not entry_id:
        return jsonify({'success': False, 'message': '缺少必要参数'}), 400
    db.execute(
        'INSERT INTO report_entry (user_id, entry_id, reason) VALUES (?, ?, ?)',
        (user_id, entry_id, reason)
    )
    db.commit()
    return jsonify({'success': True, 'message': '举报已提交'})


@bp.route('/block_entry', methods=['POST'])
def block_entry():
    db = get_db()
    # 获取前端传递的数据
    data = request.get_json()
    user_id = data.get('user_id')
    entry_id = data.get('entry_id')

    if not user_id or not entry_id:
        return jsonify({'success': False, 'message': '缺少必要参数'}), 400
    db.execute(
        'INSERT INTO block_entry (user_id, entry_id) VALUES (?,?)',
        (user_id, entry_id)
    )
    db.commit()
    return jsonify({'success': True, 'message': '条目已屏蔽'})


@bp.route('/report_comment', methods=['POST'])
def report_comment():
    db = get_db()
    # 获取前端传递的数据
    data = request.get_json()
    user_id = data.get('user_id')
    comment_id = data.get('comment_id')
    reason = data.get('reason')

    if not user_id or not comment_id:
        return jsonify({'success': False, 'message': '缺少必要参数'}), 400
    db.execute(
        'INSERT INTO report_comment (user_id, comment_id, reason) VALUES (?, ?, ?)',
        (user_id, comment_id, reason)
    )
    db.commit()
    return jsonify({'success': True, 'message': '举报已提交'})


@bp.route('/report_user', methods=['POST'])
def report_user():
    db = get_db()
    if g.user is None:
        flash('举报提交失败，请先登录！')
    else:
        reporter_id = request.form['reporter_id']
        reason = request.form['reason']
        user_id = g.user['id']  # 当前登录用户的ID
        db.execute(
            'INSERT INTO report_user (reporter_id, user_id, reason) VALUES (?, ?, ?)',
            (reporter_id, user_id, reason)
        )
        db.commit()
        flash('举报已提交，感谢您的反馈！')
    return redirect(request.referrer)


@bp.route('/block_comment', methods=['POST'])
def block_comment():
    db = get_db()
    # 获取前端传递的数据
    data = request.get_json()
    user_id = data.get('user_id')
    comment_id = data.get('comment_id')

    if not user_id or not comment_id:
        return jsonify({'success': False, 'message': '缺少必要参数'}), 400
    db.execute(
        'INSERT INTO block_comment (user_id, comment_id) VALUES (?,?)',
        (user_id, comment_id)
    )
    db.commit()
    return jsonify({'success': True, 'message': '评论已屏蔽'})


@bp.route('/like_comment', methods=['POST'])
def like_comment():
    db = get_db()
    if g.user is None:
        flash('点赞失败，请先登录！')
    else:
        comment_id = request.form['comment_id']
        user_id = g.user['id']
        db.execute(
            'INSERT INTO like (user_id, comment_id) VALUES (?, ?)',
            (user_id, comment_id)
        )
        db.commit()
        flash('点赞成功！')
    return redirect(request.referrer)


@bp.route('/api/like_cans', methods=['POST'])
def cans_like():
    db = get_db()
    if g.user is None:
        flash('点赞取消失败，请先登录！')
    else:
        comment_id = request.form['comment_id']
        user_id = g.user['id']
        db.execute(
            'DELETE FROM like WHERE user_id = ? AND comment_id = ?',
            (user_id, comment_id)
        )
        db.commit()
        flash('点赞取消成功！')
    return redirect(request.referrer)


@bp.route('/api/like_notif', methods=['POST'])
def send_like_notification(like_user_id, comment_id):
    db = get_db()

    receiver_id = db.execute(
        'SELECT user_id FROM comment WHERE comment_id = ?',
        (comment_id,)
    ).fetchone()

    if receiver_id:
        receiver_id = receiver_id[0]
        content = f"您的#{comment_id}评论在{get_current_timestamp()}被用户{
            like_user_id}点赞"
        db.execute(
            ' INSERT INTO s_message (receiver_id, content) '
            ' VALUES (?, ?)',
            (receiver_id, content)
        )
        db.commit()

    db.close()


def get_current_timestamp():
    # 获取当前时间戳，可以根据实际需求调整
    from datetime import datetime
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


@bp.route('/f/<int:forum_id>', methods=('GET', 'POST'))
def forum(forum_id):
    db = get_db()
    posts = db.execute(
        ' SELECT *'
        ' FROM entry e '
        ' JOIN topic t ON t.topic_id = e.topic_id '
        ' JOIN forums f ON f.forum_id = t.forum_id'
        ' WHERE f.forum_id = ? AND e.entry_status = 0 '
        ' ORDER BY updated DESC, e.entry_id DESC',
        (forum_id,)
    ).fetchall()
    topics = db.execute(
        ' SELECT *'
        ' FROM topic t '
        ' JOIN forums f ON f.forum_id = t.forum_id'
        ' WHERE f.forum_id = ?',
        (forum_id,)
    ).fetchall()
    # 获取每个帖子的标签
    entry_tags = {}
    for entry in posts:
        tags = db.execute(
            '''
            SELECT t.name
            FROM tags t
            JOIN entry_tags pt ON t.id = pt.tag_id
            WHERE pt.entry_id = ?
            ''',
            (entry['entry_id'],)
        ).fetchall()
        entry_tags[entry['entry_id']] = [tag['name'] for tag in tags]
    cur_forum = db.execute(
        'SELECT * FROM forums WHERE forum_id = ?',
        (forum_id,)
    ).fetchone()
    posts_data = [dict(post) for post in posts]
    topics_data = [dict(topic) for topic in topics]
    cur_forum_data = dict(cur_forum)
    return jsonify({
        'posts': posts_data,
        'topics': topics_data,
        'cur_forum': cur_forum_data,
        'entry_tags': entry_tags
    })


@bp.route('/api/forums', methods=('GET', 'POST'))
def get_all_forums():
    db = get_db()
    forums = db.execute(
        ' SELECT * FROM forums ORDER BY forum_id '
    ).fetchall()
    forums_list = [dict(forum) for forum in forums]
    return jsonify({'forums': forums_list})


@bp.route('/api/user', methods=('GET', 'POST'))
def get_user_info():
    if g.user is None:
        flash("请先登录")
        # 返回未登录的状态
        return jsonify({'status': 'error', 'message': 'Please log in'}), 400
    else:
        user_id = g.user['id']  # 当前登录用户的ID
        db = get_db()
        user = db.execute(
            ' SELECT * FROM user WHERE id=?',
            (user_id,)
        ).fetchone()
        if user is None:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404
        user_dict = dict(user)
        return jsonify({'user': user_dict})


@bp.route('/api/get_most_viewed_posts', methods=['GET'])
def get_most_viewed_posts():
    db = get_db()
    posts = db.execute(
        ' SELECT * '
        ' FROM entry e '
        'JOIN topic t ON e.topic_id = t.topic_id  '
        'JOIN forums f ON t.forum_id = f.forum_id  '
        ' ORDER BY e.views DESC'
        ' LIMIT 10 '
    ).fetchall()
    # 获取每个帖子的标签
    entry_tags = {}
    for entry in posts:
        tags = db.execute(
            '''
            SELECT t.name
            FROM tags t
            JOIN entry_tags pt ON t.id = pt.tag_id
            WHERE pt.entry_id = ?
            ''',
            (entry['entry_id'],)
        ).fetchall()
        entry_tags[entry['entry_id']] = [tag['name'] for tag in tags]
    posts_list = [dict(post) for post in posts]
    return jsonify({
        'posts': posts_list,
        'entry_tags': entry_tags
    })


@bp.route('/api/get_hottest_posts', methods=['GET'])
def get_hotness_posts():
    db = get_db()
    posts = db.execute(
        '''
        SELECT e.*, t.topic_name, f.forum_name, f.forum_id, COUNT(et.tag_id) AS common_tags_count
        FROM entry e
        JOIN topic t ON t.topic_id = e.topic_id
        JOIN forums f ON f.forum_id = t.forum_id
        LEFT JOIN entry_tags et ON e.entry_id = et.entry_id
        WHERE e.entry_status = 0
        GROUP BY e.entry_id ORDER BY (0.8 * e.commented + 0.2 * e.views) DESC, common_tags_count DESC, e.updated DESC, e.entry_id DESC
        '''
    ).fetchall()
    # 获取评论信息
    comments = db.execute(
        '''
        SELECT *
        FROM comment c
        JOIN user u ON c.user_id = u.id
        JOIN entry e ON e.entry_id = c.entry_id
        WHERE e.entry_status = 0 AND c.comment_status = 0
        ORDER BY created ASC, c.comment_id ASC
        '''
    ).fetchall()
    # 获取每个帖子的标签
    entry_tags = {}
    for entry in posts:
        tags = db.execute(
            '''
            SELECT t.name
            FROM tags t
            JOIN entry_tags pt ON t.id = pt.tag_id
            WHERE pt.entry_id = ?
            ''',
            (entry['entry_id'],)
        ).fetchall()
        entry_tags[entry['entry_id']] = [tag['name'] for tag in tags]
    # 将数据格式化为字典列表
    posts_data = [dict(post) for post in posts]
    comments_data = [dict(comment) for comment in comments]

    # 返回 JSON 响应
    return jsonify({
        'posts': posts_data,
        'comments': comments_data,
        'entry_tags': entry_tags
    })


@bp.route('/api/get_recommend_posts', methods=['GET'])
def get_recommend_posts():
    db = get_db()
    if not g.user:  # 如果用户没有登录，使用默认排序
        posts = db.execute(
            '''
            SELECT *
            FROM entry e
            JOIN topic t ON t.topic_id = e.topic_id
            JOIN forums f ON f.forum_id = t.forum_id
            WHERE e.entry_status = 0
            ORDER BY updated DESC, e.entry_id DESC
            '''
        ).fetchall()
    else:  # 如果用户已登录，使用推荐排序
        user_id = g.user['id']  # 当前用户ID

        # 获取当前用户的标签
        user_tags = db.execute(
            '''
            SELECT tag_id
            FROM user_tags
            WHERE user_id = ?
            ''', (user_id,)
        ).fetchall()

        # 获取标签ID列表
        tag_ids = [tag['tag_id'] for tag in user_tags]
        if not tag_ids:
            posts = db.execute(
                '''
                SELECT *
                FROM entry e
                JOIN topic t ON t.topic_id = e.topic_id
                JOIN forums f ON f.forum_id = t.forum_id
                WHERE e.entry_status = 0
                ORDER BY updated DESC, e.entry_id DESC
                '''
            ).fetchall()
        else:
            posts = db.execute(
                '''
                SELECT 
                    *, 
                    COALESCE(SUM(e.views), 0) AS views, -- 获取浏览量
                    COUNT(et.entry_id) AS match_count,             -- 获取标签匹配数量
                    -- 按权重计算加权总分：0.1 * 浏览量 + 5 * 标签匹配数量 + 2 * 平均评分
                    (0.1 * COALESCE(SUM(e.views), 0) + 5 * COUNT(et.entry_id) + 2 * AVG(e.avg_rate)) AS weighted_score
                FROM 
                    entry e
                LEFT JOIN 
                    entry_tags et ON e.entry_id = et.entry_id AND et.tag_id IN ({})

                JOIN topic t ON e.topic_id = t.topic_id  
                JOIN forums f ON t.forum_id = f.forum_id  
                GROUP BY 
                    e.entry_id
                ORDER BY 
                    weighted_score DESC, 
                    e.updated DESC
                '''.format(','.join(['?'] * len(tag_ids))),
                tag_ids
            ).fetchall()

    # 获取评论信息
    comments = db.execute(
        '''
        SELECT *
        FROM comment c
        JOIN user u ON c.user_id = u.id
        JOIN entry e ON e.entry_id = c.entry_id
        WHERE e.entry_status = 0 AND c.comment_status = 0
        ORDER BY created ASC, c.comment_id ASC
        '''
    ).fetchall()
    # 获取每个帖子的标签
    entry_tags = {}
    for entry in posts:
        tags = db.execute(
            '''
            SELECT t.name
            FROM tags t
            JOIN entry_tags pt ON t.id = pt.tag_id
            WHERE pt.entry_id = ?
            ''',
            (entry['entry_id'],)
        ).fetchall()
        entry_tags[entry['entry_id']] = [tag['name'] for tag in tags]
    # 将数据格式化为字典列表
    posts_data = [dict(post) for post in posts]
    comments_data = [dict(comment) for comment in comments]

    # 返回 JSON 响应
    return jsonify({
        'posts': posts_data,
        'comments': comments_data,
        'entry_tags': entry_tags
    })


@bp.route('/api/get_tags', methods=['GET'])
def get_all_tags():
    db = get_db()
    tags = db.execute('SELECT * FROM tags').fetchall()
    tags_list = [dict(tag) for tag in tags]
    return jsonify({
        'tags': tags_list
    })


@bp.route('/statistics', methods=['GET'])
def get_statistics():
    db = get_db()
    user_counts = db.execute('SELECT COUNT(*) FROM user').fetchone()[0]
    entry_counts = db.execute('SELECT COUNT(*) FROM entry').fetchone()[0]
    comment_counts = db.execute('SELECT COUNT(*) FROM comment').fetchone()[0]
    total_views = db.execute(
        'SELECT SUM(views) AS total_views FROM entry;').fetchone()[0]
    return jsonify({
        'user_counts': user_counts,
        'entry_counts': entry_counts,
        'comment_counts': comment_counts,
        'total_views': total_views
    })


@bp.route('/api/get_posted_comments', methods=["GET"])
def get_posted_comments():
    db = get_db()
    if g.user is None:
        print('get_posted_comments called, but no user')
        return jsonify({
            'error': 'No user logged in'
        })
    comments = db.execute(
        ' SELECT comment.*, entry.title AS entry_title, entry.entry_id '
        ' FROM comment '
        ' JOIN entry ON entry.entry_id = comment.entry_id'
        ' WHERE user_id = ? ORDER BY comment.created DESC LIMIT 4',
        (g.user['id'],)
    ).fetchall()
    comments_list = [dict(comment) for comment in comments]
    print('get_posted_comments called, comments:', comments_list)
    return jsonify({
        'comments': comments_list
    })


@bp.route('/api/get_history', methods=["GET"])
def get_history():
    db = get_db()
    if g.user is None:
        print('get_history called, but no user')
        return jsonify({
            'error': 'No user logged in'
        })
    records = db.execute(
        ' SELECT * '
        ' FROM history '
        ' JOIN entry ON entry.entry_id = history.entry_id'
        ' WHERE user_id = ? ORDER BY history.created DESC LIMIT 4',
        (g.user['id'],)
    ).fetchall()
    records_list = [dict(record) for record in records]
    # print('get_posted_comments called, records:', records_list)
    return jsonify({
        'records': records_list
    })


@bp.route('/api/get_recommended_topics', methods=["GET"])
def get_recommended_topic():
    db = get_db()
    topics = db.execute(
        ' SELECT topic.*, SUM(entry.views) AS total_views '
        ' FROM topic '
        ' JOIN entry ON entry.topic_id = topic.topic_id '
        ' GROUP BY topic.topic_id '
        ' ORDER BY total_views DESC '
        ' LIMIT 6 '
    ).fetchall()
    topics_list = [dict(topic) for topic in topics]
    return jsonify({
        'topics': topics_list
    })


@bp.route('/api/get_block_list/<int:entry_id>', methods=['GET'])
def get_block_list(entry_id):
    db = get_db()
    blocks = db.execute(
        ' SELECT * FROM block_entry WHERE entry_id = ?',
        (entry_id,)
    ).fetchall()
    block_list = [dict(block) for block in blocks]
    print(f"block_list: {block_list}")
    return jsonify({
        "block_list": block_list
    })


@bp.route('/api/get_block_comments_list/<int:comment_id>', methods=['GET'])
def get_block_comments_list(comment_id):
    db = get_db()
    blocks = db.execute(
        ' SELECT * FROM block_comment WHERE comment_id = ?',
        (comment_id,)
    ).fetchall()
    block_list = [dict(block) for block in blocks]
    print(f"block_list: {block_list}")
    return jsonify({
        "block_list": block_list
    })
