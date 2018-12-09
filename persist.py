import mysql.connector

def insert(placa,orgao,url):  
    mydb = mysql.connector.connect(host='127.0.0.1', user = 'root', passwd = '', database = 'hackfest')
    mycursor = mydb.cursor()
    insert = "INSERT INTO carros (placa, orgao, url) values ('{}','{}','{}')"
    mycursor.execute(insert.format(placa, orgao,url))
    mydb.commit()
