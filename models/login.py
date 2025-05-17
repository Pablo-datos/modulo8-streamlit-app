# models/login.py

def check_login(username, password):
    # Esta función simplemente revisa si el usuario es admin y la contraseña también.
    return username == "admin" and password == "admin"
