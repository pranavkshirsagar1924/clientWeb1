from flask import Flask,render_template,request
from flask_mail import Mail, Message
import json
import os

app = Flask(__name__)
m = os.environ.get('contactjadanghadan@gmail.com')
p = os.environ.get('pmty htcu igln qwvd')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = f'{m}'
app.config['MAIL_PASSWORD'] = f'{p}'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/')
def home():
    with open ('static/data.json','r') as file:
        data = json.load(file)
        print(data)
    return render_template("home.html",data=data)

@app.route('/card')
def card():
    id = request.args.get('id')
    with open ('static/data.json','r') as file:
        data = json.load(file)
        for items in data:
            if items['id'] == int(id):
               return render_template('card.html',data=items)
    return render_template('card.html',data='Order cannot be place.')

@app.route('/order',methods=['POST'])
def order():
    name = request.form.get('name')
    email = request.form.get('email')
    mob = request.form.get('mob')
    msg = request.form.get('msg')
    orderOn = json.loads(request.form.get('order'))
    send_status = send_email(name,email,mob,msg,orderOn)
    if send_status:
        return render_template('done.html',msg='Message Sent to the Owner Successfully, Owner will contact you soon!')
    return render_template('done.html',msg='Something was wrong.')

def send_email(username,email,mob,mesg,Order):
    # Create a message
    msg = Message(
        subject="Enquiry Email.",
        sender=email,
        recipients=[os.environ.get('appmail')],  # list of recipients
        body=''
    )
    msg.html = render_template('mail.html', user=username, mob=mob, message=mesg,data=Order)
    # Send the message
    mail.send(msg)
    
    return True


if __name__ == "__main__":
    app.run(debug=False)
