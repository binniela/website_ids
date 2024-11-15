from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import joblib  # For loading the model
from sklearn.preprocessing import LabelEncoder
import logging

# Initialize the Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.ERROR)

# Load your trained model
model = joblib.load('decision_tree_model.pkl')  # Ensure the file path is correct

# Load the protocol_type encoder classes
protocol_type_encoder = LabelEncoder()
protocol_type_encoder.classes_ = np.load('protocol_type_classes.npy', allow_pickle=True)

# Class descriptions for better user interpretation
class_descriptions = {
    'normal': 'The network traffic is normal.',
    'anomaly': 'Potential anomaly detected in network traffic.'
}

# Define the required input keys
required_keys = [
    'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes',
    'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins', 'logged_in',
    'num_compromised', 'root_shell', 'su_attempted', 'num_root', 'num_file_creations',
    'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login', 'is_guest_login',
    'count', 'srv_count', 'serror_rate', 'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate',
    'same_srv_rate', 'diff_srv_rate', 'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count',
    'dst_host_same_srv_rate', 'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
    'dst_host_srv_diff_host_rate', 'dst_host_serror_rate', 'dst_host_srv_serror_rate',
    'dst_host_rerror_rate', 'dst_host_srv_rerror_rate'
]

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the input data from the POST request
        data = request.get_json()
        
        # Validate input data
        for key in required_keys:
            if key not in data:
                return jsonify({'error': f'Missing field: {key}'}), 400

        # Validate protocol_type
        if data['protocol_type'] not in protocol_type_encoder.classes_:
            return jsonify({'error': f"Unknown protocol_type: {data['protocol_type']}"}), 400

        # Prepare the input features
        features = [
            data['duration'],
            protocol_type_encoder.transform([data['protocol_type']])[0],  # Encode protocol_type
            data['service'], data['flag'], data['src_bytes'], data['dst_bytes'],
            data['land'], data['wrong_fragment'], data['urgent'], data['hot'],
            data['num_failed_logins'], data['logged_in'], data['num_compromised'],
            data['root_shell'], data['su_attempted'], data['num_root'], data['num_file_creations'],
            data['num_shells'], data['num_access_files'], data['num_outbound_cmds'],
            data['is_host_login'], data['is_guest_login'], data['count'], data['srv_count'],
            data['serror_rate'], data['srv_serror_rate'], data['rerror_rate'], data['srv_rerror_rate'],
            data['same_srv_rate'], data['diff_srv_rate'], data['srv_diff_host_rate'],
            data['dst_host_count'], data['dst_host_srv_count'], data['dst_host_same_srv_rate'],
            data['dst_host_diff_srv_rate'], data['dst_host_same_src_port_rate'],
            data['dst_host_srv_diff_host_rate'], data['dst_host_serror_rate'],
            data['dst_host_srv_serror_rate'], data['dst_host_rerror_rate'],
            data['dst_host_srv_rerror_rate']
        ]
        
        # Convert to DataFrame
        df = pd.DataFrame([features], columns=required_keys)

        # Predict using the trained model
        prediction = model.predict(df)[0]

        # Send the prediction result back to the client
        return jsonify({
            'prediction': prediction,
            'description': class_descriptions.get(prediction, 'Unknown prediction class.')
        })

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=False)  # Ensure debug=False in production
