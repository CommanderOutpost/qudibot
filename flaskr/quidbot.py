from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

from flaskr.stock_market import get_stock_data, show_stock_graph

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


@bp.route("/stock_graph", methods=["GET", "POST"])
def stock_graph():
    if request.method == "POST":
        stock = request.form["stock"]
        period = request.form["period"]
        interval = request.form["interval"]
        df = get_stock_data(stock, period, interval)
        show_stock_graph(df, stock)
        return redirect(url_for("home.index"))
    return render_template("quidbot/stock_graph.html")
