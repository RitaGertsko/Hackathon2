from app.models import Users

def check_user(email):
    return Users.query.filter_by(email=f'{email}').first()

def check_password(email, password):
    return password == Users.query.filter_by(email=email).first().password