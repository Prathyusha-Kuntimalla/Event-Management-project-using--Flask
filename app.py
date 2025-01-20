from flask import Flask, render_template, request, redirect, url_for, flash
from db_config import get_db_connection

app = Flask(__name__)
app.secret_key = "your_secret_key"  # For flashing messages

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM events ORDER BY date ASC")
    events = cursor.fetchall()
    conn.close()
    return render_template('index.html', events=events)

@app.route('/add', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        location = request.form['location']
        description = request.form['description']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO events (name, date, location, description) VALUES (%s, %s, %s, %s)",
            (name, date, location, description)
        )
        conn.commit()
        conn.close()
        flash("Event added successfully!")
        return redirect(url_for('index'))
    return render_template('add_event.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_event(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM events WHERE id = %s", (id,))
    event = cursor.fetchone()
    conn.close()

    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        location = request.form['location']
        description = request.form['description']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE events SET name = %s, date = %s, location = %s, description = %s WHERE id = %s",
            (name, date, location, description, id)
        )
        conn.commit()
        conn.close()
        flash("Event updated successfully!")
        return redirect(url_for('index'))
    return render_template('edit_event.html', event=event)

@app.route('/delete/<int:id>')
def delete_event(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    flash("Event deleted successfully!")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
