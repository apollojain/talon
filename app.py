from flask import Flask, render_template, redirect, request
import Tkinter, webview, sys, threading, time
import helpers, file_upload, classify_image, webbrowser, pickledb
import subprocess
 
app = Flask(__name__)
db = pickledb.load('example.db', False)

@app.route('/')
def img_search():
    return render_template("loading.html")

@app.route('/', methods=['POST'])
def form_processing():
    print request.form 
    if 'directory' in request.form: 
        subprocess.call(["open", "-R", request.form['directory']])
    directory = helpers.get_directory()
    dictionary = db.get("dictionary")
    if directory == db.get("directory") and type(dictionary) is str:
        dictionary = eval(dictionary)
    else: 
        dictionary = classify_image.get_img_info(directory)
        db.set("directory", directory)
        db.set("dictionary", str(dictionary))
        db.dump()
    dictionary_list = helpers.formatted_index_dict_list(dictionary)
    return render_template("index.html", dictionary_list=dictionary_list)

if __name__ == '__main__':
    """  https://github.com/r0x0r/pywebview/blob/master/examples/http_server.py
    """
    file_pick = file_upload.App()
    run_app = threading.Timer(5, webbrowser.open("http://localhost:5000"))
    run_app.start()  
    app.run()
    