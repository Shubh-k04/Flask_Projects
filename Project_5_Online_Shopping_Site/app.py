# Importing all the required modules
from flask import (
    Flask,
    flash,
    request,
    redirect,
    url_for,
    render_template,
    abort,
)
from utils.market import Market

# Create Flask and Market Instance
app = Flask(__name__)
market = Market()

# Set a password
app.config["SECRET_KEY"] = "dattebayo!"

# Create a route for home page
@app.route("/")
def home_page():
    market.set_item_status()

    if market.name:
        market.add_to_val(market.name, 3)

    timelines = market.get_timeline(market.name)

    return render_template(
        "__home_page.html", logged=market.logged, name=market.name, timeline=timelines
    )


# Route For Sign In
@app.route("/signin", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conf_password = request.form["confirm_pass"]
        f = True

        if username.count(" ") == len(username):
            flash("Invalid Username Selected!!", category="fail")
            f = False
        elif market.validate(password, conf_password):
            username = str(username.lstrip().rstrip())
            if market.validate_name(username):
                response = market.init_new(username, password)
                if not response:
                    flash("Username Already Registered", category="fail")
                    f = False
                else:
                    market.logged = True
                    market.name = username
                    flash(
                        "You Are Now Successfully Registered As {}".format(username),
                        category="success",
                    )
                    market.add_timeline(
                        market.name, "Signed Up With A Username {}".format(username)
                    )
                    return redirect(url_for("home_page"))
            else:
                flash("Invalid Characters In The Name!", category="fail")
                f = False

        if f:
            flash("Passwords Not Matching!!", category="fail")

    return render_template("__sign_in.html", logged=market.logged)


# Route FOr User Logout
@app.route("/logout")
def logout():
    market.logged = False
    flash("SuccessFully Logged Out! Thanks For Visiting Us!", category="success")
    return redirect(url_for("home_page"))


# Route For User's Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["user"]
        password = request.form["pass"]

        response = market.sign_in(username, password)

        if response:
            market.logged = True
            market.name = username
            flash("SuccessFully Logged In As {}".format(username), category="success")
            return redirect(url_for("home_page"))

        flash("Invalid Username Or Password", "fail")

    return render_template("__login.html", logged=market.logged)


# Route For User's Profile
@app.route("/profile/<username>")
def profile(username):
    get_info = market.get_info(username)

    if get_info == None:
        abort(404)

    return render_template(
        "__profile.html", items=get_info, logged=market.logged, name=username
    )


# Route For Market
@app.route("/market")
def my_market():
    if market.new_item:
        market.add_new(market.new_item)
        market.new_item = []

    items = market.get_items()

    return render_template(
        "__market.html", items=items, logged=market.logged, name=market.name
    )


# Route for Creating A New Product in the market
@app.route("/market/new", methods=["GET", "POST"])
def create_new():
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        contact = request.form["number"]

        if market.is_avail(name):
            flash(
                "Choose A Different Product Name. This Name Is Already Taken!",
                category="fail",
            )

        elif (
            name.count(" ") == len(name)
            or price.count(" ") == len(price)
            or contact.count(" ") == len(contact)
        ):
            flash("Fields Cannot Be Empty")

        elif len(contact) != 10:
            flash("The Contact Number Does Not Contain 10 Digits!!")
        else:
            market.new_item = {name: [market.name, "05 May, 2021", price]}
            coins = market.get_info(market.name, need=True)[-1]
            market.set_new(market.name, coins + 199)
            flash(
                "Successfully Added The Item To The Market. You Received 199 Points For Selling Your Product!",
                category="success",
            )
            market.add_to_val(market.name, 1)
            market.add_timeline(
                market.name, "Sold Item Named {} To The Market".format(name)
            )
            return redirect(url_for("my_market"))

    return render_template("__create.html", logged=market.logged, name=market.name)


# Route for buying products
@app.route("/buy/<name>")
def buy(name):
    cost = int(market.get_items()[name][-1])

    if market.name == None:
        flash("You Need To Login Or Sign Up Before Buying Items!!", category="fail")
        return redirect(url_for("my_market"))

    coins = market.get_info(market.name, need=True)[-1]

    if cost > coins:
        flash("Not Enough Coins To Buy This Item!!")
    else:
        market.add_excludes(name)
        flash(
            "Successfully Bought {}. Your Balace Is {}".format(name, coins - cost),
            category="success",
        )
        market.add_to_val(market.name, 2)
        market.set_new(market.name, coins - cost)
        market.add_timeline(market.name, "Bought {} From the Market".format(name))

    return redirect(url_for("my_market"))


# Route For User's bag
@app.route("/bag")
def my_bag():
    try:
        items = market.get_bag()[market.name]
        items = market.make_dict(items)
    except:
        items = {}

    return render_template(
        "__your_bag.html", logged=market.logged, name=market.name, items=items
    )


# Route For User Selling
@app.route("/sell/<name>")
def sell(name):
    cost = int(market.get_items()[name][-1])

    coins = market.get_info(market.name, need=True)[-1]

    market.remove_from_bag(name)

    market.set_new(market.name, coins + cost)

    flash(
        "SuccessFully Returned {}. Your Current Balance is {}".format(
            name, coins + cost
        ),
        category="success",
    )

    market.add_to_val(market.name, 2, True)

    market.add_timeline(market.name, "Returned {}".format(name))

    return redirect(url_for("my_bag"))


# Route For User's Uploaded Items
@app.route("/your_products")
def your_products():

    user_pro = market.get_users_products()

    return render_template(
        "__your_pros.html", logged=market.logged, name=market.name, items=user_pro
    )


# Route For Clearing The User's Browse
@app.route("/clear")
def clear_browse():
    market.clear_browse()

    flash("Removed All Recent Activites", category="success")

    market.add_timeline(market.name, "Cleared Recent Activites")

    return redirect(url_for("profile", username=market.name))


# Route For Deletion Of The User
@app.route("/delete/<username>", methods=["GET", "POST"])
def delete_user(username):
    if request.method == "POST":
        password = request.form["password"]

        res = market.compare_password(username, password)

        if res == False:
            flash("Incorrect Password", category="fail")
        else:
            res = market.remove_user(username, password)
            flash("Account Has Been Deleted Successfully", category="success")
            market.logged = False
            market.name = ""
            return redirect(url_for("home_page"))

    return render_template("__delete_user.html", logged=market.logged, name=market.name)


# Route For Removing Of The Item
@app.route("/remove/<itemname>")
def remove_item(itemname):
    market.remove_from_pros(itemname)

    market.add_to_val(market.name, 1, True)

    market.add_timeline(market.name, "Removed Item {} From The Market".format(itemname))

    return redirect(url_for("your_products"))
