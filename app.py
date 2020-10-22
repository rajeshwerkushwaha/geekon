import uuid
from bs4 import BeautifulSoup
from flask import Flask, request, render_template
import subprocess
import os
from db import insertReceiptData, insertReceiptInfo, getItemFromDB
import re
import json

os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/getItem/<item>')
def getItem(item):
    result = getItemFromDB(item)
    print(type(result))
    return {
        'item': item,
        'result': json.dumps(result)
    }


@app.route('/showReceipt/<file_uuid>')
def showReceipt(file_uuid):
    command = "php escpos-tools/esc2html.php files/{}.bin".format(file_uuid)
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    script_response = proc.stdout.read()

    soup = BeautifulSoup(script_response, features="html.parser")
    body = str(soup.find('body'))

    # getReceiptInfo(file_uuid, soup)

    return render_template('receipt.html', body=body)


@app.route('/createURL/', methods=['POST'])
def createURL():
    file_uuid = str(uuid.uuid1())
    merch_uuid = request.form['mid']
    file_data = request.form['file']

    print(type(file_data))

    # write file into files folder for now
    file_name = 'files/'+file_uuid+'.bin'
    with open(file_name, "wb") as f:
        f.write(bytearray(file_data, 'utf-8'))

    command = "php escpos-tools/esc2html.php files/{}.bin".format(file_uuid)
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    script_response = proc.stdout.read()

    soup = BeautifulSoup(script_response, features="html.parser")
    html_data = str(soup.find('body'))

    # print(html_data)
    # print(type(html_data))

    # insertReceiptData(file_uuid, merch_uuid, raw_data, html_data)
    # getReceiptInfo(file_uuid, soup)

    return {
        'file_uuid': file_uuid,
        'merch_uuid': merch_uuid,
        'url': 'http://127.0.0.1:5000/showReceipt/{}'.format(file_uuid)
    }

def getReceiptInfo(file_uuid, soup):
    tags = soup.find_all("div", class_="esc-line")
    data = []
    items = []
    for tag in tags:
        class_count = len(tag["class"])
        if class_count == 1:
            data.append(tag.text)

    # hardcoded [TODO]
    data = data[1:-5]

    for d in data:
        d1 = re.split('[\s+]{2,}', d)
        d1 = [s.strip() for s in d1 ]
        items.append( (d1[0], d1[1]) )
    print(items)

    insertReceiptInfo(file_uuid, items)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    # app.run(host='0.0.0.0')







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
