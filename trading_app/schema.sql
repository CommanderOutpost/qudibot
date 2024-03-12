DROP TABLE IF EXISTS user;

DROP TABLE IF EXISTS post;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE api_key (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brain TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    api TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE prediction (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    stock TEXT NOT NULL,
    prediction TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id)
);

-- Create a table called trade with the following columns. stock, start-date, end-date, strategy, balance, user_id, time_started, time_ended, profit, status, type
CREATE TABLE trade (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stock TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    strategy TEXT NOT NULL,
    cash_balance REAL NOT NULL,
    user_id INTEGER NOT NULL,
    time_started TEXT NOT NULL,
    time_ended TEXT,
    profit REAL NOT NULL,
    status TEXT NOT NULL,
    type TEXT NOT NULL,
    history TEXT,
    stock_balance REAL NOT NULL,
    portfolio_value REAL NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id)
);
