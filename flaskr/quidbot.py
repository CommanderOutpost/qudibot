from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

from flaskr.stock_market import get_stock_data
from flask import jsonify

from flaskr.gather_all_data import gather_data

from flaskr.chat_ai import predict_up_or_down_openai, predict_up_or_down_claude

bp = Blueprint("home", __name__)


@bp.route("/")
def index():
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()
    if g.user:
        return render_template("quidbot/index.html", posts=posts, user=g.user)
    else:
        return render_template("quidbot/landingPage.html", posts=posts)


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
        print(stocks)
        openai_api_key = "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"
        all_data = gather_data(stocks)
        prediction = predict_up_or_down_claude(stocks, all_data)
        # Turn json to dictionary
        prediction = eval(prediction)
        return jsonify({"predictions": prediction})
    return render_template("quidbot/prediction.html")


@bp.route("/get_stock_data")
def get_stock_data_route():
    stock = request.args.get("stock")
    period = request.args.get("period")
    interval = request.args.get("interval")
    df = get_stock_data(stock, period, interval)
    data = df.reset_index().to_dict("list")
    return jsonify(data)
