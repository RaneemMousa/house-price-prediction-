
import os
import tarfile
from six.moves import urllib
DOWNLOAD_ROOT = "https://raw.githubusercontent.com/ageron/handson-ml/master/"
HOUSING_PATH = "datasets/housing"
HOUSING_URL = DOWNLOAD_ROOT + HOUSING_PATH + "/housing.tgz"
def fetch_housing_data(housing_url=HOUSING_URL, housing_path=HOUSING_PATH):
    if not os.path.isdir(housing_path):
        os.makedirs(housing_path)
    tgz_path = os.path.join(housing_path, "housing.tgz")
    urllib.request.urlretrieve(housing_url, tgz_path)
    housing_tgz = tarfile.open(tgz_path)
    housing_tgz.extractall(path=housing_path)
    housing_tgz.close()
fetch_housing_data()
import pandas as pd
def load_housing_data(housing_path=HOUSING_PATH):
    csv_path = os.path.join(housing_path, "housing.csv")
    return pd.read_csv(csv_path)
housing=load_housing_data()
#print(housing.head())
#print(housing.info())
#print(housing["ocean_proximity"].value_counts())
#print(housing.describe())
import matplotlib.pyplot as plt
housing.hist(bins=50, figsize=(20,15))
#plt.show()
import sklearn
import numpy as np
from sklearn.model_selection import train_test_split
train_set, test_set = train_test_split(housing, test_size=0.2, random_state=42)
housing["income_cat"] = np.ceil(housing["median_income"] / 1.5)
housing["income_cat"].where(housing["income_cat"] < 5, 5.0, inplace=True)
from sklearn.model_selection import StratifiedShuffleSplit
split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
for train_index, test_index in split.split(housing, housing["income_cat"]):
    strat_train_set = housing.loc[train_index]
    strat_test_set = housing.loc[test_index]
print(housing["income_cat"].value_counts() / len(housing))
for set in (strat_train_set, strat_test_set):
    set.drop(["income_cat"], axis=1, inplace=True)
housing = strat_train_set.copy()
#housing.plot(kind="scatter", x="longitude", y="latitude",alpha=0.1)
#plt.show()
#housing.plot(kind="scatter", x="longitude", y="latitude", alpha=0.4, s=housing["population"] / 100, label="population",c="median_house_value", cmap=plt.get_cmap("jet"), colorbar=True)
#plt.show()
#plt.legend()
corr_matrix = housing.corr()
#print(corr_matrix["median_house_value"].sort_values(ascending=False))
from pandas.plotting import scatter_matrix
#attributes = ["median_house_value", "median_income", "total_rooms", "housing_median_age"]
#scatter_matrix(housing[attributes], figsize=(12, 8))
#plt.show()
#housing.plot(kind="scatter", x="median_income", y="median_house_value",alpha=0.1)
#plt.show()
housing["rooms_per_household"] = housing["total_rooms"]/housing["households"]
housing["bedrooms_per_room"] = housing["total_bedrooms"]/housing["total_rooms"]
housing["population_per_household"]=housing["population"]/housing["households"]
corr_matrix = housing.corr()
print(corr_matrix["median_house_value"].sort_values(ascending=False))
housing = strat_train_set.drop("median_house_value", axis=1)
housing_labels = strat_train_set["median_house_value"].copy()
housing_num = housing.drop("ocean_proximity", axis=1)
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(strategy="median")
imputer.fit(housing_num)
print(imputer.statistics_)
print(housing_num.median().values)
X = imputer.transform(housing_num)
from sklearn.preprocessing import LabelBinarizer
encoder = LabelBinarizer()
housing_cat = housing["ocean_proximity"]
housing_cat_1hot = encoder.fit_transform(housing_cat)
print(housing_cat_1hot)