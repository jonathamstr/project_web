from flask import *
from sqlalchemy import *
from sqlalchemy.sql import *
from sqlalchemy.orm import sessionmaker
from sql_alchemydeclarative import  Base, User ,Publication, Commentaire

app = Flask(__name__)
app.secret_key = 'iswuygdedgv{&75619892__01;;>..zzqwQIHQIWS'
engine = create_engine('sqlite:///mabase.db')
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
valeur = 10

users = Table('user', metadata,
    Column('cle_util', Integer, autoincrement=True, primary_key=True),
    Column('email_util', String),
    Column('nom_util', String),
    Column('motpass', String),
    Column('info_uti',String))

def getPubs(number=10):
    return sessiondb.query(Publication).order_by(Publication.date.desc()).limit(number)

@app.route('/')
def index():
    logged = 'logged' in session
    message = ''
    if logged:
        message = session['Email']
        pubs = getPubs(valeur)
        for i in pubs:
            print(i.titre)
        return render_template('html/Random.html',message=message, logged=logged, pubs=pubs,valeur=valeur)
    else:
        return render_template('html/index.html',message=message, logged=logged)

@app.route('/change')
def change():
    global valeur
    valeur = request.args.get('valeur', 0, type=int)
    #return jsonify(valeur)

@app.route('/login',methods=['POST'])
def login():
    session['Email'] = escape(request.form['Email'])
    session['Password'] = escape(request.form['Password'])
    session['logged'] = False
    person = sessiondb.query(User).filter(or_(User.nom_util == session['Email'],User.email_util == session['Email'])).all()
    for row in person:
        session['logged'] = True
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
    person = sessiondb.query(User).filter(or_(User.nom_util == Name,User.email_util == Email)).all()
    for i in person:
        if(i.nom_util == Name):
            Error.append('Nom de utilisateur deja cree')
        if i.email_util ==Email:
            Error.append('Adresse Email deja registre')
        cree = True
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
    person = sessiondb.query(User).filter(or_(User.nom_util == session['Email'],User.email_util == session['Email'])).one()
    pub = Publication(cle_util = person.cle_util, auteur = person, titre  = request.form['Titre'], corps = request.form['Corps'] )
    sessiondb.add(pub)
    sessiondb.commit()
    return redirect('/')

@app.route('/posting/<Iden>')
def posting(Iden):
    publ = sessiondb.query(Publication).filter(Publication.cle_pub == Iden).one()
    comments = sessiondb.query(Commentaire).filter(Commentaire.cle_pub == Iden).all()
    editable = publ.auteur.email_util == session['Email'] or publ.auteur.nom_util == session['Email']
    return render_template('html/posting.html',message= session['Email'], logged = session['logged'],publ = publ,comments = comments , editable=editable)

@app.route('/postcomment/<Iden>',methods=['POST'])
def postcomment(Iden):
    person = sessiondb.query(User).filter(or_(User.nom_util == session['Email'],User.email_util == session['Email'])).one()
    comm  =  Commentaire(cle_pub = Iden, cle_util=person.cle_util, corps = request.form['Corps'] )
    sessiondb.add(comm)
    sessiondb.commit()
    return redirect('/posting/' + Iden)

#@app.route('/_array2python')
#def profile():
#    return json.loads(request.args.get('wordlist'))

if __name__ == '__main__':
  app.run(debug=True)
