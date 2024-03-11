from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from trading_app.auth import login_required
from trading_app.db import get_db

from trading_app.stock_market import get_stock_data
from flask import jsonify

from trading_app.gather_all_data import gather_data

from trading_app.chat_ai import (
    predict_up_or_down_openai,
    predict_up_or_down_claude,
    predict_up_or_down_groq,
)

bp = Blueprint("home", __name__)


@bp.route("/")
def index():
    db = get_db()
    if g.user:
        return render_template("quidbot/index.html", user=g.user)
    else:
        return render_template("quidbot/landingPage.html")


@bp.route("/view_stock", methods=["GET", "POST"])
def stock_graph():
    if request.method == "POST":
        stock = request.form["stock"]
        period = request.form["period"]
        interval = request.form["interval"]
        df = get_stock_data(stock, period, interval)
        return redirect(url_for("home.index"))
    return render_template("quidbot/stock_graph.html")


@bp.route("/predictions", methods=["GET", "POST"])
def prediction():
    if request.method == "POST":
        stocks = request.form["stocks"]
        stocks = stocks.split(",")
        for i, stock in enumerate(stocks):
            stocks[i] = stock[:-1]
        # Get setting from db
        db = get_db()
        setting = db.execute(
            "SELECT brain, api FROM api_key WHERE user_id = ?", (g.user["id"],)
        ).fetchone()

        if setting:
            brain = setting[0]
            api = setting[1]

        if not api:
            flash("Please set your API key in settings")

        if not brain:
            flash("Please set your model in settings")

        all_data = gather_data(stocks)

        if brain == "GPT-4":
            openai_api_key = api
            prediction = predict_up_or_down_openai(stocks, all_data, api)

        elif brain == "Claude":
            claude_api_key = api
            prediction = predict_up_or_down_claude(stocks, all_data, api)
            
        prediction = eval(prediction)

        return jsonify({"predictions": prediction})
    return render_template("quidbot/prediction.html")


@bp.route("/get_stock_data")
def get_stock_data_route():
    try:
        stock = request.args.get("stock")
        period = request.args.get("period")
        interval = request.args.get("interval")
        df = get_stock_data(stock, period, interval)
        data = df.reset_index().to_dict("list")
        return jsonify(data)
    except Exception as e:
        print("Error getting stock data")
        flash("Error getting stock data")
        return jsonify({"error": str(e)})


@bp.route("/setting", methods=["GET", "POST"])
def setting():
    prev_url = request.referrer
    g.prev_url = prev_url
    db = get_db()
    if request.method == "POST":
        model = request.form["model"]
        api = request.form["api"]

        # Check if model and api are not empty and trimmed
        if not model.strip() or not api.strip():
            flash("Please fill in all fields")
            return redirect(prev_url)
        
        # Check if setting already exists
        setting = db.execute(
            "SELECT * FROM api_key WHERE user_id = ?", (g.user["id"],)
        ).fetchone()
        print(setting)
        if setting:
            print(
                f"UPDATE query: UPDATE api_key SET brain = '{model}', api = '{api}' WHERE user_id = {g.user['id']}"
            )
            db.execute(
                "UPDATE api_key SET brain = ?, api = ? WHERE user_id = ?",
                (model, api, g.user["id"]),
            )
        else:
            print(
                f"INSERT query: INSERT INTO api_key (brain, user_id, api) VALUES ('{model}', {g.user['id']}, '{api}')"
            )
            db.execute(
                "INSERT INTO api_key (brain, user_id, api) VALUES (?, ?, ?)",
                (model, g.user["id"], api),
            )

        db.commit()

        return redirect(prev_url)


@bp.route("/get_setting")
def get_setting():
    db = get_db()
    setting = db.execute(
        "SELECT brain, api FROM api_key WHERE user_id = ?", (g.user["id"],)
    ).fetchone()
    print(setting)
    if setting:
        return jsonify({"setting": {"brain": setting[0], "api": setting[1]}})
    else:
        return jsonify({"setting": {"brain": "", "api": ""}})
