from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', title="Головна")

@app.route('/catalog')
def catalog():
    return render_template('catalog.html', title="Каталог")

@app.route('/about')
def about():
    return render_template('about.html', title="Про нас")

@app.route('/contacts')
def contacts():
    return render_template('contacts.html', title="Контакти")

if __name__ == '__main__':
    app.run(debug=True)