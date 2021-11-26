from django.core.management import call_command
from django.db import connections
import mysql.connector
import json, sys

# Create your models here.
def create_database(name):
    mydb = connect_to_database()
    database_exits = check_if_database_exists(name, mydb)
    if database_exits:
        # return False
        raise AssertionError('Banco de dados já existe!')

    mycursor = mydb.cursor()
    mycursor.execute(f"CREATE DATABASE {name}")

    newdatabase = insert_new_db_entry(name)

    connections.databases[name] = newdatabase

    call_command('migrate', app_label='auth', database=name)
    call_command('migrate', app_label='sessions', database=name)
    call_command('migrate', app_label='gere_coworking', database=name)
    
    from django.contrib.auth.models import Group
    Group.objects.using(name).get_or_create(name='administrador')
    Group.objects.using(name).get_or_create(name='funcionario')
    Group.objects.using(name).get_or_create(name='clienteEmpresa')
    Group.objects.using(name).get_or_create(name='clientePessoa')

def check_if_database_exists(name, mydb=None):
    if mydb == None:
        mydb = connect_to_database()
    mycursor = mydb.cursor()
    mycursor.execute("SHOW DATABASES")
    for database in mycursor:
        if database[0] == name:
            return True
    return False

def connect_to_database():
    mydb = mysql.connector.connect(
        host="database-2.cjbxv4nbcluu.us-east-1.rds.amazonaws.com",
        port="3306",
        user="admin",
        password="newgen123"
    )
    return mydb

def get_databases():
    f = open('local/db.json', 'r')
    databases = json.load(f)
    f.close()
    return databases

def insert_new_db_entry(name):
    databases = get_databases()
    new_entry = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': name,
        'USER': 'admin',
        'PASSWORD': 'newgen123',
        'HOST': 'database-2.cjbxv4nbcluu.us-east-1.rds.amazonaws.com',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    }
    databases[name] = new_entry
    f = open('local/db.json', 'w')
    f.write(str(json.dumps(databases)))
    f.close()
    return new_entry

