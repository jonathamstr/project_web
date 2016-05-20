from flask import *
from sqlalchemy import *
from sqlalchemy.sql import *
from sqlalchemy.orm import sessionmaker
from sql_alchemydeclarative import  Base, User ,Publication, Commentaire

app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')
app.secret_key = 'iswuygdedgv{&75619892__01;;>..zzqwQIHQIWS'
engine = create_engine('sqlite:///mabase.db', echo=True)
metadata = MetaData()
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
DBSession.bind = engine
sessiondb = DBSession()
metadata.create_all(engine)
connection = engine.connect()
Error = ''
cree = False
message = ""
logged = []

users = Table('user', metadata,
    Column('cle_util', Integer, autoincrement=True, primary_key=True),
    Column('email_util', String),
    Column('nom_util', String),
    Column('motpass', String),
    Column('info_uti',String))

@app.route('/')
def index():
    logged = 'logged' in session
    if logged:
        message = session['Email']
        #query = users.select().order_by(users.c.id.desc()).limit(5)
        pubs = sessiondb.query(Publication).order_by(Publication.date.desc()).limit(10)
        for i in pubs:
            print(i.titre)
        return render_template('html/Random.html',message=message, logged=logged,pubs=pubs)
    else:
        message = 'User ne pas trouve'
        print(message)
        return render_template('html/index.html',message=message, logged=logged)
    #return redirect(url_for('static', filename='html/index.html'))


@app.route('/login',methods=['POST'])
def login():
    session['Email'] = escape(request.form['Email'])
    session['Password'] = escape(request.form['Password'])
    session['logged'] = False
    person = sessiondb.query(User).filter(or_(User.nom_util == session['Email'],User.email_util == session['Email'])).all()
    #metadata.create_all(engine)
    #connection = engine.connect()
    #s = select([users.c.nom_util]).where(and_(or_(users.c.nom_util.like(session['Email']),users.c.email_util.like(session['Email'])),users.c.motpass.like(session['Password'])))
    #for row in connection.execute(s):
    for row in person:
        print(row)
        session['logged'] = True
        print("User found")
    print('\n')

    #result = connection.execute(s)
    #connection.close()
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


@app.route('/pub',methods=['POST'])
def pub():
    Email = session['Email']
    Name = session['Email']
    print(Email)
    person = sessiondb.query(User).filter(or_(User.nom_util == Name,User.email_util == Email)).one()
    #person = sessiondb.query(User).filter(or_(User.email_util == Email, User.nom_util == Email)).all()

    pub = Publication(cle_util = person.cle_util, auteur = person, titre  = request.form['Titre'], corps = request.form['Corps'] )
    sessiondb.add(pub)
    sessiondb.commit()
    return redirect('/')

@app.route('/posting/<Iden>')
def posting(Iden):
    publ = sessiondb.query(Publication).filter(Publication.cle_pub == Iden).one()
    logged = 'logged' in session
    message = session['Email']
    comments = sessiondb.query(Commentaire).filter(Commentaire.cle_pub == Iden).all()
    #return render_template('html/publication.html',message=message, logged=logged)
    #return app.send_static_file('html/posting.html',message=message, logged=logged,publ = id)
    return render_template('html/posting.html',message=message, logged=logged,publ = publ,comments = comments )

@app.route('/postcomment/<Iden>',methods=['POST'])
def postcomment(Iden):
    person = sessiondb.query(User).filter(or_(User.nom_util == session['Email'],User.email_util == session['Email'])).one()
    comm  =  Commentaire(cle_pub = Iden, cle_util=person.cle_util, corps = request.form['Corps'] )
    sessiondb.add(comm)
    sessiondb.commit()
    return redirect('/posting/' + Iden)
if __name__ == '__main__':
  app.run(debug=True)
