from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
    get_flashed_messages,
)
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

from trading_app.utils import (
    add_trade_to_db,
    update_trade_columns,
    get_from_table,
    clear_trades,
)

from trading_app.trading_bot import (
    mac_strategy_tradingbot,
    bollinger_bands_strategy_tradingbot,
    rsi_strategy_tradingbot,
)

from datetime import datetime

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
        # return redirect(url_for("home.index"))
    return render_template("quidbot/stock_graph.html")


# flash function is used to display a message to the user.
def flash_error(messge):
    flash(messge)


@bp.route("/predictions", methods=["GET", "POST"])
def prediction_route(flash_message=None):
    db = get_db()

    setting = db.execute(
        "SELECT brain, api FROM api_key WHERE user_id = ?", (g.user["id"],)
    ).fetchone()

    url = request.url
    api = None
    brain = None

    if setting:
        brain = setting[0]
        api = setting[1]

    if not api:
        flash("Please set your API key in settings")

    if not brain:
        flash("Please set your model in settings")

    if request.method == "POST":
        prediction = None
        stocks = request.form["stocks"]
        stocks = stocks.split(",")
        for i, stock in enumerate(stocks):
            stocks[i] = stock[:-1]
        # Get setting from db
        db = get_db()

        all_data = gather_data(stocks)

        if brain == "GPT-4":
            print("GPT-4", api)
            openai_api_key = api
            prediction = predict_up_or_down_openai(stocks, all_data, openai_api_key)

        elif brain == "Claude":
            print("Claude")
            claude_api_key = api
            prediction = predict_up_or_down_claude(stocks, all_data, api)

        return jsonify(prediction)

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
    if setting:
        return jsonify({"setting": {"brain": setting[0], "api": setting[1]}})
    else:
        return jsonify({"setting": {"brain": "", "api": ""}})


@bp.route("/trading")
def trading():
    return render_template("quidbot/trading/trading.html")


@bp.route("/trading/historical_data", methods=["GET", "POST"])
def historical_data():
    if request.method == "POST":
        stock = request.form["stock"]
        start_date = request.form["start-date"]
        end_date = request.form["end-date"]
        strategy = request.form["strategy"]
        balance = request.form["balance"]

        trade = {
            "stock": stock,
            "start_date": start_date,
            "end_date": end_date,
            "strategy": strategy,
            "cash_balance": balance,
            "user_id": g.user["id"],
            "time_started": datetime.now(),
            "time_ended": None,
            "profit": 0,
            "status": "ongoing",
            "type": "historical",
            "history": None,
            "stock_balance": 0,
            "portfolio_value": balance,
        }

        trade_db = add_trade_to_db(trade)

        if strategy == "MAC":
            trading_bot = mac_strategy_tradingbot.MACStrategyTradingBot(
                trade["stock"],
                float(trade["cash_balance"]),
                1,
                50,
                200,
                start_date,
                end_date,
            )
            trades = trading_bot.run()

        update_trade_columns(
            trade_db,
            {
                "time_ended": datetime.now(),
                "status": "completed",
                "history": str(trades["history"]),
                "cash_balance": trades["cash"],
                "stock_balance": trades["stock_balance"],
                "profit": float(trades["portfolio_value"])
                - float(trade["portfolio_value"]),
                "portfolio_value": trades["portfolio_value"],
            },
        )

        return render_template("quidbot/trading/historical_data.html")

    return render_template("quidbot/trading/historical_data.html")


@bp.route("/get_trades")
def get_trades_route():
    try:
        trades = get_from_table("trade", {"user_id": g.user["id"]})
        return jsonify(trades)
    except Exception as e:
        print("Error getting trades")
        flash("Error getting trades")
        return jsonify({"error": str(e)})


@bp.route("/clear_trades", methods=["DELETE"])
def clear_trades_route():
    try:
        clear_trades(g.user["id"])
        return jsonify({"message": "Trades cleared"})
    except Exception as e:
        print("Error clearing trades")
        flash("Error clearing trades")
        return jsonify({"error": str(e)})


@bp.route("/delete_trade", methods=["DELETE"])
def delete_trade_route():
    try:
        trade_id = request.args.get("trade_id")
        db = get_db()
        db.execute("DELETE FROM trade WHERE id = ?", (trade_id,))
        db.commit()
        return jsonify({"message": "Trade deleted"})
    except Exception as e:
        print("Error deleting trade")
        flash("Error deleting trade")
        return jsonify({"error": str(e)})
