# -*- coding: utf-8 -*-
from flask import Flask, render_template_string, request, url_for
import random
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    total_prob = 0
    total_prob_display = "0"
    comparison_text = ""
    ae_definitions = {
        "A": "最高ランク（魅力的・完璧）",
        "B": "かなり良い",
        "C": "普通",
        "D": "やや微妙",
        "E": "論外（低評価）"
    }
    age_options = ["10代", "20代前半", "20代後半", "30代前半", "30代後半", "40代以上"]
    rank_options = ["A", "B", "C", "D", "E"]

    input_data = {"age": "", "appearance": "", "personality": "", "economic": "", "fashion": ""}
    kame_image = ""

    if request.method == "POST":
        input_data["age"] = request.form.get("age", "").strip()
        input_data["appearance"] = request.form.get("appearance", "").upper()
        input_data["personality"] = request.form.get("personality", "").upper()
        input_data["economic"] = request.form.get("economic", "").upper()
        input_data["fashion"] = request.form.get("fashion", "").upper()

        rank_values = {"A": 0.05, "B": 0.04, "C": 0.03, "D": 0.02, "E": 0.01}
        age_bonus = {"10代": 0.5, "20代前半": 0.8, "20代後半": 1.0, "30代前半": 1.2, "30代後半": 1.0, "40代以上": 0.9}

        base_prob = (rank_values.get(input_data["appearance"], 0) *
                     rank_values.get(input_data["personality"], 0) *
                     rank_values.get(input_data["economic"], 0) *
                     rank_values.get(input_data["fashion"], 0)) * 100

        total_prob = base_prob * age_bonus.get(input_data["age"], 1)
        total_prob_display = f"{total_prob:.10f}".rstrip('0').rstrip('.')  # 末尾ゼロ削除

        comparisons = [
            (1 / 10295472 * 100, "ロト7当選確率"),
            (0.0000001, "隕石激突確率"),
            (0.0001, "雷に打たれる確率"),
            (0.01, "交通事故に遭う確率（年間）"),
            (0.000009, "飛行機事故で死亡する確率"),
            (0.00001, "ジャンボ宝くじ1等当選確率"),
        ]

        if total_prob > 0:
            comparison_text = "<h3>比較対象:</h3><ul>"
            for ref_prob, label in comparisons:
                comparison_text += f"<li>{label}（約{ref_prob:.8f}%）の約{total_prob/ref_prob:.1f}倍</li>"
            comparison_text += "</ul>"
        else:
            comparison_text = "<p>確率が0%未満のため、例えようがありません。</p>"

        static_folder = os.path.join(app.root_path, 'static')
        kame_images = [f for f in os.listdir(static_folder) if f.startswith("kame_face")]
        if kame_images:
            kame_image = url_for('static', filename=random.choice(kame_images))

    return render_template_string("""
    <html><head>
    <style>
    body {
        background-image: url('{{ url_for('static', filename='midori_kame_bg.jpg') }}');
        background-size: cover;
        background-attachment: fixed;
        font-family: Arial, sans-serif;
        color: white;
        padding: 20px;
    }

    h1 {
        font-family: "Comic Sans MS", "Arial Black", sans-serif;
        font-size: 5em;
        margin: 10px;
        text-align: center;
        background: linear-gradient(45deg, #f9d423, #ff4e50);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 2px 2px 5px rgba(255,255,255,0.6);
    }

    .container {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
    }

    form {
        background-color: rgba(0,0,0,0.5);
        padding: 20px;
        border-radius: 10px;
        flex: 1;
        min-width: 250px;
        max-width: 400px;
        margin: 10px;
        text-align: left;
    }

    .description {
        font-size: 1em;
        margin-bottom: 10px;
        color: #ffffcc;
    }

    .result-area {
        background-color: rgba(0,0,0,0.5);
        padding: 20px;
        border-radius: 10px;
        flex: 2;
        min-width: 300px;
        margin: 10px;
        text-align: center;
    }

    .result-text {
        font-family: "Arial Black", sans-serif;
        font-size: 2em;
        color: #fff;
        font-weight: bold;
        text-shadow: 3px 3px 8px #ffcc00;
    }

    .result-number {
        font-size: 4em;
        background: linear-gradient(45deg, #ffcc00, #ff33cc, #66ccff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 3px 3px 10px #ffffff, 0 0 20px #ffcc00;
        animation: shimmer 2s infinite;
    }

    @keyframes shimmer {
        0% { text-shadow: 3px 3px 10px #ffffff, 0 0 20px #ffcc00; }
        50% { text-shadow: 3px 3px 15px #ff33cc, 0 0 25px #66ccff; }
        100% { text-shadow: 3px 3px 10px #ffffff, 0 0 20px #ffcc00; }
    }

    .comparison {
        margin-top: 10px;
        text-align: left;
    }

    .kame-result {
        width: 300px;
        margin-top: 20px;
        opacity: 0;
        transform: scale(0.5);
        animation: fadeInScale 1s forwards;
    }

    @keyframes fadeInScale {
        to {
            opacity: 1;
            transform: scale(1);
        }
    }

    .calc-button {
        background-color: #ff6600;
        color: white;
        font-size: 1.2em;
        padding: 10px 20px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        margin-top: 10px;
    }

    @media (max-width: 767px) {
        .container {
            flex-direction: column;
            align-items: center;
        }

        h1 {
            font-size: 3em;
        }

        .result-number {
            font-size: 2.5em;
        }
    }
    </style>
    </head><body>
    <h1>亀ちゃんとの運命</h1>
    <div class="container">
        <form method="post">
            <div class="description">
                ※自分の年齢と自己評価でランクを選んで「計算」ボタンを押してな。<br>
                どのくらい付き合える可能性があるか見てみよう！
            </div>
            年齢カテゴリ:
            <select name="age">{% for option in age_options %}
                <option value="{{ option }}" {% if option==input_data['age'] %}selected{% endif %}>{{ option }}</option>{% endfor %}
            </select><br>
            見た目ランク:
            <select name="appearance">{% for option in rank_options %}
                <option value="{{ option }}" {% if option==input_data['appearance'] %}selected{% endif %}>{{ option }}</option>{% endfor %}
            </select><br>
            性格ランク:
            <select name="personality">{% for option in rank_options %}
                <option value="{{ option }}" {% if option==input_data['personality'] %}selected{% endif %}>{{ option }}</option>{% endfor %}
            </select><br>
            経済力ランク:
            <select name="economic">{% for option in rank_options %}
                <option value="{{ option }}" {% if option==input_data['economic'] %}selected{% endif %}>{{ option }}</option>{% endfor %}
            </select><br>
            ファッションランク:
            <select name="fashion">{% for option in rank_options %}
                <option value="{{ option }}" {% if option==input_data['fashion'] %}selected{% endif %}>{{ option }}</option>{% endfor %}
            </select><br><br>
            <button class="calc-button" type="submit">計算</button><br><br>
            <h3>A〜Eの定義</h3>
            <ul>{% for rank, meaning in ae_definitions.items() %}
                <li><strong>{{rank}}</strong>: {{meaning}}</li>{% endfor %}
            </ul>
        </form>

        <div class="result-area">
            <div class="result-text">亀ちゃんと付き合える可能性</div>
            <div class="result-number">{{ total_prob_display }}%</div>
            <div class="comparison">{{ comparison_text|safe }}</div>
            {% if kame_image %}
                <img src="{{ kame_image }}" alt="亀ちゃん" class="kame-result">
            {% endif %}
        </div>
    </div>
    </body></html>
    """, total_prob_display=total_prob_display, comparison_text=comparison_text, ae_definitions=ae_definitions,
       input_data=input_data, age_options=age_options, rank_options=rank_options, kame_image=kame_image)

if __name__ == "__main__":
    app.run(debug=True)
