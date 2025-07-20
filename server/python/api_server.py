from flask import Flask, jsonify, request
import pandas as pd
import os

app = Flask(__name__)

# Define base data directory
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "csv_data")

# Helper function to load CSV data
def load_csv_data(file_name):
    file_path = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(file_path):
        return None
    return pd.read_csv(file_path)

@app.route('/api/demographics', methods=['GET'])
def get_demographics():
    """Endpoint to fetch patient demographics data"""
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    dob = request.args.get('dob')
    # Load demographics data
    demographics_df = load_csv_data('demographics.csv')
    if demographics_df is None:
        return jsonify({"error": "Demographics data not found"}), 404
    
    # Find by demographics if provided
    if all([first_name, last_name, dob]):
        patient_id = find_patient_id(first_name, last_name, dob)
        if not patient_id:
            return jsonify({"error": f"Patient with name {first_name} {last_name} and DOB {dob} not found"}), 404
        
        result = demographics_df[demographics_df['patient_id'] == patient_id]
        return jsonify(result.to_dict(orient='records'))
    
    # Return all records if no identifiers specified
    return jsonify(demographics_df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
