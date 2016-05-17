from flask import *
from sqlalchemy import *
from sqlalchemy.sql import *
from sqlalchemy.orm import sessionmaker
from sql_alchemydeclarative import  Base, User

app = Flask(__name__)
app.secret_key = 'iswuygdedgv{&75619892__01;;>..zzqwQIHQIWS'
engine = create_engine('sqlite:///mabase.db', echo=True)
metadata = MetaData()
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
DBSession.bind = engine
sessiondb = DBSession()
Error = ''
cree = False

users = Table('user', metadata,
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
        message = session['Email']
    else:
        message = 'User ne pas trouve'
        print(message)
    #return redirect(url_for('static', filename='html/index.html'))
    return render_template('html/index.html',message=message, logged=logged)

@app.route('/login',methods=['POST'])
def login():
    session['Email'] = escape(request.form['Email'])
    session['Password'] = escape(request.form['Password'])
    session['logged'] = False
    metadata.create_all(engine)
    connection = engine.connect()
    s = select([users.c.nom_util]).where(and_(or_(users.c.nom_util.like(session['Email']),users.c.email_util.like(session['Email'])),users.c.motpass.like(session['Password'])))
    for row in connection.execute(s):
        print(row)
        session['logged'] = True
        print("User found")
    print('\n')

    #result = connection.execute(s)
    connection.close()
    if session['logged']:
        return redirect('/')
    else:
        session.clear()
        return render_template('html/signer.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/signin')
def signin():
    return render_template('html/signin.html')

@app.route('/register',methods=['POST'])
def register():
    cree = False
    Error = []
    Email = escape(request.form['Email'])
    Pass = escape(request.form['Pass'])
    Name = escape(request.form['Name'])
    #session['Email'] = escape(request.form['Email'])
    #session['Password'] = escape(request.form['Password'])
    metadata.create_all(engine)
    connection = engine.connect()
    person = sessiondb.query(User).filter(or_(User.nom_util == Name,User.email_util == Email)).all()
    for i in person:
        if(i.nom_util == Name):
            Error.append('Nom de utilisateur deja cree')
        else:
            Error.append('Adresse Email deja registre')
        cree = True
    #person = sessiondb.query(User).filter(or_(User.nom_util == Name,User.email_util == Email)).first()
    if cree:
        return render_template('html/signin.html',cree=cree,Error=Error)
    else:
        person = User(email_util = Email, nom_util = Name, motpass  = Pass)
        sessiondb.add(person)
        sessiondb.commit()
        session['Email'] = Email
        session['logged'] = True
    return redirect('/')

if __name__ == '__main__':
  app.run(debug=True)
