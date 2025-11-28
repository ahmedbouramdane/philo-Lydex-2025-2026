import pandas as pd
from flask import Flask, render_template
import math

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/Ahmed-projects/Philo", methods=["GET", "POST"])
def index():
    URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ3cpDBJwgW7J_0oTu0SgNMMaPYbzNFbLoLH_3GeOj0rZ0uQqaQcuIEhEZLi5ggfc6LHTOrFK890efI/pub?gid=589373664&single=true&output=csv"

    data = pd.read_csv(URL, encoding="utf-8")
    # Extract numeric score from strings like "5 / 21"
    def extract_score(val):
        if pd.isna(val):
            return None
        if isinstance(val, str):
            # Try to split and take the first part (before " / ")
            try:
                return float(val.split('/')[0].strip())
            except:
              return None
        return float(val)

    data['Score'] = data['Score'].apply(extract_score)
    data = data.sort_values(by="Score", ascending=False)
    data = data.where(pd.notnull(data), None)
    data["rank"] = data["Score"].rank(method="dense", ascending=False).astype(int)
    
    # Calculate analytics
    scores = data['Score'].dropna()
    avg_score = scores.mean()
    max_score = scores.max()
    min_score = scores.min()
    full_marks_count = (scores == 21).sum()
    
    # Calculate score ranges
    def categorize_score(score):
        if score <= 5:
            return 0
        elif score <= 10:
            return 1
        elif score <= 15:
            return 2
        elif score <= 20:
            return 3
        else:  # score == 21
            return 4
    
    # Initialize range counts
    range_counts = [0, 0, 0, 0, 0]  # 0-5, 5-10, 10-15, 15-20, 21
    for score in scores:
        if not math.isnan(score):
            if score == 21:
                range_counts[4] += 1
            elif score <= 5:
                range_counts[0] += 1
            elif score <= 10:
                range_counts[1] += 1
            elif score <= 15:
                range_counts[2] += 1
            elif score <= 20:
                range_counts[3] += 1
    
    # Exclude the full marks from the last range (15-20) since 21 is separate
    # We've already handled 21 separately
    
    return render_template(
        "index.html", 
        tables=data.to_dict(orient="records"), 
        len=data.shape[0],
        avg_score=avg_score,
        max_score=max_score,
        min_score=min_score,
        full_marks_count=full_marks_count,
        score_ranges=range_counts[:4]  # Only the first 4 ranges (0-20)
    )

if __name__ == "__main__":
    app.run(debug=True)