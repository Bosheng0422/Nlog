'''
Author: your name
Date: 2020-12-28 09:57:27
LastEditTime: 2021-01-12 06:44:47
LastEditors: Please set LastEditors
Description: In User Settings Editgn
FilePath: \2011cw2\app\views.py
'''
from flask import render_template, request, redirect, flash, url_for, make_response, session
from app import app, db ,admin
from .forms import UserForm,ArticleForm
from .models import User,Article,Category,collect_article,Comment,CommentReply
from werkzeug.utils import secure_filename
from flask_admin.contrib.sqla import ModelView
import logging
import os
import uuid


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Article, db.session))
admin.add_view(ModelView(Comment, db.session))
admin.add_view(ModelView(CommentReply, db.session))
admin.add_view(ModelView(Category, db.session))


try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

# enable to redirect back 
def redirect_back(default='blog.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))

@app.route('/login', methods=['POST', 'GET'])
def login():
    v=False
    username = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = User.query.all()
        for user in users:
            if user.username == username:
                v = True
                if user.password == password:
                    session['username']=username
                    break
                else:
                    flash('This password is incorrect.')
                    return redirect("/")
        if v == False:
            flash('This username do not exist.')
            return redirect_back(value=v)

    return redirect_back(value=v)

#blog signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form=UserForm()
    if request.method == 'POST':
        if User.query.filter(User.username == form.username.data).count() != 0 :
            flash("This username has been registered , please change")
            app.logger.info("signup:username: %s registered",form.username.data)
            redirect("/signup")
        u = User(username = form.username.data, password = form.password.data, blogname=form.blogname.data)
        db.session.add(u)
        db.session.commit()
        app.logger.info("signup:username: %s register successfully",form.username.data)
        return redirect("/")
    return render_template("signup.html", form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect("/")

@app.route('/passwordedit', methods=['GET', 'POST'])
def passwordedit():
    if request.method == 'POST':
        uname=request.form.get("uname")
        opwd=request.form.get("opwd")
        npwd=request.form.get("npwd")
        cpwd=request.form.get("cpwd")
        if 'username' not in session:
            v = 0
            flash("Log in before editing your password")
            app.logger.info("password edit:not login")
            return redirect('/')
        else:
            if uname == session['username']:
                user=User.query.filter(uname == User.username).first()
                if opwd == user.password:
                    if npwd == cpwd:
                        user.password=npwd
                        db.session.commit()
                        app.logger.info("%s password edit succesfully",uname)
                        return redirect_back()
                    else:
                        app.logger.warning("%s password edit: two new password match failed",uname)
                        flash("Two input new password are different ")
                else:
                    app.logger.warning("%s password edit: old password incorrect",uname)
                    flash("Password is incorrect")
            else:
                app.logger.warning("%s password edit: username input incorrect",uname)
                flash("Username is not correct please input your login username")
                
    return render_template("passwordedit.html")

#blog homepage
@app.route('/', methods=['GET', 'POST'])
def home():
    value = False
    if 'username' not in session:
        v = False
        blogid=0
        app.logger.info("haven't login")
    else:
        v = True
        blog=User.query.filter(User.username==session['username']).first()
        blogid=blog.id
    articles = Article.query.filter().all()
    return render_template("home.html",valuehome=v,blogid=blogid,articles=articles,same=False,coll=True)


#view the articles of the blog
@app.route('/articleslist/<int:user_id>', methods=['GET', 'POST'])
def articleslist(user_id):
    same = False
    if 'username' not in session:
        v = 0
    else:
        v = 1
        a = User.query.filter(User.username == session['username']).first()
        if a.id == user_id:
            same = True
    blogn = User.query.filter(User.id == user_id).first()
    articles = Article.query.filter(Article.author_id == user_id)
    if articles.count() ==0:
        flash("This blog has not article.")
    categories=dict()
    for c in a.categories:
        ca={c:0}
        categories.update(ca)
    for a in articles:
        c=Category.query.filter(Category.id == a.category_id).first()
        a=Article.query.filter(Article.category_id == c.id).count()
        ca={c:a}
        categories.update(ca)
    return render_template("articleslist.html",title=blogn.blogname,
        value=v,articles = articles,same = same,blog=blogn,categories=categories,blogid=blogn.id)

#write article page
def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename

@app.route('/writearticle', methods=['GET', 'POST'])
def writearticle():
    user = User.query.filter().first()
    if 'username' not in session:
        v = 0
        app.logger.info("haven't login!! cannot write article")
        return redirect('/')
    else:
        v = 1
        un=session['username']
    user = User.query.filter(User.username == un).first()
    cat = Category.query.filter().all()
    form=ArticleForm()
    app.logger.info("load succeed")
    if request.method == 'POST':
        app.logger.info("post succeed")
        if form.validate_on_submit():
            app.logger.info("article submit succeed")
            i = form.image.data
            filename = random_filename(i.filename)
            basepath = os.path.dirname(__file__)
            dirs = os.path.join(basepath, 'static/img/upload')
            if not os.path.exists(dirs):
                os.makedirs(dirs)
            upload_path = os.path.join(basepath, 'static/img/upload',secure_filename(filename))
            i.save(upload_path)
            upload_path = 'static/img/upload/' + filename
            a = Article(author_id=user.id,title=form.head.data,content = form.content.data,
            image=filename,author_name=un,category_id=form.category.data)
            db.session.add(a)
            db.session.commit()
            return redirect_back()
        else:
            app.logger.info("article form submit failed.")
    return render_template("writearticle.html",form=form,value=v,title=writearticle,blog=user,blogid=user.id,categories=cat,same=True)

#collected articles of the blog
@app.route('/collection/<int:user_id>', methods=['GET', 'POST'])
def collection(user_id):
    same=False
    if 'username' not in session:
        v = 0
    else:
        v = 1
        user = User.query.filter(User.id == user_id).first()
        loginuser = User.query.filter(User.username==session['username']).first()
        if user.id == loginuser.id:
            same=True
    return render_template("collected_articles.html",value=v,articles=user.articles,same=same)
    
    

@app.route('/article/<int:article_id>', methods=['GET', 'POST'])
def article(article_id):
    v = False
    s = False
    collected = False
    # find the article
    # avoid unbounderror : initial assignment
    article = Article.query.filter().first()
    article = Article.query.filter(Article.id == article_id).first()
    if article.comments.count() ==0:
        flash("No comment yet!")
    # find the category name
    cname = Category.query.filter(Category.id == article.category_id).first()
     # find the blog owner
    b = User.query.filter().first()
    b = User.query.filter(article.author_name == User.username).first()
    # error
    if article.id != article_id or b.username != article.author_name:
        return redirect("/")
    if 'username' not in session:
        v = False
    else:
        v = True
        # find the login user username and check if the blog owener is the login user
        sn = User.query.filter().first()
        sn = User.query.filter(User.username == session['username']).first()
        if sn.id == b.id:
            s=True      
        else:
            ar = Article.query.filter(Article.id==article_id).first()
            for u in ar.users:
                if u.id == sn.id:
                    collected = True
                else:
                    collected = False
    return render_template("article.html",title="article collection",blogid=b.id,
                    value=v,same=s,blog=b,article=article,collected=collected,cname=cname.category_name)
    
@app.route('/collected/<int:article_id>', methods=['GET', 'POST'])
def collected(article_id):
    if 'username' not in session:
        v = 0
        app.logger.info("haven't login")
        return redirect('/')
    else:
        v = 1
    sn = User.query.filter(User.username == session['username']).first()
    article = Article.query.filter(Article.id == article_id).first()
    if request.method == 'POST':
        sn.articles.remove(article)
        db.session.commit()
    return redirect_back()
    
@app.route('/collect/<int:article_id>', methods=['GET', 'POST'])
def collect(article_id):
    if 'username' not in session:
        v = 0
        app.logger.info("collect:have not login")
        return redirect_back()
    else:
        v = 1
    sn = User.query.filter(User.username == session['username']).first()
    article = Article.query.filter(Article.id == article_id).first()
    if request.method == 'POST':
        sn.articles.append(article)
        db.session.commit()
    return redirect_back()
    
@app.route('/delete/<int:article_id>', methods=['GET', 'POST'])
def delete(article_id):
    blogn = User.query.filter().first()
    blogn = User.query.filter(User.username == session['username']).first()
    if request.method == 'POST':
        ad=Article.query.filter().first()
        ad=Article.query.filter(ad.id==article_id).first()
        db.session.delete(ad)
        db.session.commit()
        return redirect("/articleslist/"+blogn.id)

@app.route('/comment/<int:article_id>', methods=['GET', 'POST'])
def comment(article_id):
    if 'username' not in session:
        value=0
        flash("Please log in to comment!")
        app.logger.info("comment:havenot login")
        return redirect_back()
    else:
        if request.method == 'POST':
            comment=request.form.get("com")
            c=Comment(content=comment,article_id=article_id,writter=session['username'])
            db.session.add(c)
            db.session.commit()
    return redirect_back()

@app.route('/reply/<int:comment_id>', methods=['GET', 'POST'])
def reply(comment_id):
    if 'username' not in session:
        value=0
        flash("Please log in to reply!")
        app.logger.info("reply:havenot login")
        return redirect_back()
    else:
        if request.method == 'POST':
            comment=request.form.get("rep")
            c=CommentReply(content=comment,comment_id=comment_id,writter=session['username'])
            db.session.add(c)
            db.session.commit()
    return redirect_back()

@app.route('/addcat', methods=['GET', 'POST'])
def addcat():
    if 'username' not in session:
        value=0
        app.logger.error("add category:havenot login")
        return redirect_back()
    else:
        if request.method == 'POST':
            newcat=request.form.get("newcat")
            if Category.query.filter(Category.category_name==newcat).count() !=0:
                flash("category is existed! Add failed.")
                app.logger.warning("add %s category failed:existed",newcat)
                return redirect_back()
        user=User.query.filter(User.username == session['username']).first()
        cat=Category(category_name = newcat,user_id=user.id)
        db.session.add(cat)
        db.session.commit()
        return redirect_back()