import pandas as pd
from sklearn.metrics import accuracy_score, roc_auc_score, f1_score, precision_score, recall_score

# Read CSV file
df = pd.read_csv('detection_results_generated_video.csv')

# Fill NaN values with False
df['is_deepfake'].fillna(False, inplace=True)

# Convert string values to boolean
df['is_deepfake'] = df['is_deepfake'].astype(bool)

# Calculate metrics for each model
models = df['model'].unique()
results = []

for model in models:
    model_df = df[df['model'] == model]
    accuracy = accuracy_score(model_df['label'], model_df['is_deepfake'])
    try:
        auc = roc_auc_score(model_df['label'], model_df['is_deepfake'])
    except ValueError:
        auc = 'AUC cannot be calculated'  # If there are not enough samples to calculate AUC
    f1 = f1_score(model_df['label'], model_df['is_deepfake'])
    precision = precision_score(model_df['label'], model_df['is_deepfake'])
    recall = recall_score(model_df['label'], model_df['is_deepfake'])
    results.append((model, accuracy, auc, f1, precision, recall))

# Calculate overall metrics
overall_accuracy = accuracy_score(df['label'], df['is_deepfake'])
try:
    overall_auc = roc_auc_score(df['label'], df['is_deepfake'])
except ValueError:
    overall_auc = 'AUC cannot be calculated'
overall_f1 = f1_score(df['label'], df['is_deepfake'])
overall_precision = precision_score(df['label'], df['is_deepfake'])
overall_recall = recall_score(df['label'], df['is_deepfake'])

# Write results to txt file
with open('model_results.txt', 'w') as f:
    for result in results:
        f.write(f"Model: {result[0]}, Accuracy: {result[1]:.4f}, AUC: {result[2]}, F1: {result[3]:.4f}, Precision: {result[4]:.4f}, Recall: {result[5]:.4f}\n")
    f.write(f"Overall Accuracy: {overall_accuracy:.4f}, Overall AUC: {overall_auc}, Overall F1: {overall_f1:.4f}, Overall Precision: {overall_precision:.4f}, Overall Recall: {overall_recall:.4f}\n")

print("Results have been written to model_results.txt.")
