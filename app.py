from flask import Flask, jsonify, request
from cs50 import SQL
from os import path

app = Flask(__name__)

# Create DB
if not path.exists('data.db'):
  open('data.db', 'w').close()

# Connect to DB, Create tables
db = SQL('sqlite:///data.db')
db.execute('''
  create table if not exists posts (
    id integer primary key autoincrement not null,
    title text not null,
    content text not null,
    author text not null,
    createdDate text not null,
    likes integer not null default 0,
    shares integer not null default 0
  );
''')
db.execute('''
  create table if not exists images (
    id integer primary key autoincrement not null,
    title text not null,
    imageUrl text not null,
    author text not null,
    createdDate text not null,
    likes integer not null default 0,
    shares integer not null default 0
  )
''')


@app.route('/latest-posts')
def latestPosts():
  posts = db.execute('''
    select * from posts order by id desc limit 100
  ''')

  return jsonify(posts), 200

@app.route('/create-post', methods=['POST'])
def createPost():
  title = request.form.get('title')
  content = request.form.get('content')
  author = request.form.get('author')
  createdDate = request.form.get('createdDate')

  if not title or not content or not author or not createdDate:
    return 'error: missing data', 400

  db.execute('''
    insert into posts (title, content, author, createdDate)
    values (?, ?, ?, ?)
  ''', title, content, author, createdDate)

  return 'success', 201


@app.route('/like-post', methods=['POST'])
def likePost():
  postId = request.form.get('postId')

  if not postId:
    return 'error: missing data', 400

  db.execute('''
    update posts set likes = likes + 1 where id = ?
  ''', postId)

  return 'success', 201


@app.route('/latest-images')
def latestImages():
  images = db.execute('''
    select * from images order by id desc limit 100
  ''')

  return jsonify(images), 200


@app.route('/upload-image', methods=['POST'])
def uploadImage():
  title = request.form.get('title')
  imageUrl = request.form.get('imageUrl')
  author = request.form.get('author')
  createdDate = request.form.get('createdDate')

  if not title or not imageUrl or not author or not createdDate:
    return 'error: missing data', 400

  db.execute('''
    insert into images (title, imageUrl, author, createdDate)
    values (?, ?, ?, ?)
  ''', title, imageUrl, author, createdDate)

  return 'success', 201


if __name__ == '__main__':
  app.run()
