from flask import Flask, jsonify, request, render_template as render
from cs50 import SQL
from os import path
from dataclasses import dataclass

@dataclass
class Shop:
  title: str
  subtitle: str
  imageName: str
  tint: str
  openUrl: str

shops: list[Shop] = [
  Shop(
    title="Temu",
    subtitle="I love child labor.",
    imageName="TemuLogo",
    tint="orange",
    openUrl="https://www.temu.com/"
  ),
  Shop(
    title="Amazon",
    subtitle="Fast shipping mommy.",
    imageName="AmazonLogo",
    tint="yellow",
    openUrl="https://www.amazon.com/"
  ),
  Shop(
    title="Shein",
    subtitle="Microtrend overdose.",
    imageName="SheinLogo",
    tint="red",
    openUrl="https://www.shein.com/"
  ),
  Shop(
    title="Vinted",
    subtitle="Second-hand slay.",
    imageName="VintedLogo",
    tint="green",
    openUrl="https://www.vinted.com/"
  )
]

@dataclass()
class UpgradeTier:
  title: str
  subtitle: str
  price: str
  features: list[str]

upgradeTiers: list[UpgradeTier] = [
  UpgradeTier(
    title="Premium",
    subtitle="Improved BIG Experience.",
    price="$9.99/mo",
    features=[
      "5% Less Ads",
      "Better Subway Surfers Gameplay"
    ]
  ),

  UpgradeTier(
    title="Pro",
    subtitle="Powerful BIG Experience.",
    price="$19.99/mo",
    features=[
      "15% Less Ads",
      "Built-in Shop",
      "Excellent Subway Surfers Gameplay",
      "Sigma Profile Widget"
    ]
  ),

  UpgradeTier(
    title="Ultra",
    subtitle="Ultimate BIG Experience.",
    price="$29.99/mo",
    features=[
      "20% Less Ads",
      "Built-in Shop",
      "Excellent Subway Surfers Gameplay",
      "Sigma Profile Widget",
      "Thank-you message"
    ]
  ),

  UpgradeTier(
    title="XTreme",
    subtitle="Extreme BIG Experience.",
    price="$69.99/mo",
    features=[
      "25% Less Ads",
      "Built-in Shop",
      "Excellent Subway Surfers Gameplay",
      "Sigma Profile Widget",
      "Thank-you message",
      "Miku Miku++"
    ]
  )
]

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


@app.route('/')
def index():
  posts = db.execute('''
    select * from posts order by id desc limit 100
  ''')

  return render("social.html", posts=posts)

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


@app.route('/picture')
def picture():
  images = db.execute('''
    select * from images order by id desc limit 100
  ''')

  return render("picture.html", images=images)


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


@app.route('/shop')
def shop():
  return render("shop.html", shops=shops)


@app.route('/detail')
def detail():
  postId = request.args.get('postId')
  if not postId:
    return render("post.html", error="no ID"), 400

  posts = db.execute('''
    select * from posts where id = ?  
  ''', postId)

  if len(posts) == 0:
    return render("post.html", error="post not found"), 404

  postTitle = posts[0]['title']
  return render("post.html", posts=posts, postTitle=postTitle)


@app.route('/upgrade')
def upgrade():
  return render("upgrade.html", tiers=upgradeTiers)

if __name__ == '__main__':
  app.run()
