from app import app

##first positive test case for'/hello' route

def test_hello_route_success():
    tester=app.test_client()
    response=tester.get('/hello')

    assert response.status_code==200




##failure test case for'/hello' route

#def test_hello_route_failure():
  #   tester=app.test_client()
   # response=tester.get('/hello')

    #assert response.status_code==500


##positive test case for'/predict' route    
def test_predict_route_success():
    tester=app.test_client()  
    data = {
    "gestation": 279,
    "parity": 1,
    "age": 25,
    "height": 160,
    "weight": 60,
    "smoke": 0
}
    response = tester.post('/predict',json=data)

    assert response.status_code==200



#test case for worng url /opredict instead of /predict
def test_predict_route_wrong_url():
    tester=app.test_client()  
    data = {
    "gestation": 279,
    "parity": 1,
    "age": 25,
    "height": 160,
    "weight": 60,
    "smoke": 0
}
    response = tester.post('/opredict',json=data)

    assert response.status_code==404



#test case for invalid data data{}
def test_predict_route_invalid_data():
    tester=app.test_client()   
    data = {
    "gestation": 279,
    "parity": 1,
    "age": 25,
    "height": 160,
    "weight": 60,
    "smoke": 0
}
   

    response = tester.post('/predict',json=data)

    assert response.status_code==400

#test case for worng methind get= post
def test_predict_route_wrong_method():
    tester=app.test_client()  
    data = {
    "gestation": 279,
    "parity": 1,
    "age": 25,
    "height": 160,
    "weight": 60,
    "smoke": 0
}
    response = tester.get('/predict',json=data)

    assert response.status_code==405


    








