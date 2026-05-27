from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('bookkeeping.db')
    return conn

@app.route('/api/transactions', methods=['GET', 'POST'])
def transactions():
    conn = get_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (id INTEGER PRIMARY KEY, date TEXT, description TEXT, amount REAL)''')
    if request.method == 'POST':
        data = request.json
        c.execute("INSERT INTO transactions (date, description, amount) VALUES (?, ?, ?)",
                  (data["date"], data["description"], data["amount"]))
        conn.commit()
        return jsonify({"status": "ok"}), 201
    else:
        c.execute("SELECT * FROM transactions ORDER BY date DESC")
        transactions = [
            {"id": row[0], "date": row[1], "description": row[2], "amount": row[3]}
            for row in c.fetchall()
        ]
        return jsonify(transactions)

if __name__ == "__main__":
    app.run(debug=True)
