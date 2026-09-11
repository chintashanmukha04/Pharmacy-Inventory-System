from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def create_database():
    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            manufacturer TEXT,
            batch_number TEXT,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            expiry_date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def home():
    conn = sqlite3.connect("pharmacy.db")
    total_medicines = conn.execute("SELECT COUNT(*) FROM medicines").fetchone()[0]
    low_stock = conn.execute("SELECT COUNT(*) FROM medicines WHERE quantity < 10").fetchone()[0]
    expired = conn.execute("SELECT COUNT(*) FROM medicines WHERE expiry_date < date('now')").fetchone()[0]
    conn.close()
    return render_template("index.html", total_medicines=total_medicines, low_stock=low_stock, expired=expired)

@app.route("/add", methods=["GET", "POST"])
def add_medicine():
    if request.method == "POST":
        name = request.form["name"]
        category = request.form["category"]
        manufacturer = request.form["manufacturer"]
        batch_number = request.form["batch_number"]
        quantity = request.form["quantity"]
        price = request.form["price"]
        expiry_date = request.form["expiry_date"]
        conn = sqlite3.connect("pharmacy.db")
        conn.execute("""
            INSERT INTO medicines
            (name, category, manufacturer, batch_number, quantity, price, expiry_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, category, manufacturer, batch_number, quantity, price, expiry_date))
        conn.commit()
        conn.close()
        return redirect("/medicines")
    return render_template("add_medicine.html")

@app.route("/medicines")
def medicines():
    conn = sqlite3.connect("pharmacy.db")
    conn.row_factory = sqlite3.Row
    medicines = conn.execute("SELECT * FROM medicines").fetchall()
    conn.close()
    return render_template("medicines.html", medicines=medicines)

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_medicine(id):
    conn = sqlite3.connect("pharmacy.db")
    conn.row_factory = sqlite3.Row
    medicine = conn.execute("SELECT * FROM medicines WHERE id = ?", (id,)).fetchone()
    if request.method == "POST":
        name = request.form["name"]
        category = request.form["category"]
        manufacturer = request.form["manufacturer"]
        batch_number = request.form["batch_number"]
        quantity = request.form["quantity"]
        price = request.form["price"]
        expiry_date = request.form["expiry_date"]
        conn.execute("""
            UPDATE medicines
            SET name = ?, category = ?, manufacturer = ?, batch_number = ?,
                quantity = ?, price = ?, expiry_date = ?
            WHERE id = ?
        """, (name, category, manufacturer, batch_number, quantity, price, expiry_date, id))
        conn.commit()
        conn.close()
        return redirect("/medicines")
    conn.close()
    return render_template("edit_medicine.html", medicine=medicine)

@app.route("/delete/<int:id>")
def delete_medicine(id):
    conn = sqlite3.connect("pharmacy.db")
    conn.execute("DELETE FROM medicines WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/medicines")

@app.route("/search")
def search():
    query = request.args.get("query", "")
    conn = sqlite3.connect("pharmacy.db")
    conn.row_factory = sqlite3.Row
    medicines = conn.execute("""
        SELECT * FROM medicines
        WHERE name LIKE ?
    """, ("%" + query + "%",)).fetchall()
    conn.close()
    return render_template("medicines.html", medicines=medicines)

@app.route("/low-stock")
def low_stock():
    conn = sqlite3.connect("pharmacy.db")
    conn.row_factory = sqlite3.Row
    medicines = conn.execute("""
        SELECT * FROM medicines
        WHERE quantity < 10
    """).fetchall()
    conn.close()
    return render_template("low_stock.html", medicines=medicines)

@app.route("/expired")
def expired_medicines():
    conn = sqlite3.connect("pharmacy.db")
    conn.row_factory = sqlite3.Row
    medicines = conn.execute("""
        SELECT * FROM medicines
        WHERE expiry_date < date('now')
    """).fetchall()
    conn.close()
    return render_template("expired.html", medicines=medicines)

if __name__ == "__main__":
    create_database()
    app.run()
    