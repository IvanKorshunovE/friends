from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialize database
db = SQLAlchemy(app)
app.app_context().push()

# Create db model
class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

# Create function to return string when we add something
    def __repr__(self):
        return f'{self.name}, id = {self.id}'
        # return '<Name %r>' % self.id


@app.route('/delete/<int:id>')
def delete(id):
    friend_to_delete = Friends.query.get_or_404(id)
    try:
        db.session.delete(friend_to_delete)
        db.session.commit()
        return redirect('/friends')
    except:
        return 'There was a problem deleting that friend'


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    friend_to_update = Friends.query.get_or_404(id)
    if request.method == 'POST':
        friend_to_update.name = request.form['name']
        try:
            db.session.commit()
            return redirect('/friends')
        except:
            return 'There was a problem updating that friend'
    else:
        return render_template('update.html', friend_to_update=friend_to_update)

@app.route('/friends', methods=['POST', 'GET'])
def friends():
    if request.method == 'POST':
        friend_name = request.form['name']
        new_friend = Friends(name=friend_name)
        try:
            db.session.add(new_friend)
            db.session.commit()
            return redirect('/friends')
        except:
            return "There was an error adding your friend"
    else:
        friends = Friends.query.order_by(Friends.date_created)
        return render_template('friends.html', friends=friends)

@app.route('/')
def index():
    pizza = ['pepperoni', 'cheese', 'mushrooms']
    return render_template('index.html', pizza=pizza)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

@app.route('/subscribe')
def subscribe():
    title = 'Subscribe to my email newslatter'
    return render_template('subscribe.html', title=title)

# 1) We are sent to def subscribe():
# 2) We make a POST to def form(): in subscribe.html. - <form action="/form" method='POST'>
# 3) in def form(): we are sent to 'form.html'

@app.route('/form', methods=['POST'])
def form():
    first_name = request.form['first_name']
    last_name = request.form.get('last_name')
    email = request.form.get('email')

    # message = 'You have been subscribed to my email'
    # server = smtplib.SMTP('smtp.gmail.com', 587)
    # server.starttls()
    # server.login('ivan.korshunov.1997@gmail.com')

    if not first_name or not last_name or not email:
        error_statement = 'All form fields required to fill...'
        return render_template('subscribe.html',
                               error_statement=error_statement,
                               first_name=first_name,
                               last_name=last_name,
                               email=email)

    title = 'Thank you'
    return render_template('form.html',
                           title=title,
                           first_name=first_name,
                           last_name=last_name,
                           email=email)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001)