"""Lab 2 model, used by make_numbers.py and copied into the notebooks. Real data: UCI 697 (Realinho et al., 2022), CC BY 4.0."""
import pandas as pd, numpy as np, os
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
HERE = os.path.dirname(os.path.abspath(__file__)); SEED = 697
CATS = ['Marital status', 'Application mode', 'Course', 'Previous qualification', 'Nacionality', "Mother's qualification", "Father's qualification", "Mother's occupation", "Father's occupation"]
def load(path=None):
    D = pd.read_csv(path or f'{HERE}/raw/data.csv', sep=';'); D.columns = [c.strip() for c in D.columns]; D['y'] = (D.Target == 'Dropout').astype(int); return D
def columns(D):
    s1 = [c for c in D.columns if '1st sem' in c]; s2 = [c for c in D.columns if '2nd sem' in c]; enrol = [c for c in D.columns if c not in s1 + s2 + ['Target', 'y']]
    return {'enrol': enrol, 'sem1': enrol + s1, 'sem2': enrol + s1 + s2}
def split(D): return train_test_split(D.index, test_size=.2, random_state=SEED, stratify=D.y)
def fit(D, cols, tr):
    X = pd.get_dummies(D[cols].astype({c: 'category' for c in cols if c in CATS}), drop_first=True).astype(float)
    m = make_pipeline(StandardScaler(), LogisticRegression(max_iter=3000, C=.3)).fit(X.loc[tr], D.y.loc[tr]); return m, X
