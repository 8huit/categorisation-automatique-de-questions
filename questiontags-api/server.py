import os
import uvicorn
import logging
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import tensorflow as tf
import joblib
import numpy as np
import pandas as pd
import re

from sklearn.feature_extraction.text import TfidfVectorizer

# Initialize logging
#my_logger = logging.getLogger()
#my_logger.setLevel(logging.DEBUG)
#logging.basicConfig(level=logging.DEBUG, filename='logs.log')

app = FastAPI()
app.mount("/vendor", StaticFiles(directory="templates/vendor"), name="vendor")
app.mount("/css", StaticFiles(directory="templates/css"), name="css")
app.mount("/js", StaticFiles(directory="templates/js"), name="js")

templates = Jinja2Templates(directory="templates")



@app.on_event("startup")
def load_model():
    global tagclass
    global model
    global dfTFIDFCommon
    global vocab
    global map_classtag
    global tag_questions

    tagclass=joblib.load('./models/tagclass.jbl.bz2')
    model = tf.keras.models.load_model("./models/rn2")
    dfTFIDFCommon=joblib.load('./models/dfTFIDFCommon.jbl.bz2')

    # dictionaire inversé pour retrouver le tag correspondant à une classe
    map_classtag = dict(zip(tagclass.values(), tagclass.keys())) 
    map_classtag[0]='autres'

    # vocabulaire constitué des colonnes(bigrammes) du dataframe TFIDFcommon
    vocab=dict(zip(dfTFIDFCommon.columns,list(range(dfTFIDFCommon.shape[1]))))


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/")
async def home(request: Request,inputQuestion: str=Form(...)):
    def tag_question(question, model,vocab):
        """
        Fonction qui retourne le tag predit par le modele 

        Parameters
        ----------
        question : string
            question sous forme d'une chaine de caracteres
        model : modele tensorflow
            réseau neuronal
        vocab : vocabulaire
            un dictionnaire de bigrammes utilisé pour calculer les valeurs TFIDF de la question
        Returns
        -------
        map_classtag : string
            le tag predit par le modele pour la question posée
        """

        question=re.sub(r'(<\/?[a-z]+>|&lt;|&gt;|//|["!\"#$%&\(\)\*\+-\.\/:;<=>\?\@\\^_\'`\{\|\}~\n"]|\d+.\d+|\S+_\S+|\*+|[0-9]+[a-z]+|[\d+]|[abcd]{2,}[a-z]*)',' ',question.lower())
        print(question)
        vectorizer= TfidfVectorizer(ngram_range = (2,2),vocabulary=vocab) #vectorize bigram with fixed vocab
        response=vectorizer.fit_transform([question]) # fit question
        tfidfQuestion=response.toarray()
        #y_pred=model.predict_classes(tfidfQuestion) #predict class
        predict_x=model.predict(tfidfQuestion) 
        y_pred=np.argmax(predict_x,axis=1)
        #y_pred=(model.predict(tfidfQuestion) > 0.5).astype("int32")
        print(y_pred)
        return map_classtag[y_pred[0]] # convert to tag

    question=inputQuestion
    tag=tag_question(question, model, vocab)
    return templates.TemplateResponse("index.html", {"request": request,"result":tag})

# Run the API with uvicorn
envPORT=os.environ.get('PORT','8000')
if __name__ == '__main__':
   uvicorn.run(app, host='0.0.0.0', port=int(envPORT))
