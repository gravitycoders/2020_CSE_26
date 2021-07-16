
from pyrebase import pyrebase
from getpass import getpass
import pydb

firebaseConfig = {
    'apiKey': "AIzaSyDuLwwFeZxXcu5BfpnghOPr5HKJviknaLY",
    'authDomain': "face-recognition-2e311.firebaseapp.com",
    'databaseURL': "https://face-recognition-2e311.firebaseio.com",
    'projectId': "face-recognition-2e311",
    'storageBucket': "face-recognition-2e311.appspot.com",
    'messagingSenderId': "70652685249",
    'appId': "1:70652685249:web:67e68fab6d406531739d40",
  }



firebase = pyrebase.initialize_app(firebaseConfig)

auth=firebase.auth()



def signin(email,password):
    try:
        signinv=auth.sign_in_with_email_and_password(email,password)
        
        print(signinv)
        pydb.init_db()
        pydb.init_company(signinv['email'])
        return True
    except Exception as e:
        print(e)
        return False



