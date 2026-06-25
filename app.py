from flask import Flask,request,jsonify
import pandas as pd
import pickle

app=Flask(__name__)


##define Your endpoint here
@app.route("/predict",methods=["POST"])
def get_prediction():
    #get data From user
    baby_data=request.get_json()

    #convert into data frame
    baby_df=pd.DataFrame(baby_data) 

    #load machine learning trained model
    with open("model/model.pkl","rb")as f:
        mymodel=pickle.load(f)
    

    #making prediction on user data
    prediction=mymodel.predict(baby_df)
    
    prediction=round(float(prediction),2)



    response={"prediction":prediction}
    return jsonify(response)



if __name__=="__main__":    
    app.run(debug=True)