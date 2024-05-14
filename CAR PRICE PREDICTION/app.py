from flask import Flask, render_template,request,jsonify
import numpy as np
import requests
import joblib
import sklearn
from sklearn.preprocessing import StandardScaler


app = Flask(__name__)

model = joblib.load('random_forest_model.joblib')

@app.route('/',methods=['GET'])

def Home():
    title = "CAR PRICE PREDICTOR"
    return render_template("index.html",title=title)


standard_to = StandardScaler()

@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel=0

    if request.method == 'POST':
        Year = int(request.form['Year'])
        Present_Price=float(request.form['Present_Price'])
        Kms_Driven=int(request.form['Kms_Driven'])
        Kms_Driven2=np.log(Kms_Driven)
        Owner=int(request.form['Owner'])
        Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
        if(Fuel_Type_Petrol=='Petrol'):
                Fuel_Type_Petrol=1
                Fuel_Type_Diesel=0
        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
        Year=2020-Year
        Seller_Type_Individual=request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0	
        Transmission_Mannual=request.form['Transmission_Mannual']
        if(Transmission_Mannual=='Mannual'):
            Transmission_Mannual=1
        else:
            Transmission_Mannual=0
        prediction=model.predict([[Present_Price,Kms_Driven2,Owner,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Mannual]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="CAR IS NOT FOR SALE")
        else:
            return render_template('index.html',prediction_text="SELL CAR AT {} LAKH".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)

