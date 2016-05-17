from flask import *
from sqlalchemy import *
from sqlalchemy.sql import *
app = Flask(__name__)
app.secret_key = 'iswuygdedgv{&75619892__01;;>..zzqwQIHQIWS'
engine = create_engine('sqlite:///mabase.db', echo=True)
metadata = MetaData()

users = Table('users', metadata,
    Column('cle_util', Integer, autoincrement=True, primary_key=True),
    Column('email_util', String),
    Column('nom_util', String),
    Column('motpass', String),
    Column('info_uti',String))

@app.route('/')
def index():
    logged = 'logged' in session
    message = ""
    if logged:
        message = session['Email'] + session['Password']
    #return redirect(url_for('static', filename='html/index.html'))
    return render_template('html/index.html',message=message, logged=logged)

@app.route('/login',methods=['POST'])
def login():
    session['Email'] = escape(request.form['Email'])
    session['Password'] = escape(request.form['Password'])
    metadata.create_all(engine)
    connection = engine.connect()
    s = select([users.c.nom_util]).\
        where(
            and_(
                users.c.nom_util.like(session['Email']),
                users.c.motpass.like(session['Password'])
            )
        )
    for row in connection.execute(s):
        print(row)
        session['logged'] = True
        print("User found")
    print('\n')
    connection.close()

    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
  app.run(debug=True)
