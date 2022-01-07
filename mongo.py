import os
from flask import Flask, jsonify, request, json,send_file,redirect,url_for,session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from bson.json_util import dumps
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from werkzeug.utils import secure_filename
from io import BytesIO

app = Flask(__name__)
app.config["MONGO_URI"] = os.environ.get("MONGODB_URI")
# app.config["MONGO_URI"] = "mongodb://localhost:27017/final"
app.config['MONGO_DBNAME'] = 'final'
app.config['JWT_SECRET_KEY'] = 'secret'
app.config['SECRET_KEY'] ='super-secret'


mongo = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

CORS(app)

@app.route('/users/register',methods=['POST'])
def register():
    users = mongo.db.users
    username = request.json['username']
    email = request.json['email']
    passwordtest=request.json['password']
    password = bcrypt.generate_password_hash(passwordtest).decode('utf-8')
    created = datetime.utcnow()
    if username =='':
        resp = jsonify({"msg":'username can not be empty'})
        return resp
    if email =='':
        resp = jsonify({"msg":'invalid email'})
        return resp
    if len(passwordtest) < 6:
            resp = jsonify({"msg":'Make sure your password is at least 6 letters'})
            return resp
    existing_users = users.find_one({'email':request.json['email']})
    if existing_users is None:
        user_id = users.insert({
            'username':username,
            'email':email,
            'password':password,
            'file':'images/userProfile.png',
            'created':created
        })
        resp=jsonify({"msg":'registered successfully!', "success":"true"})
        return resp
    resp = jsonify({"msg":'user already exists!'})
    return resp

@app.route('/users/login',methods=['POST'])
def login():
    users = mongo.db.users
    email = request.json['email']
    password = request.json['password']
    result = ""
    login_user = users.find_one({'email':email})

    if login_user:
        if bcrypt.check_password_hash(login_user['password'],password):
            access_token = create_access_token(identity = {
            'username':login_user['username'],
            'email':login_user['email'],
            'file':login_user['file'],
            })
            result = jsonify({'token':access_token})

        else:
            result = jsonify({"msg":'Invalid username and password'})
    else:
        result = jsonify({"msg":"No results found"})

                
    return result


@app.route('/profile')
def profile():
    users = mongo.db.users
    login_user = users.find(email=session['email'])
    result = jsonify({'firstname' :login_user['username']+'email' +login_user['email']})
    return result
    



@app.route('/users/update',methods=['POST'])  #for update the user (username, password )
def update():
    if request.method == 'POST':
        users = mongo.db.users
        # _id = id
        email = request.json['email']
        the_user = users.find_one({"email":email})
        username = request.json['username']
        password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8')
        confirmpassword = request.json['confirmpassword']
        if request.json['password'] == confirmpassword:
            user_id=the_user['_id']
            update_postsUsername=mongo.db.posts.update_many({'user_id': user_id},{'$set':{'username':username}})

            update_comment= mongo.db.posts.update_many ({'comments.0.user_id':user_id},{'$set':{"comments.0.username":username}})
            update_comment= mongo.db.posts.update_many ({'comments.1.user_id':user_id},{'$set':{"comments.1.username":username}})
            update_comment= mongo.db.posts.update_many ({'comments.2.user_id':user_id},{'$set':{"comments.2.username":username}})
            update_comment= mongo.db.posts.update_many ({'comments.3.user_id':user_id},{'$set':{"comments.3.username":username}})
            update_comment= mongo.db.posts.update_many ({'comments.4.user_id':user_id},{'$set':{"comments.4.username":username}})
            update_comment= mongo.db.posts.update_many ({'comments.5.user_id':user_id},{'$set':{"comments.5.username":username}})
            update_comment= mongo.db.posts.update_many ({'comments.6.user_id':user_id},{'$set':{"comments.6.username":username}})
            update_comment= mongo.db.posts.update_many ({'comments.7.user_id':user_id},{'$set':{"comments.7.username":username}})
            update_comment= mongo.db.posts.update_many ({'comments.8.user_id':user_id},{'$set':{"comments.8.username":username}})
            update_comment= mongo.db.posts.update_many ({'comments.9.user_id':user_id},{'$set':{"comments.9.username":username}})
            update_comment= mongo.db.posts.update_many ({'comments.10.user_id':user_id},{'$set':{"comments.10.username":username}})
            # work on here later instead of code above how to use loop
            # allposts = mongo.db.posts.find()

            # allposts = dumps(allposts)

            # i = 0
            # j = 0

            # while i < len(allposts):
            #         while j < len(allposts[i][comments]):
            #             update_comment= mongo.db.posts.update_many({'comments.'j'.user_id':user_id},{'$set':{"comments."j".username":username}})
            #         j += 1
            #     i += 1

            update_user= mongo.db.users.update_one({'email':email},{'$set':{'username':username,'password':password}})
            resp=jsonify({'msg':'updated successfully!!', 'success':'true'})
            return resp
        else: 
            resp= jsonify({'msg':'password not match !', 'success':'false'})
            return resp
   
    

@app.route('/updatefile',methods=['POST']) #update the file
def updateFile():
    if request.method == 'POST':
        posts = mongo.db.posts
       
        id = ObjectId(request.form['id'])
        file = request.files['file']
        if file.filename == '':
            resp = jsonify({'msg' : 'No file selected for uploading'})
            return resp
        mongo.save_file(file.filename,file)
    
        posts.update_one({ '_id': id}, { '$set' :{'file':file.filename}})
        resp = jsonify('you have updated the post!')
        return resp


@app.route('/users/post',methods=['POST']) # add a new post according to the user
def post():
    if request.method == 'POST':
        users = mongo.db.users
        the_user = users.find_one({"email":request.form['email']})
        date = datetime.utcnow()

        posts = mongo.db.posts
        title = request.form['title']
        content = request.form['content']
        category = request.form['category']
        file = request.files['file']
        if file.filename == '':
            resp = jsonify({'msg' : 'No file selected for uploading'})
            return resp
        mongo.save_file(file.filename,file)

      
        post = posts.insert({"title":title,"content":content,"category":category,
        'file':file.filename,'user_id':the_user['_id'],'username':the_user['username'],
        'userImage':the_user['file'],
        'date':date,'like':[], 'dislike':[] , 'comments':[]})
        resp = jsonify({'msg':'you have added new post!'})
        return resp



  
   

@app.route('/users/posts',methods=['GET']) #to get all the posts
def get_posts():
    posts = mongo.db.posts.find()
    resp = dumps(posts)
    return resp


@app.route('/get_post',methods=['POST']) #get all post specific for a user
def get_post():
    
    users = mongo.db.users
    the_user = users.find_one({"email":request.json['email']})

    posts = mongo.db.posts
    user_post = posts.find({'user_id':the_user['_id']})
    post_list =''
    resp = dumps(user_post)
    return resp


    



@app.route('/file/<filename>')  #to download the file given a filename
def file(filename):
    return mongo.send_file(filename)

@app.route('/updatepost',methods=['POST']) #update the post: title, content, category,file
def updatePost():
    if request.method == 'POST':
        posts = mongo.db.posts
        title = request.form['title']
        content = request.form['content']
        category = request.form['category']
        id = ObjectId(request.form['id'])
       

        posts.update_one({ '_id': id}, { '$set' :{'title':title,'content':content,'category':category}})
        resp = jsonify('you have updated the post!')
        return resp



@app.route('/deletepost',methods=['DELETE']) #delete the post
def delete():
        posts = mongo.db.posts
        id = ObjectId(request.json['id'])
        the_post = posts.find_one({"_id":id })
        posts.delete_one({'_id':id})
        resp = jsonify({'msg':'post deleted'})
        return resp

@app.route('/addcomment',methods=['POST']) # need to pass in email, comment and id of the post
def add_comment():
      if request.method == 'POST':
        users = mongo.db.users
        the_user = users.find_one({"email":request.json['email']})
        date = datetime.utcnow()

        posts = mongo.db.posts
        id = ObjectId(request.json['id'])

        posts.update({ '_id': id}, { '$push': {'comments':{   '$each': [ { "comment":request.json['comment'],"username":the_user['username'],"user_id":the_user['_id'],'date':date } ] }}} )
        resp = jsonify({'msg':'you have added new comment!'})
        return resp

@app.route('/getcomments',methods=['POST']) #for specific post
def get_comments():
    if request.method == 'POST':
        posts = mongo.db.posts
        id = ObjectId(request.json['id'])

        the_post = posts.find_one({"_id":id })

        comments = mongo.db.comments
        post_comment = comments.find({'post_id':the_post['_id']})
        resp = dumps(post_comment)
        return resp


@app.route('/plusLike',methods=['POST']) #add 1 to the like counter of a specific post
def plusLike():
      if request.method == 'POST':
        users = mongo.db.users
        the_user = users.find_one({"email":request.json['email']})
        posts = mongo.db.posts
        id = ObjectId(request.json['id'])
        # check if the user has liked before or not
        repeatedUser = posts.find_one({'_id': id})
        exist='false'
        repeated='false'
        i = 0
        j = 0

        while i < len(repeatedUser['like']):
            if repeatedUser['like'][i]['user_id'] == the_user['_id']:
                # exist='true'
                repeated='true'
            i += 1
        if  repeated=='true':
            posts.update({ '_id': id},{ '$pull': {'like':{"user_id":the_user['_id']}}})
            return jsonify({'msg':'done!' })
        else:
            while j < len(repeatedUser['dislike']):
                repeatedId=repeatedUser['dislike'][j]['user_id']
                if repeatedId == the_user['_id']:
                    exist='true'
                j += 1

        if exist == 'false':
            posts.update({ '_id': id}, { '$push': {'like':{'$each': [ {"username":the_user['username'],"user_id":the_user['_id'] } ] }}} )
            resp = jsonify({'msg':'liked User successfully added!' })
        else:
            resp = jsonify({'displaymsg':'you can like or dislike just once on each post'})
        return resp


@app.route('/plusDislike',methods=['POST']) #add 1 to the dislike counter of a specific post
def plusDislike():
    if request.method == 'POST':
      if request.method == 'POST':
        users = mongo.db.users
        the_user = users.find_one({"email":request.json['email']})

        posts = mongo.db.posts
        id = ObjectId(request.json['id'])
        # check if the user has disliked before or not
        repeatedUser = posts.find_one({'_id': id})

        exist='false'
        repeated='false'

        i = 0
        j = 0
        while i < len(repeatedUser['dislike']):
            repeatedId=repeatedUser['dislike'][i]['user_id']
            if repeatedId == the_user['_id']:
                # exist='true'
                repeated='true'
            i += 1
        if  repeated=='true':
            posts.update({ '_id': id},{ '$pull': {'dislike':{"user_id":the_user['_id']}}})
            return jsonify({'msg':'done!' })
        else:
            while j < len(repeatedUser['like']):
                if repeatedUser['like'][j]['user_id'] == the_user['_id']:
                    exist='true'
                j += 1


        if exist == 'false':
            posts.update({ '_id': id}, { '$push': {'dislike':{'$each': [ {"username":the_user['username'],"user_id":the_user['_id'] } ] }}} )
            resp = jsonify({'msg':'unliked User successfully added!'})
        else:
            resp = jsonify({'displaymsg':'you can like or dislike just once on each post'})
        return resp

@app.route('/profileUpload',methods=['POST']) # add a new post according to the user
def imageUpload():
    if request.method == 'POST':
        users = mongo.db.users
        email = request.form['email']
        file = request.files['file']
        mongo.save_file(file.filename,file)
        update_user= mongo.db.users.update_one({'email':email},{'$set':{'file':file.filename}})

        # update posts img
        the_user = users.find_one({"email":email})
        user_id=the_user['_id']
        userImg = the_user['file']
        update_postsUserImg=mongo.db.posts.update_many({'user_id': user_id},{'$set':{'userImage':userImg}})
        # end of update posts img

        login_user = users.find_one({'email':email})
        access_token = create_access_token(identity = {
            'username':login_user['username'],
            'email':login_user['email'],
            'file':login_user['file'],
            })
        result = jsonify({'token':access_token})

        resp = jsonify({'msg':'you have added new profile image!'})
        return result

@app.route('/')  #check connectivity
def connected():
    return'''
    <html>
        <h1>Connected to FlaskPro-Group Project Backend Side!!!</h1>
    </html
    '''


if __name__ == '__main__':
    app.run(debug =True )
