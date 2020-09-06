# Equipment-failure-prediction
# ConocoPhilips Equipment Failure Prediction

### Here i have solved Conocophilips equipment failure problem using Machine learning and Deep learning.

Dataset source: Data can be obtained from here. 
https://www.kaggle.com/c/equipfails/data

## This dataset has 2 types of data present in it. 
1. Static sensor measures
2. Dynamic sensor measures (time based)

## Train ipython Notebook
  - Equip_failure.ipynb

## Test 
  - app.py

Below are some modeling i have implemented.
  - Logistic regression
  - Random forest
  - XgBoost
  - Ensemble model (using LSTM and Conv1D)
  - Hybrid model (usin LSTM and RF)
  
Among all the above models XgBoost perform the best and achived 85% f1 score.

### In app.py file i have used flask to deploy my model.
<img src='https://github.com/Swarupbarua/Equipment-failure-prediction/blob/master/web.PNG?raw=true' width="800" height="400" />

First download the template csv file from the above page. Fill all the sensor data and submit. Output will be displayed.
<img src='https://github.com/Swarupbarua/Equipment-failure-prediction/blob/master/result.PNG?raw=true' width="800" height="400" />
