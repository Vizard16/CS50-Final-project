import os

from cs50 import SQL
from flask import Flask, session, request, flash, redirect, render_template
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, apology

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
    '''
    # Fetch color quantities data from the database
    color_quantities = db.execute("SELECT textile_release_id, color, size, total_quantity FROM color_quantities")

    # Organize data into a nested dictionary
    color_quantity_dict = {}
    for row in color_quantities:
        id = row['textile_release_id']
        color = row['color']
        size = row['size']
        quantity = row['total_quantity']
        if color not in color_quantity_dict:
            color_quantity_dict[color] = {}
        color_quantity_dict[color][size] = quantity

    return render_template("index.html", color_quantities=color_quantity_dict, id=id)

    '''
    releases = db.execute("SELECT * FROM textile_releases")

    return render_template("index.html", releases=releases)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

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

        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password does not match", 400)

        elif not request.form.get("confirmation"):
            return apology("no matching password", 400)

        hashed_password = generate_password_hash(request.form.get("password"))

        result = db.execute(
            "INSERT INTO users( username, hash) VALUES (?, ?)",
            request.form.get("username"),
            hashed_password
        )

        if not result:
            return apology("username already exist", 400)

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

      
        
    

        # Insert data into the 'textile_releases' table
        db.execute("INSERT INTO textile_releases (fecha, planta_key, ciudad, municipio_estado, codigo_postal, telefono_contacto, nombre_contacto, prendas_solicitadas) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   fecha, planta_key,  ciudad, f"{municipio}, {estado}", codigo_postal, telefono_contacto, nombre_contacto, prendas_solicitadas)
        

        new_release_id = db.execute("SELECT id FROM textile_releases ORDER BY id DESC LIMIT 1")
        new_release_id2 = new_release_id[0]['id']

        for c, t, q in zip(color, talla, cantidad):
            db.execute("INSERT INTO color_quantities (textile_release_id, color, size, total_quantity) VALUES (?, ?, ?, ?)",
                       new_release_id2, c, t, q)
        # Insert the data into the color_quantities table
        #db.execute("INSERT INTO color_quantities (textile_release_id, color, size, total_quantity) VALUES (?, ?, ?, ?)",
                   #new_release_id2, color, talla, cantidad)
        


        # Ensure all required fields are provided
        if not (fecha and planta_key and ciudad and municipio and estado and codigo_postal and telefono_contacto and nombre_contacto and prendas_solicitadas and cantidad and color and talla):
            return "All fields are required", 400

        

        # Redirect to a success page or wherever you want after insertion
        return redirect("/")
    else:
        # For GET requests, render the release.html template
        return render_template("release.html")
