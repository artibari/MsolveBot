import pandas as pd
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import nltk
#nltk.download('wordnet')

df = pd.read_csv("D:\\NEW MSOLVE\\msolve_data\\training.csv")
print(df.head())
X= df['issue']
y = df['class']
