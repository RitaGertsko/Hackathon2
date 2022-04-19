from app import my_app, db
from flask import render_template, redirect, url_for, flash, request
from app.forms import RegistrationForm, LoginForm, SearchForm
from app.models import Sales, Articles, Users, Products, Cart
from app.operate_user_data import check_user, check_password

logged_user = None


@my_app.route('/', methods=['GET', 'POST'])
def home():
    sales = Sales.query.all()
    first_skin_care_article = Articles.query.filter_by(category='skin care').order_by(Articles.id.desc()).first()
    first_hair_article = Articles.query.filter_by(category='hair').order_by(Articles.id.desc()).first()
    first_makeup_article = Articles.query.filter_by(category='makeup').order_by(Articles.id.desc()).first()

    return render_template('index.html', title='Home', sales=sales, skin_care_article=first_skin_care_article,
                           hair_article=first_hair_article, makeup_article=first_makeup_article)


@my_app.route('/registration', methods=['GET', 'POST'])
def sing_up():
    form = RegistrationForm()
    if form.validate_on_submit():
        if not check_user(form.email.data):
            new_user = Users(first_name=form.first_name.data,
                             last_name=form.last_name.data,
                             email=form.email.data,
                             password=form.password.data,
                             age=form.age.data)
            db.session.add(new_user)
            db.session.commit()

            flash("User created successfully", 'success')
            return redirect(url_for('home'))
        else:
            flash("User with this email already exists, try again", 'danger')
    return render_template('registration.html', title='Sing Up', form=form)


@my_app.route('/login', methods=['GET', 'POST'])
def login():
    global logged_user
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        if user := check_user(email):
            if check_password(email, password):
                logged_user = user
                flash(f"{email} logged in successfully", 'success')
                return redirect(url_for('home'))
            else:
                flash("Password incorrect, please try again", 'danger')
        else:
            flash("Email incorrect or not exists, please try again", 'danger')
    return render_template('login.html', title='Login', form=form)


@my_app.context_processor
def base():
    formSearch = SearchForm()
    return dict(formSearch=formSearch)


@my_app.route("/search_products", methods=['GET', 'POST'])
def search():
    formSearch = SearchForm()
    if formSearch.validate_on_submit:
        if formSearch.data['submit']:
            word_searched = request.form['searched']
            products = Products.query.filter(Products.title.like(f'%{word_searched}%')).all()
            return render_template('search_products.html', form=formSearch, title='Search', products=products)
    return redirect(url_for('home'))


@my_app.route('/skinCare', methods=['GET', 'POST'])
def skin_care():
    products = Products.query.filter(Products.category == 'skin care')
    return render_template('skin_care.html', title='Skin Care', products=products)


@my_app.route('/hair_products', methods=['GET', 'POST'])
def hairCare():
    products = Products.query.filter(Products.category == 'hair')
    return render_template('hair_care.html', title='Hair Care', products=products)


@my_app.route('/makeup_products', methods=['GET', 'POST'])
def makeupProducts():
    products = Products.query.filter(Products.category == 'makeup')
    return render_template('makeup_products.html', title='Makeup Products', products=products)


@my_app.route('/body_products', methods=['GET', 'POST'])
def bodyCare():
    products = Products.query.filter(Products.category == 'body')
    return render_template('body_products.html', title='Body Care', products=products)


@my_app.route('/product_info/<int:product_id>')
def productInfo(product_id):
    product = Products.query.filter_by(id=product_id).first()
    return render_template('product_info.html', title='Product Info', product=product)


@my_app.route("/cart", methods=["GET", "POST"])
def cart():
    cart_items = Products.query.join(Cart).add_columns(Products.cart_quantity, Products.price, Products.title,
                                                       Products.img,
                                                       Products.id).all()
    total = 0
    for item in cart_items:
        total += float(item.price) * int(item.cart_quantity)

    if request.method == "POST":
        qty = request.form.get("qty")
        id_product = request.form.get("id-product")
        cart_item = Products.query.filter(Products.id == id_product).first()
        cart_item.cart_quantity = qty
        db.session.commit()
        cart_items = Products.query.join(Cart).add_columns(Products.cart_quantity, Products.price, Products.title,
                                                           Products.img,
                                                           Products.id).all()
        total = 0
        for item in cart_items:
            total += float(item.price) * int(item.cart_quantity)

    return render_template('cart.html', title='Cart', cart=cart_items, total=round(total, 2))


@my_app.route('/addToCart/<int:product_id>')
def addToCart(product_id):
    product = Cart.query.filter_by(product_id=product_id).first()
    if product:
        product = Products.query.filter(Products.id == product_id, Products.cart_quantity > 0).first()
        product.cart_quantity += 1
        db.session.commit()
        flash('This item is already in your cart, 1 more added!', 'success')
    else:
        product = Products.query.filter_by(id=product_id).first()
        cart_item = Cart(cart_items=product)
        product.cart_quantity = 1
        db.session.add(cart_item)
        db.session.commit()
        flash('Your item has been added to your cart!', 'success')
    return redirect(url_for('cart'))


@my_app.route("/removeFromCart/<int:product_id>")
def removeFromCart(product_id):
    product = Products.query.filter(Products.id == product_id, Products.cart_quantity > 0).first()
    product.cart_quantity = 0
    item_to_remove = Cart.query.filter_by(product_id=product_id).first()
    db.session.delete(item_to_remove)
    db.session.commit()
    flash('Your item has been removed from your cart!', 'danger')
    return redirect(url_for('cart'))


@my_app.errorhandler(404)
def error_404():
    return render_template("./errors/404_error.html"), 404
