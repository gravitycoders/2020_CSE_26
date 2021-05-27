import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import numpy as np


# initializations 
cred = credentials.Certificate('face-recognition-key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

 
#adding first data
def init_db():
    global collectiondb
    collectiondb = db.collection('companies')


def init_company(email):
    global company
    print(email)
    query = collectiondb.where('email', '==', email ).get()
    for q in query:
        print(q.id)
        cname=q.id
    company=collectiondb.document(cname)
    global employee,face_data,all_encodings
    employee=company.collection('employees')
    face_data=company.collection('face_data')
    all_encodings = face_data.stream()
    return org_face_data(all_encodings)


'''def add_employee(name,role):
    global employee
    new_emp={
        'name':name,
        'role':role
    }
    doc=employee.document()
    doc.set(new_emp)
    return doc.id,name

def add_face(uid,jsdoc):
    global face_data    
    face_data.document(uid).set(jsdoc)
    return True
'''   
def imgdecode(facestr):
    # Deserialization
    print("Decode JSON serialized NumPy array")
    decodedArrays=[]
    for cface in facestr:
        decodedArrays.append(json.loads(cface))

    finalNumpyArray = np.array(decodedArrays)
    print("NumPy Array done")
    return finalNumpyArray

def org_face_data(all_encodings):
    names=[]
    facestr=[]
    for doc in all_encodings:
       currdoc=doc.to_dict()
       names.append(currdoc['name'])
       facestr.append(currdoc['face'])
    facestr=imgdecode(facestr)
    return names,facestr

def getitems():
    return names,facestr
 
init_db()
names,facestr=init_company('tcs@comp.com')
print('success')