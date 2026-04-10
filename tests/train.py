"""train.py
Train the churn model and save pipeline to churn_model.pkl
Usage: python train.py
"""
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score


def main(csv_path: str = "Telco-Customer-Churn.csv"):
    df = pd.read_csv(csv_path)

    if 'customerID' in df.columns:
        df.drop('customerID', axis=1, inplace=True)

    if 'TotalCharges' in df.columns:
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
        df['TotalCharges'].fillna(df['TotalCharges'].median(), inplace=True)

    if 'Churn' in df.columns:
        df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})
    else:
        raise RuntimeError('Dataset must contain a Churn column')

    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    if 'Churn' in numerical_cols:
        numerical_cols.remove('Churn')

    preprocessor = ColumnTransformer(transformers=[
        ('num', StandardScaler(), numerical_cols),
        ('cat', OneHotEncoder(drop='first', sparse=False), categorical_cols)
    ])

    X = df.drop('Churn', axis=1)
    y = df['Churn']
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp)

    smote = SMOTE(random_state=42)
    # Fit preprocessor on training data and transform to numeric array before SMOTE
    preprocessor.fit(X_train)
    X_train_trans = preprocessor.transform(X_train)
    # X_train_trans is a numpy array after ColumnTransformer; now apply SMOTE
    X_train_res, y_train_res = smote.fit_resample(X_train_trans, y_train)

    model = RandomForestClassifier(n_estimators=200, random_state=42, class_weight='balanced')
    # Recreate a pipeline that includes the preprocessor and classifier.
    # Since SMOTE was applied to transformed arrays, we need a pipeline for inference only.
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', model)
    ])

    # Fit classifier on the resampled numeric array. For convenience, transform X_train_res back
    # into the pipeline by fitting the classifier using the preprocessor's inverse mapping isn't
    # straightforward, so we refit the pipeline on the original X_train and y_train_res by
    # creating a small helper: create X_train_res_df by sampling from X_train using indices from
    # SMOTE is not returning indices, so instead retrain the classifier by using the resampled
    # array directly: fit the classifier on X_train_res and y_train_res after bypassing preprocessor.
    # We'll fit the classifier on the transformed space and then wrap it in a pipeline that
    # applies the preprocessor during inference.
    model.fit(X_train_res, y_train_res)
    # Attach trained classifier to the pipeline
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', model)
    ])

    y_pred = pipeline.predict(X_val)
    y_proba = pipeline.predict_proba(X_val)[:, 1]

    print("Classification Report:\n", classification_report(y_val, y_pred))
    print("ROC-AUC Score:", roc_auc_score(y_val, y_proba))

    joblib.dump(pipeline, "churn_model.pkl")
    print('Model trained and saved to churn_model.pkl')


if __name__ == '__main__':
    main()
