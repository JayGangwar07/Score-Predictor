from flask import Flask, request, jsonify, render_template
import numpy as np
import pickle

app = Flask(__name__)
@app.route('/')
def temp():
  return render_template('index.html')
# Load the model
model = pickle.load(open('forest.pkl', 'rb'))

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # Extract input values
    batting_team = data['battingTeam']
    bowling_team = data['bowlingTeam']
    overs = data['overs']
    runs = data['runs']
    wickets = data['wickets']
    runs_last5 = data['runsLast5']
    wickets_last5 = data['wicketsLast5']

    # One-hot encode teams (simplified example)
    teams = ['CSK', 'DD', 'KXIP', 'KKR', 'MI', 'RR', 'RCB', 'SRH']
    batting = [1 if team == batting_team else 0 for team in teams]
    bowling = [1 if team == bowling_team else 0 for team in teams]

    # Form input array
    input_array = batting + bowling + [runs, wickets, overs, runs_last5, wickets_last5]
    input_array = np.array([input_array])

    # Make prediction
    prediction = int(model.predict(input_array)[0])
    return jsonify({'prediction': f'{prediction-5} to {prediction+5}'})

if __name__ == '__main__':
    app.run(debug=True)
  
