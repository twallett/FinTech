#%%
import pickle
import pandas as pd
from sklearn.preprocessing import QuantileTransformer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.base import clone

with open('ensemble.pkl', 'rb') as f:
    ensemble = pickle.load(f)
    
df = pd.read_csv("Clean_NYC_Property_Data.csv", 
                 index_col=0)

df = df.sample(1000000)

transformer = QuantileTransformer(output_distribution="normal")
df = transformer.fit_transform(df)

X = df[:,[6,7,9]]
Y = df[:,5]

X_train, X_test, Y_train, Y_test = train_test_split(X ,
                                                    Y, 
                                                    test_size= 0.2)

ensemble_clone = clone(ensemble)

for i, (estimator_name, estimator) in enumerate(ensemble_clone.estimators):
    cv_scores = cross_val_score(estimator, X_train, Y_train, cv=5, scoring='r2')
    mean_cv_score = cv_scores.mean()
    print(f"{estimator_name} Cross-validated R2 Score: {mean_cv_score:.4f}")
# %%
