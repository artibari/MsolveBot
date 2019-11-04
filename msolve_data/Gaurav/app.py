from flask import Flask
import send_mail_trail

app = Flask(__name__)

@app.route('/sendMailTrail')
def hello():
    # complete the flask api as per your need
    # call send mail function over here
    # Check the rest api locally 
    # run the commands from commands.txt in docker env (need full internet access)
    # check in postman weather http://localhost:7001/sendMailTrail is working or not
    return "hello docker"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001) 
 
