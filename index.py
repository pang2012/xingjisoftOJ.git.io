from flask import Flask, render_template, redirect,request,session,make_response
import threading,time,easygui
import subprocess,hashlib,os
 
app = Flask(__name__)

nowques=None
app.secret_key = 'c4d038b4bed09fdb1471ef51ec3a32cd'

online=[]
onlineip=[]
 
@app.route('/')
def index():
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    user_ip = request.remote_addr
    if (user_ip in onlineip):
        return render_template('login_main.html',username=online[onlineip.index(user_ip)])
    return render_template('main.html',username="")
 
 
@app.route('/login_page')
def login_page():
    return render_template('login.html')

@app.route('/main_page')
def main_page():
    return render_template('main.html',username="")

@app.route('/login_main_page <username>')
def login_main_page(username):
    #username = session.get('username')
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    user_ip = request.remote_addr
    usern=online[onlineip.index(user_ip)]
    if (usern!=username):
        return "你个酸萝卜别吃，我好不容易做的网页，你却给我投机取巧，是当我们是伞兵吗？我警告你，你再这样做，下场不会好。我劝你耗子尾汁，改过自新。"
    if not(username in online):
        return "你个酸萝卜别吃，我好不容易做的网页，你却给我投机取巧，是当我们是伞兵吗？我警告你，你再这样做，下场不会好。我劝你耗子尾汁，改过自新。"
    return render_template('login_main.html',username=username)

@app.route('/rank_page <username>')
def rank_page(username):
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    user_ip = request.remote_addr
    usern=online[onlineip.index(user_ip)]
    if (usern!=username):
        return "你个酸萝卜别吃，我好不容易做的网页，你却给我投机取巧，是当我们是伞兵吗？我警告你，你再这样做，下场不会好。我劝你耗子尾汁，改过自新。"
    if not(username in online):
        return "你个酸萝卜别吃，我好不容易做的网页，你却给我投机取巧，是当我们是伞兵吗？我警告你，你再这样做，下场不会好。我劝你耗子尾汁，改过自新。"
    return render_template('rank.html',username=username)

@app.route('/problems <username>')
def problems_page(username):
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    user_ip = request.remote_addr
    usern=online[onlineip.index(user_ip)]
    try:
        #return render_template('problem.html',username=username)
        if (usern!=username):
            return "你个酸萝卜别吃，我好不容易做的网页，你却给我投机取巧，是当我们是伞兵吗？我警告你，你再这样做，下场不会好。我劝你耗子尾汁，改过自新。"
        if not(username in online):
            return "你个酸萝卜别吃，我好不容易做的网页，你却给我投机取巧，是当我们是伞兵吗？我警告你，你再这样做，下场不会好。我劝你耗子尾汁，改过自新。"
        return render_template('problem.html',username=username)
    except:
        return render_template('login.html',loginmsg="请先登录再使用题库")

@app.route('/login')
def login():
    global online
    username = request.values.get("username")
    password = request.values.get("password")
    alluserf=open("static/userdata/username.txt","r")
    allpasswordf=open("static/userdata/userpassword.txt","r")
    alluser=alluserf.readlines()
    allpassword=allpasswordf.readlines()
    alluserf.close()
    allpasswordf.close()
    password=hashlib.md5(password.encode("utf-8")).hexdigest()
    if (username in online):
        return render_template('login.html',loginmsg="此账号已在其他设备登录")
    for i in range(len(alluser)):
        if (alluser[i].strip("\n")==username and password==allpassword[i].strip("\n")):
            #session['username'] = username
            x_forwarded_for = request.headers.get('X-Forwarded-For')
            user_ip = request.remote_addr
            online.append(username)
            onlineip.append(user_ip)
            return render_template('login_main.html',username=username)
    return render_template('login.html',loginmsg="账号或密码错误")

@app.route('/problem <name>-<username>')
def problemsxx_page(name,username):
    #try:
        #global nowques
        #nowques=name
    return render_template('questions/'+name+'.html',username=username)
    #except:
        #return render_template('login.html',loginmsg="请先登录再使用题库")

@app.route('/submit<name> <language> <ques>', methods=['POST'])
def submit(name,language,ques):
    text = request.form['code']
    # 处理text...
    print('Text received: {}'.format(text))
    output=None
    def judge(name):
        global output
        f=open("submit/"+name,"w")
        f.write(text)
        f.close()
        # 使用subprocess.run来运行外部程序
        process = subprocess.run(['python',"judger.py", name,'submit/'+name,language], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()
        output = process.stdout
        return render_template('questions/'+ques+'.html',judgeresult="Accepted")

    thread = threading.Thread(target=lambda:judge(name))
    thread.start()
    f=open("data.log","r")
    output=f.read()
    f.close()
    return output

@app.route('/images/<path:path>')
def send_image(path):
    # 假设图片存储在static/images目录下
    return app.send_static_file("images/"+path)

@app.route('/css/<path:path>')
def send_css(path):
    # 假设css存储在static/css目录下
    return app.send_static_file("css/"+path)

@app.route('/js/<path:path>')
def send_js(path):
    #存储在static/js目录下
    return app.send_static_file("js/"+path)

@app.route('/close_page <username>')
def close_page(username):
    global online,onlineip
    for i in range(len(online)):
        if (online[i]==username):
            online.pop(i)
            onlineip.pop(i)
    return render_template('main.html',username="")
 
if __name__ == '__main__':
    app.config['SERVER_NAME'] = '192.168.124.7:5000'
    app.run(debug=True)