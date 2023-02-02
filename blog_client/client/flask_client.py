
from flask import Flask, send_file

app = Flask(__name__)

@app.route('/index')
def index():
    
    return send_file('templates/index.html')

@app.route('/login')
def login():
    
    return send_file('templates/login.html')

@app.route('/register')
def register():
    
    return send_file('templates/register.html')

@app.route('/<username>/info')
def info(username):
    
    return send_file('templates/about.html')

@app.route('/<username>/change_info')
def change_info(username):
    
    return send_file('templates/change_info.html')

@app.route('/<username>/topic/release')
def topic_release(username):
    
    return send_file('templates/release.html')


@app.route('/<username>/topics')
def topics(username):
    
    return send_file('templates/list.html')

@app.route('/<username>/topics/detail/<t_id>')
def topics_detail(username, t_id):
    
    return send_file('templates/detail.html')

#@app.route('/test_api')
#def test_api():
    #return send_file('templates/test_api.html')

if __name__ == '__main__':
    app.run(debug=True)

