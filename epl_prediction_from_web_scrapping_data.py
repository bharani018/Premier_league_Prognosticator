# -*- coding: utf-8 -*-
"""EPL_prediction_from_web_scrapping_Data.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1TToWATGgjbQFHBW_aSaGTblxWme0AvM2
"""

import pandas as pd

data = pd.read_csv('/content/drive/MyDrive/matches.csv')

data1  = data[data['season'] == '2023-24']
data2 = data[data['season'] == '2022-23']

data1 = data1.drop(columns = 'season')

data1.head(3)

data1.dtypes

data1['date'] = pd.to_datetime(data1['date'], format = '%m/%d/%Y')

data1.dtypes

data1['Matchup'] = data1['opponent'] +' vs '+ data1['team']

new_df = data1.drop_duplicates(subset=['date', 'time', 'round', 'day', 'referee'])

new_df.head()

new_df.shape



new_df.isnull().sum()

new_df = new_df.dropna(subset=['result'])

new_df.isnull().sum()

new_df.shape

#  58 Matches has to be played from today
# So here we have 322 data (322 matches played this season)
380-58

new_df = new_df.drop(columns = 'notes')

new_df['team'] = new_df['team'].str.lower()
new_df['Matchup'] = new_df['Matchup'].str.lower()
new_df['opponent'] = new_df['opponent'].str.lower()

new_df['venue']= new_df['venue'].map({'Home':1,'Away':0})

new_df['result']= new_df['result'].map({'W':3,'D':1,'L':0})

new_df['day'].value_counts()



new_df['day'] = new_df['day'].astype("category").cat.codes

"""0 - friday

1 - saturday

2 - sunday

.
.
.


"""

new_df.head(2)

new_df['team_code'] = new_df['team'].astype("category").cat.codes

new_df['ref_code'] = new_df['referee'].astype("category").cat.codes

new_df['opp_code'] = new_df['opponent'].astype("category").cat.codes

new_df.to_csv('new.csv')

"""MODEL SELECTION AND DEVELOPMENT

"""



from sklearn.model_selection import train_test_split

x = new_df[[ 'day', 'venue', 'gf', 'ga', 'xg', 'xga', 'team_code', 'opp_code','ref_code']]
y = new_df['result']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state=42)

from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report



nb_classifier = GaussianNB()

nb_classifier.fit(x_train, y_train)

y_pred = nb_classifier.predict(x_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

print("Classification Report:\n", classification_report(y_test, y_pred))

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

li_reg = LinearRegression()

li_reg.fit(x_train, y_train)

y_pred_lr = li_reg.predict(x_test)

mse = mean_squared_error(y_test, y_pred)

r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse:.2f}")
print(f"R-squared: {r2:.2f}")

from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report

svm_model = SVC(kernel='linear')
svm_model.fit(x_train, y_train)

y_pred_svm = svm_model.predict(x_test)

accuracy = accuracy_score(y_test, y_pred_svm)
print(f"Accuracy: {accuracy:.2f}")

print("Classification Report:\n", classification_report(y_test, y_pred_svm))

from sklearn.ensemble import RandomForestClassifier

rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(x_train, y_train)

y_pred = rf_classifier.predict(x_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

print("Classification Report:\n", classification_report(y_test, y_pred))