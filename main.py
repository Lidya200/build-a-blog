from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Build-a-blog:zxcv@localhost:8889/Build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(1000))


    def __init__(self, title, content):
        self.title = title
        self.content = content

@app.route("/blog", methods=["POST", "GET"])
@app.route('/', methods=['POST', 'GET'])
def index():




    if request.method == 'POST':
        error_title = ""
        error_content =""
        blog_title = request.form['title']
        blog_content = request.form['content']
        if len(blog_title) >=120 or len(blog_title) ==0:
            error_title = "Your title length exceeds the limit, please shorten your title."
            blog_title =""
        if len(blog_content) >=1000 or len(blog_content) ==0:
            error_content = "your content length exceeds the limit, please shorten your content."
            blog_content = ""
        if len(error_title)>0 or len(error_content)>0:
            return render_template('index.html', title= blog_title, content= blog_content, error_title=error_title, error_content=error_content)
        else:
            new_task = Blog(blog_title, blog_content)
            db.session.add(new_task)
            db.session.commit()
            return redirect("/blog_page?id=" +str(new_task.id))

    else:
        posts = Blog.query.all()
        

 
    return render_template('blog.html', posts= posts)

@app.route('/newpost', methods=['post', 'get'])
def add():

    post = ""
    new_blog = ""
    if request.method == "POST":
        #blog_id = request.form['id']
        blog_title = request.form['title']
        blog_content = request.form['content']

        new_blog = Blog(blog_title, blog_content)
        db.session.add(new_blog)
        db.session.commit()

        blog_id = new_blog.id
       
        return redirect("/singlepost?id=" + str(blog_id))

    return render_template("newpost.html", post=new_blog)

@app.route("/singlepost")
def singlepost():
    
    posts = db.session.query(Blog)
    post = ""
    for post in posts:
        post = post
    return render_template("single_post.html", post=post)
if __name__ == '__main__':
    app.run()