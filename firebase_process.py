from pyrebase import pyrebase
import firebaseConfigFile
import numpy as np

# connect firebase
firebase = pyrebase.initialize_app(firebaseConfigFile.firebaseConfig)
storage = firebase.storage()
db = firebase.database()


def readFirebase(variablesObject,device):
    data = db.child(f"state/{device}").get()
    if data.val() == 0:
        print("henüz soru yok")
        return 0

    elif data.val() == 1:

        questionArray = []
        keyArray = ["question", "a", "b", "c", "d", "e"]

        # get question from firebase
        data = (db.child(f"questions/{device}").get()).val()

        for i in keyArray:
            questionArray.append(data[i])

        questionArray = np.asarray(questionArray)

        variablesObject.setQuestion(questionArray)

        # get image from firebase
        storage.child(f"{device}/1.jpg").download("1.jpg")
        return 1


def writeFirebase(answer,device):
    # set answer and state to firebase
    db.child(f"state/{device}").set(0)
    db.child(f"answers/{device}").set(answer)

def createFirebase(id):
    # create new device in database
    if db.child(f"questions/{id}").get().val() == None:
        db.child(f"questions/{id}/a").set(0)
        db.child(f"questions/{id}/b").set(0)
        db.child(f"questions/{id}/c").set(0)
        db.child(f"questions/{id}/d").set(0)
        db.child(f"questions/{id}/e").set(0)
        db.child(f"questions/{id}/question").set(0)
        db.child(f"state/{id}").set(0)
        db.child(f"answers/{id}").set("")
        return True

    else:
        return False
