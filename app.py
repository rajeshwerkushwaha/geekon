import uuid
from bs4 import BeautifulSoup
from flask import Flask, request, render_template
import subprocess
import os
import db

os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

db = {}

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/showReceipt/<file_uuid>')
def showReceipt(file_uuid):
    command = "php escpos-tools/esc2html.php files/{}.bin".format(file_uuid)
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    script_response = proc.stdout.read()

    soup = BeautifulSoup(script_response, features="html.parser")
    body = str(soup.find('body'))

    return render_template('receipt.html', body=body)


@app.route('/createURL/<merch_uuid>', methods=['POST'])
def createURL(merch_uuid):
    file_uuid = str(uuid.uuid1())
    file_data = request.form['data']

    # print(file_data)
    # write file into files folder for now
    file_name = 'files/'+file_uuid+'.bin'
    with open(file_name, "wb") as f:
        f.write(str.encode(file_data))

    command = "php escpos-tools/esc2html.php ../files/{}".format(file_name)
    print(command)
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    script_response = proc.stdout.read()
    print(script_response)

    db[file_uuid] = {
        "merch_uuid": merch_uuid,
        "data": file_data
    }
    print(db)


    command = "php escpos-tools/esc2html.php files/{}.bin".format(file_uuid)
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    script_response = proc.stdout.read()
    soup = BeautifulSoup(script_response, features="html.parser")
    html_data = str(soup.find('body'))

    insertReceiptData(file_uuid, merch_uuid, file_data, html_data)

    return {
        'file_uuid': file_uuid,
        'merch_uuid': merch_uuid,
        'file_data': file_data,
        'url': 'http://127.0.0.1:5000/showReceipt/{}'.format(file_uuid)
    }




if __name__ == '__main__':
    app.run(debug=True)







# import uuid
# from bs4 import BeautifulSoup
# from flask import Flask, request, render_template
# from flask_restful import Resource, Api
# import subprocess
# import os
#
# os.path.dirname(os.path.abspath(__file__))
#
# app = Flask(__name__)
# # api = Api(app)
# db = {}
#
# @app.route('/')
# def hello():
#     return 'Hello World!'
#
# @app.route('/showReceipt/<file_uuid>')
# def showReceipt(file_uuid):
#     command = "php escpos-tools/esc2html.php files/{}.bin".format(file_uuid)
#     proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
#     script_response = proc.stdout.read()
#
#     soup = BeautifulSoup(script_response, features="html.parser")
#     body = str(soup.find('body'))
#
#     return render_template('receipt.html', body=body)
#
#
# @app.route('/createURL/<merch_uuid>', methods=['POST'])
# def createURL(merch_uuid):
#     file_uuid = str(uuid.uuid1())
#     file_data = request.form['data']
#
#     # print(file_data)
#     # write file into files folder for now
#     file_name = 'files/'+file_uuid+'.bin'
#     with open(file_name, "wb") as f:
#         f.write(str.encode(file_data))
#
#     command = "php escpos-tools/esc2html.php ../files/{}".format(file_name)
#     print(command)
#     proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
#     script_response = proc.stdout.read()
#     print(script_response)
#
#     db[file_uuid] = {
#         "merch_uuid": merch_uuid,
#         "data": file_data
#     }
#     print(db)
#     return {
#         'file_uuid': file_uuid,
#         'merch_uuid': merch_uuid,
#         'file_data': file_data,
#         'url': 'http://127.0.0.1:5000/showReceipt/{}'.format(file_uuid)
#     }
#
#
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
