from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from services.auth_client import signup, login as do_login, AuthError

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/signup", methods=["GET", "POST"])
def signup_view():
    if request.method == "POST":
        try:
            user_id = signup(
                request.form["name"].strip(),
                request.form["email"].strip().lower(),
                request.form["password"],
            )
            session["user_id"] = user_id
            session["user_name"] = request.form["name"].strip()
            flash("Welcome to Find Fitness!", "success")
            return redirect(url_for("search.home"))
        except AuthError as exc:
            flash(str(exc), "error")
    return render_template("signup.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            user = do_login(request.form["email"].strip().lower(), request.form["password"])
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            flash(f"Welcome back, {user['name']}.", "success")
            return redirect(url_for("search.home"))
        except AuthError as exc:
            flash(str(exc), "error")
    return render_template("login.html")


@bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out.", "success")
    return redirect(url_for("auth.login"))