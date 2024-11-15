# IDS Prediction API

This Flask app serves a machine learning model to predict whether network traffic is normal or anomalous.

## Setup

1. Install dependencies:

2. Ensure your model file (`ids_model.joblib`) is in the same directory as `app.py`.

3. Run the app:

4. Make POST requests to `http://127.0.0.1:5000/predict` with the required features in JSON format.

## Example Request:

```json
{
 "duration": 100,
 "protocol_type": "tcp",
 "service": "http",
 "flag": "SF",
 "src_bytes": 200,
 "dst_bytes": 300,
 "land": 0,
 "wrong_fragment": 0,
 "urgent": 0,
 "hot": 0,
 "num_failed_logins": 1,
 "logged_in": 1,
 "num_compromised": 0,
 "root_shell": 0,
 "su_attempted": 0,
 "num_root": 0,
 "num_file_creations": 0,
 "num_shells": 0,
 "num_access_files": 0,
 "num_outbound_cmds": 0,
 "is_host_login": 0,
 "is_guest_login": 0,
 "count": 5,
 "srv_count": 10,
 "serror_rate": 0.01,
 "srv_serror_rate": 0.02,
 "rerror_rate": 0.03,
 "srv_rerror_rate": 0.04,
 "same_srv_rate": 0.5,
 "diff_srv_rate": 0.1,
 "srv_diff_host_rate": 0.2,
 "dst_host_count": 10,
 "dst_host_srv_count": 20,
 "dst_host_same_srv_rate": 0.3,
 "dst_host_diff_srv_rate": 0.2,
 "dst_host_same_src_port_rate": 0.1,
 "dst_host_srv_diff_host_rate": 0.1,
 "dst_host_serror_rate": 0.05,
 "dst_host_srv_serror_rate": 0.03,
 "dst_host_rerror_rate": 0.02,
 "dst_host_srv_rerror_rate": 0.01
}
