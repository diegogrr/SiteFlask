from flask import Flask, render_template

app = Flask(__name__)

# Create pages
@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/contact')
def contacts():
    return render_template('contact.html')

@app.route('/users/<my_user>')
def users(my_user):
    return render_template('users.html', my_user=my_user)

# Execute the server function
if __name__ == "__main__":
    app.run(debug=True)
