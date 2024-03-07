#%%
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import VotingRegressor
import pickle

seed = 123

model1 = DecisionTreeRegressor(max_depth=10,
                               random_state=seed)
model2 = RandomForestRegressor(max_depth =10,
                               n_estimators=50,
                               random_state=seed)
model3 = LinearRegression()
model4 = MLPRegressor(hidden_layer_sizes=(100),
                      activation="logistic",
                      max_iter= 10000,
                      momentum=0.999,
                      random_state=seed)

ensemble = VotingRegressor(estimators=[('decision_tree', model1), 
                                       ('random_forest', model2), 
                                       ('linear_regression', model3),
                                       ('multi-layered perceptron', model4)],
                           verbose=True)

with open('ensemble.pkl', 'wb') as f:
    pickle.dump(ensemble, f)
# %%
