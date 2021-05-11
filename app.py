from flask import Flask, render_template, request
import pickle
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

# Load in our model
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))

@app.route('/', methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()

@app.route('/predict', methods=['POST'])
def predict():
    Fuel_Type_Diesel = 0
    if request.method == 'POST':
        # Reference name in index.html
        year  = int(request.form['Year'])
        year = 2020 - year
        present_price = float(request.form['Present_Price'])
        kms_driven = int(request.form['Kms_Driven'])
        owner = int(request.form['Owner'])

        # Handling Fuel Types
        Fuel_Type_Petrol = request.form['Fuel_Type_Petrol']
        if Fuel_Type_Petrol == 'Petrol':
            Fuel_Type_Petrol = 1
            Fuel_Type_Diesel = 0
        
        elif Fuel_Type_Petrol == 'Diesel':
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 1

        else:
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 0

        Seller_Type_Individual = request.form['Seller_Type_Individual']
        if Seller_Type_Individual == 'Individual':
            # Individual
            Seller_Type_Individual = 1
        else:
            # Dealer
            Seller_Type_Individual = 0

        Transmission_Manual = request.form['Transmission_Manual']
        if Transmission_Manual == 'Manual':
            Transmission_Manual = 1
        else:
            Transmission_Manual = 0
        
        prediction = model.predict([[present_price, 
        year, kms_driven, owner, Fuel_Type_Petrol, 
        Fuel_Type_Diesel, Seller_Type_Individual, Transmission_Manual]])

        output= round(prediction[0], 2)
        if output < 0:
            return render_template('predicted.html', prediction_text='Sorry, you cannot sell this car any longer')
        
        else:
            return render_template('predicted.html', prediction_text= f'You can sell this car at {output} lakhs')
    else:
        return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)