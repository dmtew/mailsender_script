
import requests
import json
import smtplib
import time
import uuid
import urllib3
from requests import Session
from zeep import Client
from zeep.transports import Transport
import logging

logging.basicConfig(filename="api.log", level=logging.INFO)


def ws_support_register(email, title, mes):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    session = Session()
    session.verify = False
    transport = Transport(session=session)
    client = Client("http://support.robokassa.ru/svc/support.asmx?WSDL", transport=transport)
    RegisterRequest = {
        'EMail': email,
        'Title': title,
        'Message': mes,
        "RequestID": 2000000,
        'PersonID': str(uuid.uuid4())
    }
    #  print(RegisterRequest['PersonID'])
    result = client.service.Register(request=RegisterRequest)
    return result


res = requests.post(url='https://robokassa.com/mod/api/?api_key=1bcad56ad87824be83169db7b4f0ff81&method=getLeads'
                        '&status=0&count=999')
json_ = json.loads(res.text)

count=0
for _id_ in json_["data"]["leads"]:
    #  print(json_["data"]["leads"][_id_]["num"])
    title = 'Обращение от [' + json_["data"]["leads"][_id_]["client"]["name"] + json_["data"]["leads"][_id_]["form_data"]["653702"]["value"] + ']'
    phone = json_["data"]["leads"][_id_]["client"]["phone"]
    email = json_["data"]["leads"][_id_]["client"]["email"]
    #  print(email)
    if email == '':
        email = str(uuid.uuid4())+'@noemail.local'
    print(title, phone, email)
    
    if "310277" in json_["data"]["leads"][_id_]["form_data"]:
        mes = 'Мой номер ' + phone + '\n' + json_["data"]["leads"][_id_]["form_data"]["310277"]["value"]  # Само сообщение
        
    elif "900782" in json_["data"]["leads"][_id_]["form_data"]:
        mes = 'Мой номер ' + phone + '\n'+ "Хочу получить консультацию " + str(json_["data"]["leads"][_id_]["form_data"]["900782"]["value"]) + str(json_["data"]["leads"][_id_]["form_data"]["283224"]["value"])
        
    elif "521993" in json_["data"]["leads"][_id_]["form_data"]:
        mes = 'Мой номер ' + phone + '\n'+ "Хочу у вас работать [Резюме загружено во Flexbe]"
        
    elif json_["data"]["leads"][_id_]["pay"]["summ"] == "1.00":
        mes = 'Мой номер ' + phone + '\n' + json_["data"]["leads"][_id_]["form_data"]["988427"]["value"] + '[Консультация!]'
    else:
        mes = '[ERROR]'
    #  print(mes)
    try:
        res_from_robo = ws_support_register(email, title, mes)
        #  print(res_from_robo)
        if res_from_robo['Result']:
            res = requests.post(
                url='https://robokassa.com/mod/api/?api_key=1bcad56ad87824be83169db7b4f0ff81&method=changeLead&id=' + _id_ + '&status=1')
            print(json.loads(res.text)["status"])
    except Exception as e:
        print(e)
    #  print('---------------------------------------------------------------------------------------------------------')
    time.sleep(5)




    count+=1
#  print(count)
