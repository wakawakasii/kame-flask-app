from flask import Flask, render_template_string, request, url_for, session
import random, os

app = Flask(__name__)
app.secret_key = "kame_secret_key"

@app.route("/", methods=["GET", "POST"])
def index():
    total_prob, display_prob, comparison_text = 0, "0", ""
    ae_defs = {"A": "最高ランク", "B": "良い", "C": "普通", "D": "やや微妙", "E": "低評価"}
    age_opts, rank_opts = ["10代", "20代前半", "20代後半", "30代前半", "30代後半", "40代以上"], ["A","B","C","D","E"]
    inputs, kame_img, taco_msg = {"age": "", "appearance": "", "personality": "", "economic": "", "fashion": ""}, "", ""

    if request.method == "POST":
        for key in inputs.keys():
            inputs[key] = request.form.get(key, "").upper() or "C"
        rv = {"A": 0.05, "B": 0.04, "C": 0.03, "D": 0.02, "E": 0.01}
        ab = {"10代": 0.5, "20代前半": 0.8, "20代後半": 1.0, "30代前半": 1.2, "30代後半": 1.0, "40代以上": 0.9}
        base = (rv.get(inputs["appearance"], 0) * rv.get(inputs["personality"], 0) * rv.get(inputs["economic"], 0) * rv.get(inputs["fashion"], 0)) * 100
        total_prob = base * ab.get(inputs["age"], 1)
        display_prob = f"{total_prob:.10f}".rstrip('0').rstrip('.')

        comp = [
            (0.001, "流れ星に願いが叶う（約0.001%）"),
            (0.00013333, "隕石激突（約0.00013%）"),
            (0.00001, "ジャンボ宝くじ1等当選（約0.00001%）"),
            (0.00000971, "ロト7当選（約0.0000097%）"),
            (0.0001, "ハリウッド俳優と出会う（約0.0001%）"),
            (0.005, "UFO目撃（約0.005%）"),
            (0.2, "スパイシータコス無料券当選（約0.2%）"),
            (1.0, "宝くじ5等（約1%）"),
            (0.01, "交通事故（約0.01%）"),
            (0.000009, "飛行機事故（約0.000009%）"),
            (10.0, "恋愛成就（理想型）（約10%）"),
            (50.0, "結婚できる確率（約50%）"),
            (0.00001, "芸能人と付き合える確率（約0.00001%）"),
            (15.0, "バレンタインでチョコ貰う確率（約15%）")
        ]
        comp_sorted = sorted(comp, key=lambda c: abs(total_prob - c[0]), reverse=True)[:4]
        comparison_text = "<ul>"
        for c in comp_sorted:
            ratio_value = total_prob / c[0] if c[0] else float('inf')
            relation = "高い" if ratio_value >= 1 else "低い"
            ratio = f"{ratio_value:.6f}" if c[0] else "∞"
            comparison_text += f"<li>{c[1]}より約{ratio}倍{relation}</li>"
        comparison_text += "</ul>"

        img_dir = os.path.join(app.root_path, "static")
        imgs = [f for f in os.listdir(img_dir) if f.startswith("kame_face")]
        kame_img = url_for('static', filename=random.choice(imgs)) if imgs else url_for('static', filename="default_kame.jpg")

        tacos = [
            "今日の恋愛はタコス並みにスパイシー！大胆に攻めろ🔥",
            "サルサソースの辛さのように、情熱をぶつけていけ💘",
            "トルティーヤで包むように、相手を優しく包み込め🌯",
            "いつでもどこでもタコスが似合う！まだまだ亀ちゃんには届かない🐢",
            "俺に恋するのやめろって…でもやっぱり気になるやろ？😉",
            "サルサソースの酸味みたいに、恋も時には刺激が必要や🔥",
            "タコスに負けるな！恋も人生も自分次第やで💪",
            "トルティーヤみたいに柔軟に、相手に合わせるのがカギやな🔑",
            "亀ちゃん、タコスは持ってるけど、恋は持ってない！？💫",
            "恋もサルサソースのように、一度かけたら止められへん🔥",
            "トルティーヤで包み込めば、誰でも恋に落ちる不思議🐢",
            "恋のスパイスはタコスに学べ！刺激と甘さのバランスや😉",
            "サルサソースだけじゃなく、心もホットにいこうや🔥",
            "トルティーヤのように層を重ね、相手の本音を見抜け👀",
            "俺に恋するのは勝手やけど、亀ちゃんには敵わんで💘"
        ]
        prev_msg = session.get("prev_msg", "")
        new_msg = random.choice([t for t in tacos if t != prev_msg] or tacos)
        taco_msg = new_msg
        session["prev_msg"] = new_msg

    return render_template_string("""
    <html><head>
    <style>
    body {background:url('{{ url_for('static', filename='midori_kame_bg.jpg') }}') no-repeat center/cover; font-family:"Comic Sans MS",sans-serif; color:white; padding:20px;}
    h1 {font-size:5em;text-align:center;background:linear-gradient(45deg,#f9d423,#ff4e50);-webkit-background-clip:text;-webkit-text-fill-color:transparent;text-shadow:0 0 30px #fff;}
    .container {display:flex;flex-wrap:wrap;justify-content:space-between;}
    .form-section {flex:1;min-width:250px;max-width:400px;background:rgba(0,0,0,0.6);padding:20px;border-radius:10px;margin:10px;}
    .result-section {flex:2;min-width:300px;background:rgba(0,0,0,0.6);padding:20px;border-radius:10px;margin:10px;text-align:center;}
    .result-num {font-size:6em;background:linear-gradient(45deg,#ffcc00,#ff33cc,#66ccff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;text-shadow:0 0 30px #fff,0 0 60px #ffcc00;animation:shimmer 2s infinite;}
    @keyframes shimmer {0%{text-shadow:0 0 30px #fff,0 0 60px #ffcc00;}50%{text-shadow:0 0 35px #ff33cc,0 0 65px #66ccff;}100%{text-shadow:0 0 30px #fff,0 0 60px #ffcc00;}}
    .compare {background:rgba(0,0,0,0.5);padding:10px;border-radius:10px;margin-top:10px;text-align:left;}
    .kame-pic {width:300px;margin-top:10px;animation:fadeInScale 1s;}
    @keyframes fadeInScale {from{opacity:0;transform:scale(0.5);}to{opacity:1;transform:scale(1);}}
    .taco-msg {font-size:2em;text-align:center;color:#ffcc00;text-shadow:0 0 20px #ff33cc;animation:slideIn 3s infinite alternate;margin-top:30px;}
    @keyframes slideIn {from{transform:translateX(-30px);}to{transform:translateX(30px);}}
    .description {color:#ffff99;}
    .ae-defs {color:#ffcc66;}
    button[type="submit"] {
        background: linear-gradient(45deg, #ff6f61, #ffcc33);
        border: none;
        color: white;
        font-size: 1.5em;
        padding: 15px 30px;
        border-radius: 10px;
        cursor: pointer;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
        position: relative;
    }
    button[type="submit"]::after {
        content: " 💖";
        font-size: 1.2em;
        position: absolute;
        right: 10px;
        top: 50%;
        transform: translateY(-50%);
    }
    button[type="submit"]:hover {
        background: linear-gradient(45deg, #ffcc33, #ff6f61);
        transform: scale(1.1);
        box-shadow: 0 6px 10px rgba(0,0,0,0.4);
    }
    @media (max-width: 767px) {.container{flex-direction:column;align-items:center;}.result-num{font-size:4em;}.form-section,.result-section{width:90%;}}
    </style></head><body>
    <h1>亀ちゃんとの運命</h1>
<audio id="bgm-player" autoplay loop>
  <source src="{{ url_for('static', filename='bgm.mp3') }}" type="audio/mpeg">
  お使いのブラウザではBGM再生に対応していません。
</audio>

<button id="bgm-toggle-btn">🔊 BGM停止</button>

<script>
  const bgmPlayer = document.getElementById('bgm-player');
  const bgmToggleBtn = document.getElementById('bgm-toggle-btn');

  bgmToggleBtn.addEventListener('click', function() {
    if (bgmPlayer.paused) {
      bgmPlayer.play();
      bgmToggleBtn.textContent = "🔊 BGM停止";
    } else {
      bgmPlayer.pause();
      bgmToggleBtn.textContent = "🔈 BGM再生";
    }
  });
</script>
    <div class="container">
    <div class="form-section">
    <p class="description">※自分の年齢と自己評価でランクを選んで「計算」ボタンを押してな。<br>どのくらい付き合える可能性があるか見てみよう！</p>
    <form method="post">
    年齢:<select name="age">{% for o in age_opts %}<option value="{{o}}" {%if o==inputs['age']%}selected{%endif%}>{{o}}</option>{%endfor%}</select><br>
    見た目:<select name="appearance">{% for o in rank_opts %}<option value="{{o}}" {%if o==inputs['appearance']%}selected{%endif%}>{{o}}</option>{%endfor%}</select><br>
    性格:<select name="personality">{% for o in rank_opts %}<option value="{{o}}" {%if o==inputs['personality']%}selected{%endif%}>{{o}}</option>{%endfor%}</select><br>
    経済力:<select name="economic">{% for o in rank_opts %}<option value="{{o}}" {%if o==inputs['economic']%}selected{%endif%}>{{o}}</option>{%endfor%}</select><br>
    ファッション:<select name="fashion">{% for o in rank_opts %}<option value="{{o}}" {%if o==inputs['fashion']%}selected{%endif%}>{{o}}</option>{%endfor%}</select><br><br>
    <button type="submit">計算</button></form>
    <h3 class="ae-defs">A～Eの定義</h3><ul>{% for k,v in ae_defs.items() %}<li><strong>{{k}}</strong>:{{v}}</li>{%endfor%}</ul>
    </div>
    <div class="result-section">
    <div>亀ちゃんと付き合える可能性</div>
    <div class="result-num">{{display_prob}}%</div>
    {% if kame_img %}<img src="{{kame_img}}" class="kame-pic">{%endif%}
    <div class="compare">{{comparison_text|safe}}</div>
    </div>
    </div>
    <div class="taco-msg">🌮 {{taco_msg}} 🌮</div>
    </body></html>
    """, display_prob=display_prob, comparison_text=comparison_text, inputs=inputs, age_opts=age_opts, rank_opts=rank_opts, kame_img=kame_img, ae_defs=ae_defs, taco_msg=taco_msg)

if __name__ == "__main__":
    app.run(debug=True)
