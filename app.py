import bson.errors
from bson import ObjectId
from flask import Flask, render_template, jsonify, request, abort
from pymongo import MongoClient
from datetime import datetime, timedelta
import jwt
import hashlib

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
            user = db.users.find_one({"id": payload["id"]}, {'_id': False})
            return render_template('index.html', posts=posts, id=user["id"])
        except jwt.ExpiredSignatureError:
            return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
        except jwt.DecodeError:
            return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})
    else:
        return render_template('index.html', posts=posts)

@app.route('/login_main')
def login_main():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

@app.route('/register', methods=['POST'])
def register_user():
    id_receive = request.form['id']
    pw_receive = request.form['pw']
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    doc = {
        "id": id_receive,
        "pw": pw_hash,
    }

    db.users.insert_one(doc)
    return jsonify({'result': 'success'})

@app.route('/register/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"id": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})

@app.route('/login', methods=['POST'])
def login():
    id_receive = request.form['id']
    pw_receive = request.form['pw']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'id': id_receive, 'pw': pw_hash})

    if result is not None:
        payload = {
         'id': id_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

@app.route('/posts', methods=['GET'])
def get_post_list():
    posts = list(db.post.find({}))
    for post in posts:
        post["_id"] = str(post["_id"])
    return jsonify({'posts': posts})

@app.route('/post', methods=['GET'])
def get_post():
    try:
        post_id_receive = request.args.get("post_id")
        post_id_valid_check(post_id_receive)
        post = db.post.find_one({'_id': ObjectId(post_id_receive)})
        post["_id"] = str(post["_id"])
        return render_template('post.html', post=post)
    except bson.errors.InvalidId:
        abort(404)

@app.route('/post', methods=['POST'])
def add_post():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        title_receive = request.form['title']
        content_receive = request.form['content']
        image_receive = request.form['image']
        user = db.users.find_one({"id": payload["id"]}, {'_id':False})

        doc = {
            'id': user["id"],
            'title': title_receive,
            'content': content_receive,
            'image': image_receive,
            'postDate': datetime.now()
        }

        db.post.insert_one(doc)
        return jsonify({'msg': '고민이 성공적으로 작성되었습니다.'})
    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})

@app.route('/comment', methods=['POST'])
def add_comment():

    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        user = db.users.find_one({"id": payload["id"]})
        post_id_receive = request.form['post_id']
        comment_receive = request.form['com']
        post_id_valid_check(post_id_receive)
        db.post.update_one({'_id': post_id_receive},
                           {'$push': {'comments': {'comment': comment_receive, 'id': user["id"]}}})
        return jsonify({'msg': '댓글이 작성되었습니다.'})
    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})

@app.route('/post', methods=['DELETE'])
def delete_post():
    # todo auth try-catch
    post_id_receive = request.form['post_id']

    post_id_valid_check(post_id_receive)
    db.post.delete_one({'_id': post_id_receive})
    return jsonify({'msg': '고민이 삭제되었습니다.'})

@app.route('/post', methods=['PUT'])
def update_post():
    # todo auth try-catch
    post_id_receive = request.form['post_id']
    title_receive = request.form['title']
    content_receive = request.form['content']
    image_receive = request.form['image']

    post_id_valid_check(post_id_receive)

    db.post.update_one({'_id': post_id_receive},{'$set': {'title': title_receive,'content': content_receive,'image': image_receive}})
    return jsonify({'msg': '고민이 수정되었습니다.'})

@app.route('/like', methods=['POST'])
def like_post():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        user = db.users.find_one({"id": payload["id"]})
        action_receive = request.form["action"]
        post_id_receive = request.form["post_id"]
        post_id_valid_check(post_id_receive)

        like = db.likes.find_one({"post_id": post_id_receive, "id": user["id"]})

        if action_receive == "like":
            if like is None :
                doc = {
                    "post_id": post_id_receive,
                    "id": user["id"],
                    "like": 1
                }
                db.likes.insert_one(doc)
            else:
                db.likes.update_one({"post_id": post_id_receive, "id": user["id"]}, {"$set": {"like": 1}})
        else:
            if like is None:
                doc = {
                    "post_id": post_id_receive,
                    "id": user["id"],
                    "like": -1
                }
                db.likes.insert_one(doc)
            else:
                db.likes.update_one({"post_id": post_id_receive}, {"id": user["id"]}, {"$set": {"like": -1}})

        like_count = db.likes.count({"post_id": post_id_receive, "like": 1})
        unlike_count = db.likes.count({"post_id": post_id_receive, "like": -1})
        return jsonify({"result": "success", 'msg': 'updated', "like_count": like_count, "unlike_count": unlike_count})
    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})


@app.route('/unlike', methods=['POST'])
def unlike_post():
    post_id_receive = request.form['post_id']
    post_id_valid_check(post_id_receive)
    db.post.update_one({'_id': post_id_receive}, {'$inc': {'unlike':1}})
    return jsonify({'msg': '비추천.'})

def post_id_valid_check(post_id):
    if db.post.find_one({'_id': ObjectId(post_id)}) is None:
        abort(404)
    return

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)