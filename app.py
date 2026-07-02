from flask import Flask,request,jsonify,render_template
import pandas as pd
import pickle
import os

app=Flask(__name__)



def get_cleaned_data(form_data):
    gestation= float(form_data['gestation'])
    parity= int(form_data['parity'])
    age= float(form_data['age'])
    height= float(form_data['height'])
    weight= float(form_data['weight'])
    smoke= float(form_data['smoke'])


    cleaned_data={"gestation": [gestation],
                   "parity": [parity],
                   "age": [age],
                    "height": [height],
                   "weight": [weight],
                   "smoke": [smoke]
                   }
    return cleaned_data

#creating home page
@app.route("/",methods=["GET"])
def home():
    #get data from user

    return render_template("index.html")

EXPECTED_COLUMNS=["gestation","parity","age","height","weight","smoke"]


#defining end point
@app.route("/hello",methods=["GET"])
def hello():
    return "hello World!"    


##define Your endpoint here
@app.route("/predict",methods=["POST"])
def get_prediction():
    #get data From user
    #baby_data_form=request.form
    baby_data_form=request.get_json()

    baby_data_cleaned = get_cleaned_data(baby_data_form)


    #convert into data frame
    baby_df = pd.DataFrame(baby_data_cleaned)
    baby_df = baby_df[EXPECTED_COLUMNS]

    path = os.path.join(os.path.dirname(__file__), "model.pkl")

    #load machine learning trained model
    with open(path,"rb")as f: 
        mymodel=pickle.load(f)
    

    #making prediction on user data
    prediction=mymodel.predict(baby_df)
    
    prediction=round(float(prediction[0]),2)


#return response IN json format
    response={"Prediction":prediction}
    #return render_template("index.html",prediction=prediction)
    return response


if __name__=="__main__":    
    app.run(debug=True)