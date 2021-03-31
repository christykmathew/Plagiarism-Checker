import flask
from flask import Flask, render_template, request
import requests
from plagiarism import Online_Plagiarism, Offline_Plagiarism

app = Flask(__name__)

@app.route('/')
def land():
    return render_template('index.html')

@app.route('/main')
def main_page():
    return render_template('main.html')

@app.route('/send', methods=["GET"])
def check():
    input_text1 =flask.request.args.get('val1')
    input_text2 = flask.request.args.get('val2')
    type = flask.request.args.get('val3')
    if (input_text1 == '' and input_text2 == ''):
        return flask.jsonify({"result":"No Text Entered"})
    if (type == 'Offline'):
        if (input_text1 == '' or input_text2 == ''):
            return flask.jsonify({"result":"Enter Text in both fields"})
        out = Offline_Plagiarism()
        t = out.check_text(input_text1, input_text2)
        if (t[:t.index('%')] == '100.00'):
            return flask.jsonify({"result":"<h2>Both Texts are same</h2>"})
        return flask.jsonify({"result":"<span style=\"font-size: 25px\">"+t[:t.index('%')+1]+" </span><span style=\"font-size: 20px\">"+t[t.index('%')+1:]+"</span>"})        
    if (type == 'Online'):
        if (input_text1 == ''):
            return flask.jsonify({"result":"Enter Text Field"})
        if (len(input_text1) < 250):
            return flask.jsonify({"result": "Input Insufficient"})
        out = Online_Plagiarism()
        t = out.check_text(input_text1)
        if (len(t) == 0):
            return flask.jsonify({"result": "No Plagiarism found"})
        a = "<tr><th rowspan='2' style= \"font-size: 30px; margin-right:15px\" onmouseover=\"this.style.color='yellowgreen'\" onmouseout=\"this.style.color=''\">"
        b = "</th><td><a href=\""
        c = "\" onmouseover=\"this.style.color='#006db9'\" onmouseout=\"this.style.color='#fff'\" style=\"margin-left:8px; font-weight:bold; color: white; text-decoration:none\">"
        d = "↴</a></td></tr><tr style =\"padding-bottom: 100px\"><td onmouseover=\"this.style.color='#006db9'\" onmouseout=\"this.style.color=''\" ><i style=\"margin-left:8px;\">"
        e = "</i></td></tr><tr><th colspan = '2'>_________________________________________________________</tr>"
        temp = '<table>'
        for i in t:
            temp = temp + a+str(i[2])+'%'+b+i[0]+c+i[0]+d+i[1][:200]+'...'+e
        print("Sending Response")
        return flask.jsonify({"result":temp})
 
@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)