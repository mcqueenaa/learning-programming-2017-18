from flask import Flask
from flask import request
from flask import render_template
from random import choice

app = Flask(__name__)

@app.route('/')
def index():
    prizes = ['автомобиль', 'обезьянку', 'Наташку']
    prize = choice(prizes)
    return render_template('main.html', prize = prize)
    
    #return render_template('main.html')

##@app.route('/hi')
##def notindex():
##    if 'name' in request.args:
##        name = request.args['name']
##        return '<html><body><p>Hello, {}!</p></body></html>'.format(name)
##    else:
##        return '<p>Вы кто???!</p>'

if __name__ == '__main__':
    app.run(debug=True)
