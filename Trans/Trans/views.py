import sqlite3
from django.http import HttpResponse
import requests as rq;
import os;
import random
import json;
from datetime import datetime;


#helpfunc 
def db(command):
    conn = sqlite3.connect("data.sqlite");
    cursor = conn.cursor();
    data='0';
    if "SELECT" in command:
        cursor.execute(command);
        data = cort_to_list(cursor.fetchall());
    elif "UPDATE" in command  or "INSERT" in command or "DELETE" in command:
        cursor.execute(command);
        conn.commit();
    conn.close();
    return data;
def dateNow():
    d=datetime.now();
    date="{0}.{1}.{2} {3}:{4}:{5}".format(str(d.day),str(d.month),str(d.year),str(d.hour),str(d.minute),str(d.second));
    return date;
def cort_to_list(cort):
    list_=[];
    for i in range(len(cort)):
        list_.append(cort[i][0]);
    return list_;
def httpPost(url,body):
    r = rq.post(url,headers={},data=body);
    return r;
#helpfunc 


#function transaction generate and send new transaction
def transaction(request): #create mode
    ID=0;
    ids=db("SELECT ID FROM trans");
    while ID in ids:
        ID=random.randint(1,9999);
    TimeStamp=dateNow();
    Type="someType";
    Actor="someActor";
    TransactionData={"some":"data"};
    TransactionData=json.dumps(TransactionData);
    body={"ID":ID,"TimeStamp":TimeStamp,"Type":Type,"Actor":Actor,"TransactionData":TransactionData};
    res=httpPost("http://localhost:8080/save_transaction/",body=body);
    send={"res":"OK","err":0,"date":TimeStamp};
    send=json.dumps(send);
    return HttpResponse(send, content_type='application/json');
#function save_transaction get and save generated transactions
def save_transaction(request):
    ID=request.POST['ID'];
    TimeStamp=request.POST['TimeStamp'];
    Type=request.POST['Type'];
    Actor=request.POST['Actor'];
    TransactionData=request.POST['TransactionData'];
    print(ID,TimeStamp,Type,Actor,TransactionData);
    db("INSERT INTO 'trans' VALUES('{0}','{1}','{2}','{3}','{4}')".format(ID,TimeStamp,Type,Actor,TransactionData));
    send={"res":"OK","err":0};
    send=json.dumps(send);
    return HttpResponse(send, content_type='application/json');

#function ed_transactions exist as help for do requests to edit_transactons
def ed_transactions(request): #create mode
    #delete:
    body={"ID":"0","mode":"delete"};
    
    #update
    #body={"ID":"0","mode":"update","dataKey":"TimeStamp","dataVal":"0"};
    
    send=httpPost("http://localhost:8080/edit_transactions/",body=body);
    return HttpResponse(send, content_type='application/json');
#function edit_transactions use for edit and delete transactions
def edit_transactions(request):
    try:
        ID=request.POST['ID'];
        mode=request.POST['mode']; #delete, update, 
        if mode=="update":
            dataKey=request.POST['dataKey'];
            dataVal=request.POST['dataVal'];
            print(dataKey,dataVal)
            command="UPDATE trans SET '{0}'='{1}' WHERE id={2}".format(dataKey,dataVal,ID);
        else:
            command="DELETE FROM trans WHERE id={0}".format(ID)
        db(command);
        send={"res":"OK","err":0};
    except Exception as e:
        print(e);
        send={"res":"requaired args are ID (must exist) and mode (update/delete). If you want update db you must add dataKey (ID/TimeStamp/Type/Actor/TransactionData) and dataVal(*).  ","err":1};
    send=json.dumps(send);
    return HttpResponse(send, content_type='application/json');


