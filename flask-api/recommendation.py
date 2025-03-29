from flask import Flask, jsonify
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

# Load and preprocess dataset
def load_data():
    file_path = "data.csv"  # Adjust the path as needed
    df = pd.read_csv(file_path, header=None)
    transactions = df.apply(lambda row: row.dropna().tolist(), axis=1).tolist()
    return transactions

# Train the recommendation model
def train_model(transactions):
    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)
    df_encoded = pd.DataFrame(te_ary, columns=te.columns_)
    frequent_itemsets = apriori(df_encoded, min_support=0.01, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
    return rules

# Initialize Flask app
app = Flask(__name__)
transactions = load_data()
rules = train_model(transactions)

@app.route("/recommend/<product>", methods=["GET"])
def recommend(product):
    related_rules = rules[rules['antecedents'].apply(lambda x: product in x)]
    recommendations = set()
    for _, row in related_rules.iterrows():
        recommendations.update(row['consequents'])
    return jsonify({"recommendations": list(recommendations)})

if __name__ == "__main__":
    app.run(debug=True)