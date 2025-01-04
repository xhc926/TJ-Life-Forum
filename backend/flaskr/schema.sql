DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS admin;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS comment;
DROP TABLE IF EXISTS forums;
DROP TABLE IF EXISTS topic;
DROP TABLE IF EXISTS entry;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS user_tags;
DROP TABLE IF EXISTS post_tags;
DROP TABLE IF EXISTS apply_entry;
DROP TABLE IF EXISTS report_entry;
DROP TABLE IF EXISTS block_entry;
DROP TABLE IF EXISTS entry_tags;
DROP TABLE IF EXISTS entry_images;
DROP TABLE IF EXISTS report_comment;
DROP TABLE IF EXISTS report_user;
DROP TABLE IF EXISTS block_comment;
DROP TABLE IF EXISTS u_message;
DROP TABLE IF EXISTS s_message;
DROP TABLE IF EXISTS like;
DROP TABLE IF EXISTS history;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    introduction TEXT DEFAULT '这个人很神秘~',
    user_status INTEGER DEFAULT 0,       -- ENUM(0:active, 1:inactive)
    is_verified INTEGER DEFAULT 0,
    avatar TEXT
);
CREATE TABLE forums (
    forum_id INTEGER PRIMARY KEY AUTOINCREMENT,
    forum_name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE topic (
    topic_id INTEGER PRIMARY KEY AUTOINCREMENT ,
    topic_name VARCHAR(100) NOT NULL ,
    forum_id INTEGER NOT NULL ,
    description TEXT,
    FOREIGN KEY (forum_id) REFERENCES forums(forum_id)
);
CREATE TABLE entry (
    entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    avg_rate DECIMAL(2,1) DEFAULT 0.0,
    commented INTEGER DEFAULT 0,
    views INTEGER DEFAULT 0,
    entry_status INTEGER DEFAULT 0,       -- ENUM(0:active, 1:inactive)
    FOREIGN KEY (topic_id) REFERENCES topic(topic_id)
);
CREATE TABLE apply_entry(
    apply_id INTEGER PRIMARY KEY AUTOINCREMENT ,
    user_id INTEGER NOT NULL ,
    topic_id INTEGER NOT NULL ,
    entry_name TEXT NOT NULL,
    description TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    apply_status INTEGER DEFAULT 0,       -- ENUM(0:pending, 1:accept, 2:reject)
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (topic_id) REFERENCES topic(topic_id)
);
CREATE TABLE report_entry(
    report_id INTEGER PRIMARY KEY AUTOINCREMENT ,
    user_id INTEGER NOT NULL ,
    entry_id INTEGER NOT NULL,
    reason TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    report_status INTEGER DEFAULT 0,       -- ENUM(0:pending, 1:accept, 2:reject, 3:error)
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (entry_id) REFERENCES entry(entry_id)
);
CREATE TABLE block_entry (
    block_id INTEGER PRIMARY KEY AUTOINCREMENT ,
    user_id INTEGER NOT NULL ,
    entry_id INTEGER NOT NULL ,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (entry_id) REFERENCES entry(entry_id)
);
CREATE TABLE report_comment(
    report_id INTEGER PRIMARY KEY AUTOINCREMENT ,
    user_id INTEGER NOT NULL ,
    comment_id INTEGER NOT NULL,
    reason TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    report_status INTEGER DEFAULT 0,       -- ENUM(0:pending, 1:accept, 2:reject, 3:error)
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (comment_id) REFERENCES comment(comment_id)
);
CREATE TABLE block_comment(
    report_id INTEGER PRIMARY KEY AUTOINCREMENT ,
    user_id INTEGER NOT NULL ,
    comment_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (comment_id) REFERENCES comment(comment_id)
);
CREATE TABLE report_user(
    report_id INTEGER PRIMARY KEY AUTOINCREMENT ,
    reporter_id INTEGER NOT NULL ,
    user_id INTEGER NOT NULL ,
    reason TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    report_status INTEGER DEFAULT 0,       -- ENUM(0:pending, 1:accept, 2:reject, 3:error)
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (reporter_id) REFERENCES user (id)
);
CREATE TABLE admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);
INSERT INTO admin(username, password)
VALUES ('admin','scrypt:32768:8:1$7ktMopw8sYs2VA2F$aeb1b4c211743e1743e2720a82b71b90c033aafb68e9f75d9b3ad8804f1142d45bc8be622d09313dc9fa9a3a1cdfb8b9b6b7d95de90bc307d4f4540998a8e95c');
INSERT INTO user(username, email, password, is_verified)
VALUES (
        '123',
        '2254235@tongji.edu.cn',
        'scrypt:32768:8:1$puGOttzojIts1B65$880c723e88116477c1179588904bd47c66cea986fe37fead820fb957049742b37701a0669caef37581c88dea061e7e3e350733c42c8ace97e2db0ca81647b3d1',
        1
    );
-- 密码为123
CREATE TABLE comment (
    comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    rate INTEGER NOT NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    comment_status INTEGER DEFAULT 0,   --ENUM(0:active, 1:inactive)
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (entry_id) REFERENCES entry(entry_id),
    FOREIGN KEY (user_id) REFERENCES user (id)
);
CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL
);
CREATE TABLE user_tags (
    user_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags (id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, tag_id)
);
CREATE TABLE entry_tags(
    entry_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    FOREIGN KEY (entry_id) REFERENCES entry (entry_id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags (id) ON DELETE CASCADE,
    PRIMARY KEY (entry_id, tag_id)
);
CREATE TABLE entry_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    -- 图片记录的唯一标识
    entry_id INTEGER NOT NULL,
    -- 关联的 entry ID
    image_path TEXT NOT NULL,
    -- 图片存储的相对路径
    uploaded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -- 上传时间
    FOREIGN KEY (entry_id) REFERENCES entry(entry_id) ON DELETE CASCADE
);
CREATE TABLE u_message (
    message_id INTEGER PRIMARY KEY AUTOINCREMENT,
    auther_id INTEGER,
    receiver_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_read INTEGER DEFAULT 0,          -- ENUM(0:not read, 1:read)
    FOREIGN KEY (auther_id) REFERENCES user(id),
    FOREIGN KEY (receiver_id) REFERENCES user(id)
);
CREATE TABLE s_message (
    message_id INTEGER PRIMARY KEY AUTOINCREMENT,
    receiver_id INTEGER NOT NULL,
    title TEXT DEFAULT '来自系统的消息',
    content TEXT NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_read INTEGER DEFAULT 0,          -- ENUM(0:not read, 1:read)
    FOREIGN KEY (receiver_id) REFERENCES user(id)
);
CREATE TABLE like (
    like_id INTEGER PRIMARY KEY AUTOINCREMENT ,
    comment_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL ,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE history(
    record_id INTEGER PRIMARY KEY AUTOINCREMENT ,
    user_id INTEGER NOT NULL ,
    entry_id INTEGER NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (entry_id) REFERENCES entry(entry_id),
    CONSTRAINT unique_user_entry UNIQUE (user_id, entry_id)
);

CREATE TRIGGER update_entry_timestamp
AFTER UPDATE ON entry
FOR EACH ROW
WHEN NEW.updated = OLD.updated  -- 确保不是因为直接更新了 updated 列触发的
BEGIN
    UPDATE entry SET updated = CURRENT_TIMESTAMP WHERE entry_id = OLD.entry_id;
END;

CREATE TRIGGER increment_commented_count
AFTER INSERT ON comment
FOR EACH ROW
BEGIN
    UPDATE entry
    SET commented = commented + 1
    WHERE entry_id = NEW.entry_id;
END;

CREATE TRIGGER update_avg_rate
AFTER INSERT ON comment
BEGIN
    UPDATE entry
    SET avg_rate = (
        SELECT AVG(rate)
        FROM comment
        WHERE entry_id = NEW.entry_id
    )
    WHERE entry_id = NEW.entry_id;
END;

CREATE TRIGGER update_avg_rate_on_update
AFTER UPDATE OF rate ON comment
BEGIN
    UPDATE entry
    SET avg_rate = (
        SELECT AVG(rate)
        FROM comment
        WHERE entry_id = NEW.entry_id
    )
    WHERE entry_id = NEW.entry_id;
END;

-- 插入论坛数据
INSERT INTO forums(forum_name, description)
VALUES
    ('学业', '关于学习和学术研究的讨论'),
    ('选课', '有关课程选择的建议与讨论'),
    ('娱乐', '关于娱乐活动和文化娱乐的讨论'),
    ('树洞', '情感问题和匿名吐槽的交流'),
    ('旅游', '全球各地旅游景点及旅行心得分享'),
    ('美食', '美食爱好者的聚集地，分享各地美食心得'),
    ('体育', '关于体育赛事、健身和运动的讨论'),
    ('职场', '职场经验分享与职业规划'),
    ('游戏', '关于游戏、电竞和虚拟世界的讨论');

-- 插入话题数据
INSERT INTO topic(topic_name, forum_id, description)
VALUES
    ('软件工程', '1', '关于软件开发、编程语言及实践的讨论'),
    ('人工智能', '1', '探讨人工智能的最新研究与应用'),
    ('操作系统', '1', '讨论操作系统的设计与实现'),
    ('课程选择经验', '2', '分享各类课程选择的心得与经验'),
    ('羽毛球', '3', '羽毛球爱好者的讨论与活动安排'),
    ('桌游', '3', '讨论各类桌游与相关活动'),
    ('情感故事', '4', '分享情感经历与恋爱故事'),
    ('旅行攻略', '5', '旅游达人分享全球旅行经验'),
    ('美食推荐', '6', '餐饮爱好者推荐各地美食'),
    ('健身与运动', '7', '讨论健身与运动的技巧与健康话题'),
    ('职场经验', '8', '分享职场中的成功与失败经验'),
    ('电竞比赛', '9', '最新的电竞赛事和赛事评论'),
    ('摄影', '5', '分享摄影作品与摄影技巧');

-- 插入用户数据
INSERT INTO user(username, email, password, is_verified)
VALUES
    ('张伟', 'zhangwei@example.com', 'scrypt:32768:8:1$xyz$abcdef1234567890', 1),
    ('李娜', 'lina@example.com', 'scrypt:32768:8:1$xyz$abcdef1234567890', 1),
    ('王磊', 'wanglei@example.com', 'scrypt:32768:8:1$xyz$abcdef1234567890', 1),
    ('刘芳', 'liufang@example.com', 'scrypt:32768:8:1$xyz$abcdef1234567890', 1),
    ('陈杰', 'chenjie@example.com', 'scrypt:32768:8:1$xyz$abcdef1234567890', 1),
    ('赵敏', 'zhaomin@example.com', 'scrypt:32768:8:1$xyz$abcdef1234567890', 1),
    ('杨梅', 'yangmei@example.com', 'scrypt:32768:8:1$xyz$abcdef1234567890', 1),
    ('孙亮', 'sunliang@example.com', 'scrypt:32768:8:1$xyz$abcdef1234567890', 1),
    ('周婷', 'zhouting@example.com', 'scrypt:32768:8:1$xyz$abcdef1234567890', 1),
    ('钱国', 'qianguo@example.com', 'scrypt:32768:8:1$xyz$abcdef1234567890', 1);

-- 插入帖子数据
INSERT INTO entry(topic_id, title, description, views)
VALUES
    ('1', '软件工程课程概述', '软件工程的基本理论和实践经验分享', 5),
    ('1', '学习C语言的技巧', '如何高效学习C语言编程', 14),
    ('2', 'AI的发展历程', '人工智能从诞生到现在的演变与未来的前景', 4),
    ('2', '机器学习的入门教程', '机器学习的基本概念和实践操作', 7),
    ('3', '操作系统的基本原理', '操作系统的设计原理和实现方法', 4),
    ('3', 'Linux命令行技巧', 'Linux常用命令与技巧总结', 2),
    ('4', '2022年秋季选课建议', '2022年秋季学期的选课建议', 3),
    ('4', '如何选择最适合自己的课程', '基于兴趣与职业规划的课程选择建议', 5),
    ('5', '羽毛球运动技巧', '羽毛球的基本技巧与训练方法', 4),
    ('6', '桌游爱好者分享', '大家最喜欢的桌游有哪些？', 8),
    ('7', '情感故事分享', '关于恋爱、婚姻、人生的感人故事', 10),
    ('8', '最新旅游目的地推荐', '分享全球最受欢迎的旅游景点', 3),
    ('9', '全球美食推荐', '分享来自世界各地的美味食品', 2),
    ('10', '健身房推荐与选择', '如何选择适合自己的健身房', 10),
    ('11', '电竞比赛分析', '分析最近几场热门电竞比赛的精彩瞬间', 0),
    ('12', '如何成为职业摄影师', '从业余爱好到职业摄影师的转变过程', 2);

-- 插入评论数据
INSERT INTO comment(entry_id, user_id, body, rate, title)
VALUES
    ('1', '1', '非常喜欢这门课程，讲解清晰', 9, '很实用'),
    ('2', '1', 'C语言的学习不易，但有技巧可以提升效率', 8, '学习心得'),
    ('3', '3', '人工智能真的很有前景，希望能多关注这方面的课程', 10, '未来可期'),
    ('4', '4', '机器学习是一个非常有挑战性的话题，值得深入研究', 8, '探索AI'),
    ('5', '5', '操作系统理论非常深奥，但很有趣，建议加强实际操作', 7, '学习心得'),
    ('6', '6', 'Linux命令行很强大，值得每天多用', 9, '命令行技巧'),
    ('7', '7', '选课建议非常有用，感谢分享', 9, '选课心得'),
    ('8', '8', '选课时，选择自己喜欢的课程是最重要的', 8, '课程选择'),
    ('9', '9', '羽毛球运动非常适合锻炼，喜欢的朋友可以多学学', 9, '羽毛球技巧'),
    ('10', '10', '桌游真的很有趣，推荐大家试试', 9, '桌游推荐'),
    ('11', '11', '情感故事很感人，大家都应该认真看一看', 8, '情感故事'),
    ('12', '12', '旅行地推荐很棒，大家可以去看看', 9, '旅游推荐'),
    ('13', '13', '美食真是诱人，每一道都想试试', 10, '全球美食'),
    ('14', '14', '健身房的选择真的很重要，大家要多了解', 8, '健身选择'),
    ('15', '15', '电竞比赛分析非常到位，学到了很多', 9, '电竞赛事'),
    ('16', '16', '摄影的技巧需要不断摸索，不断进步', 9, '摄影技巧');

-- 插入标签数据
INSERT INTO tags (name)
VALUES
    ('编程'),
    ('人工智能'),
    ('操作系统'),
    ('运动'),
    ('旅行'),
    ('美食'),
    ('摄影'),
    ('桌游'),
    ('情感'),
    ('职场');

-- 插入用户标签数据
INSERT INTO user_tags (user_id, tag_id)
VALUES
    (1, 1),  -- 张伟的兴趣标签 '编程'
    (2, 2),  -- 李娜的兴趣标签 '人工智能'
    (3, 3),  -- 王磊的兴趣标签 '操作系统'
    (4, 4),  -- 刘芳的兴趣标签 '运动'
    (5, 5),  -- 陈杰的兴趣标签 '旅行'
    (6, 6),  -- 赵敏的兴趣标签 '美食'
    (7, 7),  -- 杨梅的兴趣标签 '摄影'
    (8, 8),  -- 孙亮的兴趣标签 '桌游'
    (9, 9),  -- 周婷的兴趣标签 '情感'
    (10, 10); -- 钱国的兴趣标签 '职场'

-- 插入帖子标签数据
INSERT INTO entry_tags (entry_id, tag_id)
VALUES
    (1, 1), (1, 2),    -- 软件工程和编程、人工智能相关
    (2, 1), (2, 3),    -- C语言和操作系统相关
    (3, 1), (3, 2),    -- AI和编程、人工智能相关
    (4, 1), (4, 2),    -- 机器学习和编程、人工智能相关
    (5, 1), (5, 3),    -- 操作系统和编程相关
    (6, 3),            -- Linux和操作系统相关
    (9, 4),            -- 羽毛球和运动相关
    (10, 8),           -- 桌游相关
    (11, 9), (11, 10), -- 情感和职场相关
    (12, 5),           -- 旅游相关
    (13, 6),           -- 美食相关
    (14, 4),           -- 健身房和运动相关
    (16, 7), (16, 10); -- 职业摄影师和摄影、职场相关
-- 插入申请提交的帖子数据
INSERT INTO apply_entry(user_id, topic_id, entry_name, description)
VALUES
    (1, 1, '软件工程项目管理', '关于如何管理大型软件开发项目的心得和经验'),
    (2, 2, '人工智能的伦理问题', '人工智能在伦理方面的挑战与问题探讨'),
    (3, 3, 'Linux系统性能优化', '如何优化Linux系统的性能，提升运行效率'),
    (4, 4, '秋季选课的常见错误', '分享在选课时容易犯的一些错误和避免方法'),
    (5, 5, '羽毛球比赛策略', '分析羽毛球比赛中的常见策略和技巧'),
    (6, 6, '全球美食推荐', '推荐一些来自世界各地的美食和餐厅'),
    (7, 7, '摄影基础教程', '从基础开始学习摄影的技巧和方法'),
    (8, 8, '桌游活动组织技巧', '如何组织一场桌游活动，提升参与感'),
    (9, 9, '情感交流与心理学', '探索情感交流中的心理学知识，提升沟通技巧'),
    (10, 10, '职场沟通技巧', '如何在职场中有效沟通，提升工作效率');
-- 插入举报帖子数据
INSERT INTO report_entry(user_id, entry_id, reason)
VALUES
    (1, 1, '标题和内容不符，误导读者'),
    (2, 3, '内容过于冗长，缺乏实际指导意义'),
    (3, 5, '内容抄袭他人，缺乏原创性'),
    (4, 7, '标题与内容不相关，违反论坛规范'),
    (5, 2, '内容涉及政治敏感话题，不符合社区规定'),
    (6, 9, '广告性质的帖子，恶意推广商品'),
    (7, 10, '语言不文明，含有不当言辞'),
    (8, 4, '内容与话题不相关，偏离讨论主题'),
    (9, 6, '内容不专业，缺乏深度'),
    (10, 8, '过于商业化，缺乏讨论价值');
-- 插入举报评论数据
INSERT INTO report_comment(user_id, comment_id, reason)
VALUES
    (1, 1, '评论内容不符合社区规范，存在侮辱性言辞'),
    (2, 3, '评论内容偏离主题，且无关紧要'),
    (3, 5, '评论语言不文明，使用了脏话'),
    (4, 7, '评论存在恶意抄袭，未经原创'),
    (5, 8, '评论信息不实，误导他人'),
    (6, 9, '评论过于简短，缺乏建设性意见'),
    (7, 6, '评论带有广告性质，恶意推广商品'),
    (8, 2, '评论与帖子内容不符，无法理解'),
    (9, 4, '评论涉嫌人身攻击，内容恶俗'),
    (10, 10, '评论带有种族歧视内容');
-- 插入举报用户数据
INSERT INTO report_user(reporter_id, user_id, reason)
VALUES
    (1, 2, '该用户频繁发布低质量内容，扰乱论坛秩序'),
    (2, 3, '该用户恶意评论，影响他人体验'),
    (3, 4, '该用户侵犯了我的个人隐私，恶意散布我的个人信息'),
    (4, 5, '该用户涉嫌作弊行为，违反社区规则'),
    (5, 6, '该用户发布了恶意广告，干扰了正常讨论'),
    (6, 7, '该用户辱骂他人，行为恶劣'),
    (7, 8, '该用户发布不实言论，制造舆论冲突'),
    (8, 9, '该用户发布恶意链接，存在网络诈骗风险'),
    (9, 10, '该用户言辞激烈，情绪失控，多次发生口角'),
    (10, 1, '该用户没有遵守社区规范，发了很多无关内容');
-- 插入系统消息
INSERT INTO s_message(receiver_id, content)
VALUES
    (1, '您的账户已成功注册，请完成邮箱验证以启用您的账户。'),
    (2, '您的申请的条目《如何选课》已通过审核，现已发布。'),
    (3, '系统检测到您未完成设置个人资料，请尽快完善您的个人信息。'),
    (4, '您的申请已被管理员批准，您现在可以发布帖子。'),
    (5, '您在论坛中发布的帖子《计算机网络课程讨论》违反了社区规范，已被删除。'),
    (6, '您发布的评论《我觉得这个课程很有趣》已被审核通过。'),
    (7, '系统正在进行维护，预计将在 30 分钟后完成。'),
    (8, '您的账号登录地点发生异常，若不是您本人操作，请立即更改密码。'),
    (9, '论坛管理员已审核通过您的申请条目《操作系统入门》并发布。'),
    (10, '您的评论《这篇文章写得很好》已被删除，因违反论坛评论规定。');
INSERT INTO s_message(receiver_id, content)
VALUES
    (1, '您的密码已成功重置，请使用新密码登录。'),
    (1, '系统检测到您的账户登录地点异常，请检查是否为您本人操作。'),
    (1, '您的账户已通过安全验证，您现在可以进行敏感操作。'),
    (1, '您的账户因违反社区规范已被临时冻结，详情请查看邮件通知。'),
    (1, '论坛管理员已批准您的申请，并允许您创建新的帖子。');
-- 插入用户之间的消息
INSERT INTO u_message(auther_id, receiver_id, content)
VALUES
    (1, 2, '嗨，看到你发的帖子了，内容挺不错的，能否分享一下相关资料？'),
    (2, 3, '你好，我看到你对“人工智能伦理”话题有些看法，想和你交流一下，能否约个时间聊聊？'),
    (3, 1, '感谢你的回复，我会按照你的建议进行修改，期待更多的交流。'),
    (4, 5, '你好，关于你申请的条目，我有些问题想问，能否具体说明一下内容？'),
    (5, 4, '我对你的评论有些不同意见，咱们能否探讨一下？'),
    (6, 7, '你好，我看到你发的评论有点过于苛刻了，希望你能给我一些建设性的建议。'),
    (7, 6, '你好，关于你对《操作系统》话题的看法，我认为你的分析有点片面，我们可以再聊聊吗？'),
    (8, 9, '你好，我发现你在评论中使用了不当的语言，希望下次注意一下。'),
    (9, 8, '非常抱歉，如果我的言辞让你不愉快，我会更加小心的。'),
    (10, 1, '我对你的帖子有些疑问，能不能详细说一下你的观点？');

INSERT INTO history(user_id, entry_id)
VALUES
    (1, 2),
    (1, 3),
    (3, 4),
    (2, 6),
    (1, 4),
    (1, 6);
