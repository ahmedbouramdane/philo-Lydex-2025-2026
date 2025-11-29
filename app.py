import pandas as pd
from flask import Flask, render_template, send_file
import math
import qrcode
import io
import requests 
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/qrcode")
def get_qrcode():
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSc9KEg7Nh9KttTXu6i12-niwD09h8qBglEy2mNnGQA089Y_6A/viewform?usp=header/viewform" # Replace with actual URL if known, or keep generic
    # url = "https://docs.google.com/forms" 
    
    img = qrcode.make(form_url)
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0) 
    return send_file(buf, mimetype='image/png')

@app.route("/Ahmed-projects/Philo", methods=["GET", "POST"])
def index():
    # save a copy of the sheet in data dir with name philo-lydex.csv and update it every time the page is refreshed
    import dotenv
    dotenv.load_dotenv()
    URL = os.getenv("URL")
    response = requests.get(URL)
    with open("data/philo-lydex.csv", "wb") as f:
        f.write(response.content)

    data = pd.read_csv(URL, encoding="utf-8")
    def extract_score(val):
        if pd.isna(val):
            return None
        if isinstance(val, str):
            try:
                return float(val.split('/')[0].strip())
            except:
              return None
        return float(val)

    data['Score'] = data['Score'].apply(extract_score)
    data = data.sort_values(by="Score", ascending=False)
    data = data.where(pd.notnull(data), None)
    data["rank"] = data["Score"].rank(method="dense", ascending=False).astype(int)
    
    scores = data['Score'].dropna()
    avg_score = scores.mean()
    max_score = scores.max()
    min_score = scores.min()
    full_marks_count = (scores == 21).sum()
    
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
    
    return render_template(
        "index.html", 
        tables=data.to_dict(orient="records"), 
        len=data.shape[0],
        avg_score=avg_score,
        max_score=max_score,
        min_score=min_score,
        full_marks_count=full_marks_count,
        score_ranges=range_counts[:4] 
    )

if __name__ == "__main__":
    app.run(debug=True)
