from bson import ObjectId
from flask import Flask, render_template, jsonify, request, abort, Response
from pymongo import MongoClient
from datetime import datetime, timedelta
import jwt
import hashlib


## AWS DB 접속
#client = MongoClient('mongodb://test:test@localhost', 27017)
client = MongoClient('localhost', 27017)
db = client.honorablejudge
app = Flask(__name__)

SECRET_KEY = '99judge2'

@app.route('/')
def main():
    token_receive = request.cookies.get('mytoken')

    posts = list(db.post.find({}))
    for post in posts:
        post["_id"] = str(post["_id"])

    if token_receive is not None:
        try:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            user = db.users.find_one({"user_id": payload["user_id"]}, {'_id': False})
            return render_template('index.html', posts=posts, id=user["user_id"])
        except jwt.ExpiredSignatureError:
            msg = '로그인 시간이 만료되었습니다.'
            return render_template('401.html', msg=msg), 401
        except jwt.DecodeError:
            msg = '로그인 정보가 존재하지 않습니다.'
            return render_template('401.html', msg=msg), 401
    else:
        return render_template('index.html', posts=posts)


@app.route('/login_main')
def login_main():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

@app.route('/mypage')
def mypage():
    token_receive = request.cookies.get('mytoken')

    if token_receive is not None:
        try:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            user = db.users.find_one({"user_id": payload["user_id"]}, {'_id': False})

            posts = list(db.post.find({'user_id': user["user_id"]}))
            for post in posts:
                post["_id"] = str(post["_id"])
                post["like"] = db.likes.count_documents({"post_id": post["_id"], "like": 1})
                post["unlike"] = db.likes.count_documents({"post_id": post["_id"], "like": -1})

            comments = list(db.comment.find({'user_id': user["user_id"]}))
            for comment in comments:
                comment["_id"] = str(comment["_id"])
                post = db.post.find_one({"_id": ObjectId(comment["post_id"])})
                comment["post_title"] = post["title"]

            return render_template('mypage.html', posts=posts, comments=comments, id=user["user_id"], page_size=10)
        except jwt.ExpiredSignatureError:
            msg = '로그인 시간이 만료되었습니다.'
            return render_template('401.html', msg=msg), 401
        except jwt.DecodeError:
            msg = '로그인 정보가 존재하지 않습니다.'
            return render_template('401.html', msg=msg), 401
    else:
        return render_template('index.html')

@app.route('/register', methods=['POST'])
def register_user():
    user_id_receive = request.form['user_id']
    pw_receive = request.form['pw']
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    if is_user_id_exist(user_id_receive):
        return Response(response='이미 존재하는 ID 입니다. 중복 확인을 다시 해주세요.', status=400)
    else:
        doc = {
            "user_id": user_id_receive,
            "pw": pw_hash,
        }

        db.users.insert_one(doc)
        return jsonify({'result': 'success'})


@app.route('/register/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"user_id": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})


@app.route('/login', methods=['POST'])
def login():
    user_id_receive = request.form['user_id']
    pw_receive = request.form['pw']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'user_id': user_id_receive, 'pw': pw_hash})

    if result is not None:
        payload = {
            'user_id': user_id_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

@app.route('/posts', methods=['GET'])
def get_post_list():
    user_id_receive = request.args.get('user_id')

    if user_id_receive is None:
        posts = list(db.post.find({}))
        for post in posts:
            post["_id"] = str(post["_id"])
            post["postDate"] = str(post["postDate"])
            post["like"] = db.likes.count_documents({"post_id": post["_id"], "like": 1})
            post["unlike"] = db.likes.count_documents({"post_id": post["_id"], "like": -1})
        return jsonify({'posts': posts})
    else:
        posts = list(db.post.find({"user_id": user_id_receive}))
        for post in posts:
            post["_id"] = str(post["_id"])
            post["postDate"] = str(post["postDate"])
            post["like"] = db.likes.count_documents({"post_id": post["_id"],"user_id": user_id_receive, "like": 1})
            post["unlike"] = db.likes.count_documents({"post_id": post["_id"],"user_id": user_id_receive,  "like": -1})
        return jsonify({'posts': posts})

@app.route('/post', methods=['GET'])
def get_post():
    token_receive = request.cookies.get('mytoken')

    post_id_receive = request.args.get("post_id")
    post_id_valid_check(post_id_receive)
    post = db.post.find_one({'_id': ObjectId(post_id_receive)})
    post["_id"] = str(post["_id"])

    comments = list(db.comment.find({'post_id': post_id_receive}))
    for comment in comments:
        comment["_id"] = str(comment["_id"])

    like_count = db.likes.count({"post_id": post_id_receive, "like": 1})
    unlike_count = db.likes.count({"post_id": post_id_receive, "like": -1})

    if token_receive is not None:
        try:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            user = db.users.find_one({"user_id": payload["user_id"]}, {'_id': False})
            return render_template('post.html', post=post, comments=comments, like_count=like_count, unlike_count=unlike_count, user_id=user["user_id"])
        except jwt.ExpiredSignatureError:
            msg = '로그인 시간이 만료되었습니다.'
            return render_template('401.html', msg=msg), 401
        except jwt.DecodeError:
            msg = '로그인 정보가 존재하지 않습니다.'
            return render_template('401.html', msg=msg), 401
    else:
        return render_template('post.html', post=post, comments=comments, like_count=like_count, unlike_count=unlike_count)

@app.route('/post', methods=['POST'])
def add_post():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user = db.users.find_one({"user_id": payload["user_id"]}, {'_id': False})

        title_receive = request.form['title']
        content_receive = request.form['content']
        content_receive = content_receive.replace('\n', '<br>')
        image_receive = request.form['image']

        doc = {
            'user_id': user["user_id"],
            'title': title_receive,
            'content': content_receive,
            'image': image_receive,
            'postDate': datetime.now(),
            'view': 0
        }
        db.post.insert_one(doc)

        return jsonify({'msg': '고민이 성공적으로 작성되었습니다.'})
    except jwt.ExpiredSignatureError:
        msg = '로그인 시간이 만료되었습니다.'
        return render_template('401.html', msg=msg), 401
    except jwt.DecodeError:
        msg = '로그인 정보가 존재하지 않습니다.'
        return render_template('401.html', msg=msg), 401

@app.route('/view', methods=['POST'])
def plus_post_view():
    post_id_receive = request.form["post_id"]
    post_id_valid_check(post_id_receive)
    db.post.update_one({'_id': ObjectId(post_id_receive)}, {'$inc': {'view': 1}})
    return jsonify({'msg': '조회수 추가.'})

@app.route('/post/update')
def load_update_page():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user = db.users.find_one({"user_id": payload["user_id"]}, {'_id': False})

        post_id_receive = request.args.get("post_id")
        post_id_valid_check(post_id_receive)
        if is_post_owner(post_id_receive, user):
            post = db.post.find_one({'_id': ObjectId(post_id_receive)})
            post["_id"] = str(post["_id"])
            return render_template('edit.html', post=post)
        else:
            return Response(response='해당 글에 대한 권한이 없습니다.', status=403)
    except jwt.ExpiredSignatureError:
        msg = '로그인 시간이 만료되었습니다.'
        return render_template('401.html', msg=msg), 401
    except jwt.DecodeError:
        msg = '로그인 정보가 존재하지 않습니다.'
        return render_template('401.html', msg=msg), 401

@app.route('/post', methods=['PUT'])
def update_post():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user = db.users.find_one({"user_id": payload["user_id"]})

        post_id_receive = request.form['post_id']
        title_receive = request.form['title']
        content_receive = request.form['content']
        content_receive = content_receive.replace('\n', '<br>')
        image_receive = request.form['image']

        post_id_valid_check(post_id_receive)
        if is_post_owner(post_id_receive, user):
            db.post.update_one({'_id': ObjectId(post_id_receive)},
                               {'$set': {'title': title_receive, 'content': content_receive, 'image': image_receive}})
            return jsonify({'msg': '고민이 수정되었습니다.'})
        else:
            return Response(response='해당 글에 대한 권한이 없습니다.', status=403)
    except jwt.ExpiredSignatureError:
        msg = '로그인 시간이 만료되었습니다.'
        return render_template('401.html', msg=msg), 401
    except jwt.DecodeError:
        msg = '로그인 정보가 존재하지 않습니다.'
        return render_template('401.html', msg=msg), 401

@app.route('/post', methods=['DELETE'])
def delete_post():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user = db.users.find_one({"user_id": payload["user_id"]})

        post_id_receive = request.form['post_id']

        post_id_valid_check(post_id_receive)
        if is_post_owner(post_id_receive, user):
            db.post.delete_one({'_id': ObjectId(post_id_receive)})
            return jsonify({'msg': '고민이 삭제되었습니다.'})
        else:
            return Response(response='해당 글에 대한 권한이 없습니다.', status=403)

    except jwt.ExpiredSignatureError:
        msg = '로그인 시간이 만료되었습니다.'
        return render_template('401.html', msg=msg), 401
    except jwt.DecodeError:
        msg = '로그인 정보가 존재하지 않습니다.'
        return render_template('401.html', msg=msg), 401

@app.route('/comment', methods=['POST'])
def add_comment():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user = db.users.find_one({"user_id": payload["user_id"]})

        post_id_receive = request.form['post_id']
        comment_receive = request.form['comment']
        comment_receive = comment_receive.replace('\n', '<br>')
        create_date_receive = request.form['create_date']
        post_id_valid_check(post_id_receive)

        doc = {
            'user_id': user["user_id"],
            'post_id': post_id_receive,
            'comment': comment_receive,
            'create_date': create_date_receive
        }

        db.comment.insert_one(doc)
        return jsonify({'msg': '댓글이 작성되었습니다.'})
    except jwt.ExpiredSignatureError:
        msg = '로그인 시간이 만료되었습니다.'
        return render_template('401.html', msg=msg), 401
    except jwt.DecodeError:
        msg = '로그인 정보가 존재하지 않습니다.'
        return render_template('401.html', msg=msg), 401


@app.route('/comment', methods=['DELETE'])
def delete_comment():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user = db.users.find_one({"user_id": payload["user_id"]})

        post_id_receive = request.form['post_id']
        comment_id_receive = request.form['comment_id']

        post_id_valid_check(post_id_receive)

        if is_comment_owner(comment_id_receive, user):
            db.comment.delete_one({'_id': ObjectId(comment_id_receive)})
            return jsonify({'msg': '댓글이 제거되었습니다.'})
        else:
            return Response(response='해당 댓글에 대한 권한이 없습니다.', status=403)
    except jwt.ExpiredSignatureError:
        msg = '로그인 시간이 만료되었습니다.'
        return render_template('401.html', msg=msg), 401
    except jwt.DecodeError:
        msg = '로그인 정보가 존재하지 않습니다.'
        return render_template('401.html', msg=msg), 401

@app.route('/like', methods=['POST'])
def like_post():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user = db.users.find_one({"user_id": payload["user_id"]})

        post_id_receive = request.form["post_id"]
        action_receive = request.form["action"]

        post_id_valid_check(post_id_receive)
        like = db.likes.find_one({"post_id": post_id_receive, "user_id": user["user_id"]})
        if action_receive == "like":
            if like is None:
                doc = {
                    "post_id": post_id_receive,
                    "user_id": user["user_id"],
                    "like": 1
                }
                db.likes.insert_one(doc)
            else:
                db.likes.update_one({"post_id": post_id_receive, "user_id": user["user_id"]}, {"$set": {"like": 1}})
        else:
            if like is None:
                doc = {
                    "post_id": post_id_receive,
                    "user_id": user["user_id"],
                    "like": -1
                }
                db.likes.insert_one(doc)
            else:
                db.likes.update_one({"post_id": post_id_receive, "user_id": user["user_id"]}, {"$set": {"like": -1}})

        like_count = db.likes.count({"post_id": post_id_receive, "like": 1})
        unlike_count = db.likes.count({"post_id": post_id_receive, "like": -1})

        return jsonify({"result": "success", 'msg': 'updated', "like_count": like_count, "unlike_count": unlike_count})
    except jwt.ExpiredSignatureError:
        msg = '로그인 시간이 만료되었습니다.'
        return render_template('401.html', msg=msg), 401
    except jwt.DecodeError:
        msg = '로그인 정보가 존재하지 않습니다.'
        return render_template('401.html', msg=msg), 401

def is_user_id_exist(user_id):
    return db.users.find_one({'user_id': user_id}) is not None

def post_id_valid_check(post_id):
    if db.post.find_one({'_id': ObjectId(post_id)}) is None:
        abort(404)
    return

def is_post_owner(post_id, user):
    post = db.post.find_one({'_id': ObjectId(post_id)})
    return post["user_id"] == user["user_id"]

def is_comment_owner(comment_id, user):
    comment = db.comment.find_one({'_id': ObjectId(comment_id)})
    return comment["user_id"] == user["user_id"]

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
