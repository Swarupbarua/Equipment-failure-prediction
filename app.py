from flask import Flask, jsonify, request, flash, redirect, url_for, send_file,render_template
import pandas as pd
import numpy as np
import string
import pickle
import os
from sklearn.externals import joblib
from werkzeug.utils import secure_filename

# https://www.tutorialspoint.com/flask
import flask
app = Flask(__name__, static_url_path='/static', template_folder='templates')


###################################################
# feature engineering - Max change over time
def get_max(xs):
	l = [x for x in xs]
	return (max(l)-min(l))
# Get Avg of features
def get_avg(xs):
	l = [x for x in xs]
	return (sum(l)/len(l))
###################################################


@app.route('/')
def hello_world():
	return 'Hello World!'


@app.route('/index')
def index():
	return flask.render_template('index.html')


# Download API
@app.route('/download')
def download_file():
	path = "template.csv"
	return send_file(path, as_attachment=True)


@app.route('/predict', methods=['GET','POST'])
def predict():
	if request.method == 'POST':
		if 'file' not in request.files:
			flash('No file part')
			return redirect(url_for('index'))
		file = request.files['file']
		if file.filename == '':
			flash('No selected file')
			return redirect(url_for('index'))
		
		data_csv = secure_filename(file.filename)
		file.save(data_csv)  	 
		project_data = pd.read_csv(data_csv)                # read csv data
		
		project_data = project_data.replace('na',np.nan)    # replace na with nan if any
		for col in project_data.columns:                    # Convert all column values to numeric
			project_data[col] = pd.to_numeric(project_data[col])
		data = project_data.drop(columns=drop_columns, axis=1)  # drop most nan columns
		data = data.iloc[:,1:].fillna(data.median())        # Fill nan values with median
		df = data.values
		df = scaler.transform(df)                           # normalize the data
		data = pd.DataFrame(df, columns=data.columns,index=data.index)
		data.drop(columns='sensor54_measure', axis=1, inplace=True)  # drop sensor54
		
		# feature engineering - Max change over time & moving avg
		MaxChange = pd.DataFrame()
		MoveAvg = pd.DataFrame()
		for i in range(len(hist_sensor_sort)):
			col = [l for l in hist_col if hist_sensor_sort[i] in l]
			col1 = hist_sensor_sort[i]+'_MaxC'
			col2 = hist_sensor_sort[i]+'_MoveAvg'
			MaxChange[col1] = data[col].apply(get_max, axis=1)
			MoveAvg[col2] = data[col].apply(get_avg, axis=1)
		data = pd.concat([data, MaxChange, MoveAvg], axis=1)
		
		# feature engineering - Avg of non TB features
		data['AvgChangeNT'] = data[non_TB_feature].apply(get_avg, axis=1)
		
		# Predict
		predict_y = best_xgb.predict(data)   
		if predict_y[0] == 1:
			prediction = 'Downhole failure'
		else:
			prediction = 'Surface failure'
		os.remove(data_csv)
		
		return jsonify({'prediction': prediction})


if __name__ == '__main__':
	app.config['SECRET_KEY'] = "<some-key>"
	app.config['SESSION_TYPE'] = 'filesystem'
	app.config['SESSION_PERMANENT']= False
	
	drop_columns, hist_sensor_sort, hist_col, non_TB_feature = joblib.load('All_required_features.pkl')
	best_xgb = joblib.load('XgBoost_model.pkl')
	scaler = joblib.load('norm_scaler.pkl')
	app.run(host='0.0.0.0', port=8080)
