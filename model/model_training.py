import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize

# Shuffling data and writing to the file (This is to be done only once) 
dataFrame = pd.read_csv('data/demo.csv')
dataFrame = dataFrame.sample(frac=1)
dataFrame.to_csv('data/shuffledDemo.csv')

# Clean data
server = pd.get_dummies(dataFrame['server'])
created = pd.get_dummies(dataFrame['created_at'])
dataFrame.drop(['server'], axis=1, inplace=True)
dataFrame.drop(['created_at'], axis=1, inplace=True)
print(dataFrame.head())
dataFrame = pd.concat([dataFrame, server, created], axis=1)
print(dataFrame.columns)
features = [column for column in dataFrame.columns if column != 'username' and column != 'id' and column != 'Threat']
print(features)

# Preprocess data 
features_normalized = normalize(dataFrame[features])
expected_result = dataFrame['Threat']
print(expected_result)

# Spliting the data in train and test where train covers 70% of the data frame
X_train, X_test, y_train, y_test = train_test_split(features_normalized, expected_result, random_state=42, test_size=0.3)

# Train model
model = LogisticRegression(class_weight='balanced')
model.fit(X_train, y_train)
with open('model.pickle', 'wb') as f:
    pickle.dump(model, f)