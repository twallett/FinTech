#%%
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
import numpy as np

df = pd.read_csv("Clean_MD_Property_Data.csv", 
                 index_col=0)

X = df.drop(columns='consideration')
Y = df.consideration

X_train, X_test, Y_train, Y_test = train_test_split(X ,
                                                    Y, 
                                                    test_size= 0.2)

pca = PCA(n_components=3)
X_train_pca = pca.fit_transform(X_train)

pca_components_abs = np.abs(pca.components_)

column_names = df.drop(columns='consideration').columns

feature_importance_scores = pca_components_abs.sum(axis=0)

best_feature_indices = np.argsort(feature_importance_scores)[::-1][:3]

best_feature_names = column_names[best_feature_indices]

print(best_feature_names)

# %%
