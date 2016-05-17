from flask import Flask , request , url_for
app = Flask(__name__)

@app.route('/')
def hey():
  return redirect(url_for('static'),filename="html/index.html")

if __name__ == '__main__':
  app.run(debug=True)
