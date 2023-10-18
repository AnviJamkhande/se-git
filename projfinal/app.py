from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import matplotlib.pyplot as plt
import hashlib
import os

# from chart_data import get_company_graph_data
app = Flask(__name__)
app.static_folder = 'static'
# Generate a random secret key
secret_key = os.urandom(24)
app.secret_key = secret_key


# Create a SQLite database for storing block names
conn = sqlite3.connect('blocks.db')
cursor = conn.cursor()

# Create the table for block names if it doesn't exist
cursor.execute('CREATE TABLE IF NOT EXISTS Blocks (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE)')

# Fetching block names from database
cursor.execute('SELECT name FROM Blocks')
rows = cursor.fetchall()
block_names = [row[0] for row in rows]

conn.close()


def connect_to_database(block_name):
    # Replace spaces with underscores for database name
    db_name = block_name.replace(' ', '_')

    conn = sqlite3.connect(f'{db_name}.db')
    cursor = conn.cursor()

    # Create the table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name_Of_Company TEXT,
            Type TEXT,
            Website TEXT,
            Location TEXT,
            Money_sponsored REAL,
            Contact_email TEXT,
            Comments TEXT
        )
    ''')

    conn.commit()
    conn.close()

def add_block_to_database(block_name):
    conn = sqlite3.connect('blocks.db')
    cursor = conn.cursor()

    # Insert the block name into the database
    cursor.execute('INSERT INTO Blocks (name) VALUES (?)', (block_name,))

    conn.commit()
    conn.close()

def fetch_block_names():
    conn = sqlite3.connect('blocks.db')
    cursor = conn.cursor()

    cursor.execute('SELECT name FROM Blocks')
    rows = cursor.fetchall()
    block_names = [row[0] for row in rows]

    conn.close()

    return block_names

# Create databases and tables for each block
for block_name in block_names:
    connect_to_database(block_name)

# Create the table for block names if it doesn't exist
conn = sqlite3.connect('blocks.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS Blocks (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE)')
conn.commit()
conn.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        new_block_name = request.form.get('new_block_name')
        if new_block_name:
            # Check if the block already exists
            if new_block_name in block_names:
                error_message = f"The block '{new_block_name}' already exists."
                return render_template('index.html', block_names=block_names, error_message=error_message)

            # Connect to the database and create a new block
            connect_to_database(new_block_name)
            add_block_to_database(new_block_name)
            block_names.append(new_block_name)
    return render_template('index.html', block_names=block_names)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Hardcoded username and password for testing
        if username == 'Anvi Jamkhande' and password == 'hello world':
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            error_message = 'Invalid username or password'
            return render_template('login.html', error_message=error_message)

    return render_template('login.html')



@app.route('/block/<block_name>')
def block(block_name):
    # Connect to the database for the clicked block
    db_name = block_name.replace(' ', '_')
    conn = sqlite3.connect(f'{db_name}.db')
    cursor = conn.cursor()
    
    # Fetch data from the table and sort by company name
    cursor.execute('SELECT * FROM Companies ORDER BY Name_Of_Company')
    data = cursor.fetchall()

    conn.close()

    return render_template('block.html', block_name=block_name, data=data)

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/Crif_India')
def Crif_India():
    return render_template('Crif_India.html')

@app.route('/block/<block_name>/add_company', methods=['GET', 'POST'])
def add_company(block_name):
# checking if logged in
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        company_name = request.form.get('company_name')
        company_type = request.form.get('company_type')
        website = request.form.get('website')
        location = request.form.get('location')
        money_sponsored = request.form.get('money_sponsored')
        contact_email = request.form.get('contact_email')
        comments = request.form.get('comments')

        db_name = block_name.replace(' ', '_')
        conn = sqlite3.connect(f'{db_name}.db')
        cursor = conn.cursor()

        # Insert the new company into the table
        cursor.execute('INSERT INTO Companies (Name_Of_Company, Type, Website, Location, Money_sponsored, Contact_email, Comments) VALUES (?, ?, ?, ?, ?, ?, ?)', (company_name, company_type, website, location, money_sponsored, contact_email, comments))

        conn.commit()
        conn.close()

        return redirect(url_for('block', block_name=block_name))

    return render_template('add_company.html', block_name=block_name)

@app.route('/block/<block_name>/view_company/<int:company_id>', methods=['GET'])
def view_company(block_name, company_id):
    # Connect to the database for the clicked block
    db_name = block_name.replace(' ', '_')
    conn = sqlite3.connect(f'{db_name}.db')
    cursor = conn.cursor()

    # Fetch data from the table for the selected company
    cursor.execute('SELECT * FROM Companies WHERE id = ?', (company_id,))
    data = cursor.fetchone()

    graph_data = data[-1]
    conn.close()

    return render_template('view_company.html', block_name=block_name, data=data)


@app.route('/block/<block_name>/edit_company/<int:company_id>', methods=['GET', 'POST'])
def edit_company(block_name, company_id):
    # Connect to the database for the clicked block
    db_name = block_name.replace(' ', '_')
    conn = sqlite3.connect(f'{db_name}.db')
    cursor = conn.cursor()

    # Fetch data from the table for the selected company
    cursor.execute('SELECT * FROM Companies WHERE id = ?', (company_id,))
    data = cursor.fetchone()

    if request.method == 'POST':
        company_name = request.form.get('company_name')
        company_type = request.form.get('company_type')
        website = request.form.get('website')
        location = request.form.get('location')
        money_sponsored = request.form.get('money_sponsored')
        contact_email = request.form.get('contact_email')
        comments = request.form.get('comments')


        # Update the company in the table
        cursor.execute('UPDATE Companies SET Name_Of_Company = ?, Type = ?, Website = ?, Location = ?, Money_sponsored = ?, Contact_email = ?, Comments = ? WHERE id = ?', (company_name, company_type, website, location, money_sponsored, contact_email, comments, company_id))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        return redirect(url_for('view_company', block_name=block_name, company_id=company_id))

    # Close the connection
    conn.close()

    return render_template('edit_company.html', block_name=block_name, company_id=company_id, data=data)


if __name__ == '__main__':
    app.run(debug=True)
