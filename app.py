from flask import Flask,render_template,request
from flask_cors import cross_origin
from information import Person,Messages
import json
## Flask -----------------------------------------------------------------------

app = Flask(__name__)


@app.route('/login',methods=['GET','POST'])
@cross_origin()
def login():
    return render_template('login.html')

@app.route('/check_login',methods=["GET","POST"])
@cross_origin()
def check_login():
    email = request.form['email']
    password = request.form['password']

    client = Person()
    try:
        client.load_data()
        corr_email = client.email_id
        corr_password = client.password
        if(email == corr_email and password == corr_password):
            return render_template('admin.html')
    except:
        pass
    return render_template('login.html')

@app.route('/correct1',methods=['GET',"POST"])
@cross_origin()
def correct1():
    client = Person()
    try:
        if request.method=='POST':
            name = request.form['name']
            client.replace_name(name)
            return render_template('admin.html')
    except:
        pass
    return render_template('admin.html')

@app.route('/add_resume',methods = ['GET',"POST"])
@cross_origin()
def add_resume():
    try:
        if request.method=='POST':
            resume = request.form['resume']
            client = Person()
            client.replace_resume(resume)
        return render_template('admin.html')
    except:
        pass
    return render_template('admin.html')


@app.route('/correct2',methods=['GET',"POST"])
@cross_origin()
def correct2():
    client = Person()
    try:
        if request.method=='POST':
            about = request.form['about']
            client.replace_about(about)
            return render_template('admin.html')
    except:
        pass
    return render_template('admin.html')

@app.route('/correct3',methods=['GET',"POST"])
@cross_origin()
def correct3():
    client = Person()
    try:
        if request.method == 'POST':
            skill = request.form['skill']
            star = int(request.form['star'])
            client.add_skill(skill,star)
            return render_template('admin.html')
    except:
        pass
    return render_template('admin.html')


@app.route('/correct4',methods=['GET',"POST"])
@cross_origin()
def correct4():
    client = Person()
    try:
        if request.method == 'POST':
            skill = request.form['skill']
            client.remove_skill(skill)

            return render_template('admin.html')
    except Exception as e:
        print(e)
        pass
    return render_template('admin.html')




@app.route('/correct5',methods=['GET',"POST"])
@cross_origin()
def correct5():
    client = Person()
    try:
        if request.method == 'POST':
            new_project = {"title":request.form['title'],
                "tech_stack" : request.form['tech_stack'],
                "content" : request.form['content'],
                "github_link" : request.form['github_link'],
                "demo_link" : request.form['demo_link']
                }
            client.add_project(new_project)
            return render_template('admin.html')
    except:
        pass
    return render_template('admin.html')


@app.route('/correct6',methods=['GET',"POST"])
@cross_origin()
def correct6():
    client = Person()
    try:
        if request.method == 'POST':
            title = request.form['title']
            client.remove_project(title)
            return render_template('admin.html')
    except:
        pass
    return render_template('admin.html')


@app.route('/signin',methods = ['GET','POST'])
@cross_origin()
def signin():
    return render_template("signin.html")

@app.route('/add_user',methods=['GET','POST'])
@cross_origin()
def add_user():
    if request.method == 'POST':
        try:
            name = request.form["name"]
            email = request.form["email"]
            password = request.form["password"]

            client = Person()
            if (client.first_time_login()):
                client.reset_user(name,email,password)

            return render_template('login.html')
        except:
            pass
        return  render_template('singin.html')


## SEND FEEDBACK -------------------------------------------------------------------------------------------------------

@app.route('/mail',methods = ['GET','POST'])
@cross_origin()
def mail():
    client = Person()
    try:
        if request.method=='POST':
            mess = {
                "name" : request.form['name'],
                "email" : request.form['email'],
                "content" :request.form['text']
                }

            message_box = Messages()

            message_box.send_message(mess)
            # print(mess)
    except Exception as e:
        print(e)
        pass
    return render_template("home.html", name=client.name, image=client.image_file, about=client.about,
                           skills=client.skills, projects=client.projects, user=True)


@app.route("/reset",methods =["GET","POST"])
@cross_origin()
def reset():
    try:
        client = Person()
        client.reset_all()
        message = Messages()
        message.reset_message()
        return render_template('signin.html')
    except:
        pass

@app.route("/load_messages",methods=["GET","POST"])
@cross_origin()
def load_messages():
    try:
        message_box = Messages()
        messages = [message_box.message[mess] for mess in range(min(len(message_box.message),10))]

        return render_template('admin.html',messages = messages)
    except Exception as e:
        print(e)
        pass
    return render_template('admin.html')


@app.route("/del_messages", methods=["GET", "POST"])
@cross_origin()
def del_messages():
    try:
        message_box = Messages()
        message_box.reset_message()
    except:
        pass
    return render_template('admin.html')


## HOME PORTFOLIO ------------------------------------------------------------------------------------------------------

@app.route('/',methods = ['GET','POST'])
@cross_origin()
def home():
    try:
        client = Person()
        if client.first_time_login():
            return render_template('signin.html')
        if request.method == 'POST':
            return render_template("home.html",name = client.name,resume = client.resume,image = client.image_file,about =client.about,skills = client.skills,projects =client.projects,user = True)
        else:
            return render_template("home.html",name = client.name,image = client.image_file,about =client.about,skills = client.skills,projects =client.projects,user = True)

    except Exception as e:
        print(e)
        pass
    return render_template('signin.html')


if __name__ == "__main__":
    app.run()
