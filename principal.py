from flask import *
app = Flask(__name__)
app.secret_key = 'iswuygdedgv{&75619892__01;;>..zzqwQIHQIWS'

@app.route('/')
def index():
    logged = 'logged' in session
    message = ""
    if logged:
        message = session['name']
    #return redirect(url_for('static', filename='html/index.html'))
    return render_template('html/index.html',message=message, logged=logged)

@app.route('/login',methods=['POST'])
def login():
    session['name'] = escape(request.form['Email'])
    session['logged'] = True
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
  app.run(debug=True)
