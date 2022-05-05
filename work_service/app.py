from flask import Flask, render_template, request
from work_service.db_request import db_request
import json

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
  return render_template('home.html')

@app.route('/result', methods=['POST', 'GET'])
def result():
   output = request.form.to_dict()
   phrase = output["phrase"]
   res = db_request(phrase)
   print(res)
   return render_template('home.html', phrase=phrase, results=res)

if __name__ == "__main__":
   app.run()