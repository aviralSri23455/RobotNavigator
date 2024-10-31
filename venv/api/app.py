# app.py
from flask import Flask, jsonify
from simulation import Simulation

app = Flask(__name__)

@app.route('/start-simulation', methods=['POST'])
def start_simulation():
    sim = Simulation()
    sim.run()
    return jsonify({'message': 'Simulation started'})

if __name__ == '__main__':
    app.run(debug=True)
