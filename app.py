from flask import Flask,request,jsonify,render_template
import pandas as pd
import pickle
import os
from flask_restx import Api,Resource,fields

app=Flask(__name__)

#configure your swagger ui

api= Api(app,title="Flask api documnetation",description="test your api",doc="/docs")

#create name space
hello_namespace=api.namespace("Hello",description="hello apis",path="/hello")
user_namespace=api.namespace("User",description="User CRUD",path="/user")
pred_namespace=api.namespace("Prediction",description="Prediction APIs",path="/predict")


#create class for your namespace

@hello_namespace.route("/")
class Hello(Resource):
    
    def get(self):
        return {"msg":"hello World!"}

#CRUDS operation for user application
@user_namespace.route("/")
class User(Resource):
    def get(self):
        return {"msg":"hello User!"}
    def post(self):
        return {"msg":"hello User!"}
    def put(self):
        return {"msg":"hello User!"}
    def delete (self):
        return {"msg":"hello User!"}
    

input_model = pred_namespace.model("PredictionInput", {
    "gestation": fields.Float(required=True),
    "parity": fields.Integer(required=True),
    "age": fields.Float(required=True),
    "height": fields.Float(required=True),
    "weight": fields.Float(required=True),
    "smoke": fields.Float(required=True)
})

   
    

#prediction namespace docs
@pred_namespace.route('/')
class Prediction(Resource):
    @pred_namespace.expect(input_model)
    def post(self):
        """Predicts the baby's birth outcome based on input health parameters.
        **Request Body Format**
        -'gestation' (List[int]):Number of gestation days
        -'parity' (List[int]):Number of previous pregnancies
        -'age' (List[float]):Age of the mother 
        -'height' (List[float]):Height of the mother in centimeters
        -'weight' (List[float]):Weight of the mother in kilograms
        -'smoke' (List[float]):Smoking status (0 for non-smoker
        
        *returns:*
        -JSON response containing the predicted baby's birth outcome."""
        baby_data_form = request.get_json()

        baby_data_cleaned = get_cleaned_data(baby_data_form)

        baby_df = pd.DataFrame(baby_data_cleaned)
        baby_df = baby_df[EXPECTED_COLUMNS]
        
        #get data From user
        #baby_data_form=request.form
        
        #convert into data frame
        
        

        #load machine learning trained model
        path = os.path.join(os.path.dirname(__file__), "model.pkl")
        with open(path,"rb")as f: 
            mymodel=pickle.load(f)
        

        #making prediction on user data
        prediction=mymodel.predict(baby_df)
        
        prediction=round(float(prediction[0]),2)


    #return response IN json format
        response={"Prediction":prediction}
        #return render_template("index.html",prediction=prediction)
        return response


    

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


@app.route("/hello",methods=["GET"])
def hello():
    return {"msg":"hello World!"}

#creating home page
@app.route("/",methods=["GET"])
def home():
    #get data from user

    return render_template("index.html")

EXPECTED_COLUMNS=["gestation","parity","age","height","weight","smoke"]


#defining end point
   


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