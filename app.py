import os

from cs50 import SQL
from flask import Flask, session, request, jsonify, flash, redirect, render_template
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, apology

import datetime

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///textil.db")



@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    
    return response

@app.route("/")
@login_required
def index():
    # Fetch textile releases data from the database
    releases = db.execute("SELECT * FROM textile_releases")

    return render_template("index.html", releases=releases)
    
# Route to handle status updates
@app.route("/update_status", methods=["POST"])
def update_status():
    # Extract release ID and status from the POST request
    release_id = request.form.get("release_id")
    status = request.form.get("status")

    # Update status in the database
    db.execute("UPDATE textile_releases SET status = ? WHERE id = ?", status, release_id)

    # Optionally provide a response
    return "Status updated successfully"

@app.route("/delete_release", methods=["POST"])
@login_required
def delete_release():
    if request.method == "POST":
        release_id = request.form.get("release_id")

        # Check if release_id is provided
        if not release_id:
            return "Release ID is missing", 400

        try:
            # Delete related records from the color_quantities table
            db.execute("DELETE FROM color_quantities WHERE textile_release_id = ?", release_id)

            # Delete the release from the textile_releases table
            db.execute("DELETE FROM textile_releases WHERE id = ?", release_id)

            

            return (redirect("/"))
        except Exception as e:
            # Log the error for debugging
            app.logger.error(f"Error deleting release: {e}")
            # Return a generic error message to the client
            return "An error occurred while deleting the release", 500
    else:
        return "Invalid request method", 405

    
@app.route("/colors", methods=["GET", "POST"])
@login_required
def colors():
    # Fetch color quantities data from the database
    color_quantities = db.execute("SELECT textile_release_id, color, size, total_quantity FROM color_quantities")

    # Organize data into a nested dictionary
    color_quantity_dict = {}
    for row in color_quantities:
        textile_release_id = row['textile_release_id']
        color = row['color']
        size = row['size']
        quantity = row['total_quantity']
        if textile_release_id not in color_quantity_dict:
            color_quantity_dict[textile_release_id] = {}
        if color not in color_quantity_dict[textile_release_id]:
            color_quantity_dict[textile_release_id][color] = {}
        color_quantity_dict[textile_release_id][color][size] = quantity

    return render_template("colors.html", color_quantities=color_quantity_dict)

    


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted


        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            flash("You must insert username")
            return (redirect("/login"))

        # Ensure password was submitted
        elif not password:
            flash("You must insert password")
            return (redirect("/login"))
        

        if not username or not password:
            flash("You must insert password AND username")
            return (redirect("/login"))

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            flash("invalid username and/or password")
            return (redirect("/login"))

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":


        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            flash("You must insert username")
            return (redirect("/register"))

        # Ensure password was submitted
        elif not password:
            flash("You must insert password")
            return (redirect("/register"))

        elif password != confirmation:
            flash("password does not match")
            return (redirect("/register"))
            
        

        elif not confirmation:
            flash("no matching password")
            return (redirect("/register"))

        hashed_password = generate_password_hash(request.form.get("password"))

        result = db.execute(
            "INSERT INTO users( username, hash) VALUES (?, ?)",
            request.form.get("username"),
            hashed_password
        )

        if not result:
            flash("Username already in existence")
            return redirect("/register")

        # Log the user in automatically after registration
        session["user_id"] = result

        # Flash a success message
        flash("Registered successfully!")

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    # Clear session
    session.clear()

    # redirect
    return redirect("/")
    
@app.route("/release", methods=["GET", "POST"])
@login_required
def release():
    if request.method == "POST":
        # Extract form data
        fecha = request.form.get("fecha")
        planta_key = request.form.get("clave_planta")
        ciudad = request.form.get("ciudad")
        municipio = request.form.get("municipio")
        estado = request.form.get("estado")
        codigo_postal = request.form.get("codigo_postal")
        telefono_contacto = request.form.get("telefono_contacto")
        nombre_contacto = request.form.get("nombre_contacto")
        prendas_solicitadas = request.form.get("total_prendas")

        cantidad = request.form.getlist("cantidad")
        color = request.form.getlist("color")
        talla = request.form.getlist("talla")

       # Ensure all required fields are provided
        if not (fecha and planta_key and ciudad and municipio and estado and codigo_postal and telefono_contacto and nombre_contacto and prendas_solicitadas and cantidad and color and talla):
            flash("Llene todos los datos requeridos")
            return redirect("/release")
        
    

        # Insert data into the 'textile_releases' table
        db.execute("INSERT INTO textile_releases (fecha, planta_key, ciudad, municipio_estado, codigo_postal, telefono_contacto, nombre_contacto, prendas_solicitadas, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   fecha, planta_key, ciudad, f"{municipio}, {estado}", codigo_postal, telefono_contacto, nombre_contacto, prendas_solicitadas, 'in progress')

        

        new_release_id = db.execute("SELECT id FROM textile_releases ORDER BY id DESC LIMIT 1")
        new_release_id2 = new_release_id[0]['id']

        for c, t, q in zip(color, talla, cantidad):
            db.execute("INSERT INTO color_quantities (textile_release_id, color, size, total_quantity) VALUES (?, ?, ?, ?)",
                       new_release_id2, c, t, q)
        # Insert the data into the color_quantities table
        #db.execute("INSERT INTO color_quantities (textile_release_id, color, size, total_quantity) VALUES (?, ?, ?, ?)",
                   #new_release_id2, color, talla, cantidad)

        # Redirect to a success page or wherever you want after insertion
        return redirect("/")
    else:
        # For GET requests, render the release.html template
        return render_template("release.html")

@app.route("/handle-alert", methods=["POST"])
def handle_alert():
    message = request.form.get("message")
    flash(message)
    return "Alert message sent to backend"

@app.route("/search_date")
@login_required
# only render template
def search_date():
    today = datetime.datetime.now()
    return render_template("search_date.html", today=today)



@app.route("/search_date/search")
def search_date2():
    # Get the query parameter from the request
    q = request.args.get("q")


    # Check if the query parameter is present
    if q:
        try:
            # Convert the query parameter to a datetime object
            year, month, day = map(int, q.split('-'))
            query_date = datetime.datetime(year, month, day)

            # Query the database for the textile release data
            results = db.execute("SELECT * FROM textile_releases WHERE fecha = ?", q)

            # Return the results as JSON
            return jsonify(results)
        except ValueError:
            # Return an error message if the date format is incorrect
            return jsonify({"error": "Invalid date format. Please use YYYY-MM-DD."}), 400
    else:
        # Return an empty response if no query parameter is provided
        return jsonify([])
    

@app.route("/search_name")
# only render template
@login_required
def search_name():
    return render_template("search_name.html")


@app.route("/search_name/search")
def search_name2():
    # When input, return query as json so ir can be displayed dinamically
    q = request.args.get("q")
    if q:
        results = db.execute("SELECT * FROM textile_releases WHERE nombre_contacto LIKE ?", f"%{q}%")
    else:
        results = []
    return jsonify(results)

@app.route("/search_id")
@login_required
def search_id():
    return render_template("search_id.html")

@app.route("/search_id/search")
def search_id2():
    q = request.args.get("q")
    if q:
        results = db.execute("SELECT * FROM textile_releases WHERE id LIKE ?",  f"%{q}%")
    else:
        results = []
    return jsonify(results)

@app.route("/search_colors")
@login_required
def search_colors():
    return render_template("search_colors.html")

@app.route("/search_colors/search")
def search_colors2():
    q = request.args.get("q")
    if q:
        results = db.execute("SELECT * FROM color_quantities WHERE textile_release_id LIKE ?", f"%{q}%")
    else:
        results = []
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)