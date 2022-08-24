import json
import os
import time
from datetime import date, datetime

from flask import Flask, url_for, request, render_template, redirect  # , flash, escape, session
from flask_bcrypt import Bcrypt
# from werkzeug.utils import secure_filename
# from werkzeug.datastructures import ImmutableMultiDict
from flask_login import LoginManager, UserMixin, login_user, login_required  # , logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
# from requests import RequestException
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length  # , ValidationError


def anyempty(*args):
    for i in args:
        if i == "":
            return False
    return True

def TimeConvert(day=date.today()):
    w = day.day
    month = day.strftime("%b")  # defines the correct month
    year = day.strftime("%Y")  # defines the correct year
    time_obj = time.localtime()
    local_time = time.strftime("%a " + str(month) + " " + str(w) + " " + str(20) + ":00:00 " + year, time_obj)
    time_sting = time.strptime(local_time)
    converted_time = str(time.mktime(time_sting)).split(".")[0]
    return converted_time

def TimeConvert2(t):
    converted_time = str(datetime.utcfromtimestamp(float(t) + .0)).split(" ")[0]
    return converted_time

def OrderTableKeyTime(elem):
    return elem[1]

def OrderTableKeyDiff(elem):
    return elem[2]

# for uploading ---------------------------------------------------------------
folder = "static/images/dynamic/images"
extensions = {"jpg", "png", "svg", "txt"}

def fileallowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in extensions
# json-functions -------------------------------------------------------------

def SafeContentToJson():
    try:
        with open("static/data/about.txt", "r") as f:
            content = f.read()
            dictionary = {
                "about_content": content,
            }
            json_obj = json.dumps(dictionary, indent=1)
            with open("static/data/about_data.json", "w") as jsonfile:
                jsonfile.write(json_obj)
    except KeyError:
        return redirect(url_for("admin"))
def GetJsonContent(content):
    with open("static/data/about_data.json") as f:
        data = json.load(f)
        return data[content]

def AddMemberToJson(name, status):
    try:
        with open("static/data/member_data.json", "r") as f:
            data = json.load(f)
        color = "#48cdff"
        if status == "Leader":
            color = "#042478"
        elif status == "Co-Leader":
            color = "#581378"
        elif status == "Freeze1":
            color = "#48cdff"
        elif status == "Freeze2":
            color = "#9efff3"
        dictionary = {
            "Name": name,
            "Status": status,
            "MiiPath": f"images/dynamic/images/Member/Miis/Mii_{name}.png",
            "FlagPath": f"images/dynamic/images/Member/Flags/Flag_{name}.png",
            "Color": color
        }
        data["Members"][name] = dictionary
        with open("static/data/member_data.json", "w") as f:
            json.dump(data, f, indent=4)
    except KeyError:
        return redirect(url_for("admin"))
def RemoveMemberFromJson(name):
    try:
        with open("static/data/member_data.json", "r") as f:
            data = json.load(f)
            del data["Members"][name]
        with open("static/data/member_data.json", "w") as f:
            json.dump(data, f, indent=4)
    except KeyError:
        return redirect(url_for("admin"))
def GetJsonMembers():
    with open("static/data/member_data.json") as f:
        data = json.load(f)["Members"]
    return data

def AddNewsToJson(title, author, color):
    try:
        with open("static/data/news_data.json", "r") as f:
            data = json.load(f)
            id = len(data["News"])
        with open("static/data/news.txt", "r") as f:
            content = f.read()
        dictionary = {
            "Title": title,
            "Author": author,
            "Content": content,
            "Color": color,
            "id": id,
            "Date": date.today().strftime("%B %d, %Y")
        }
        data["News"][id] = dictionary
        with open("static/data/news_data.json", "w") as f:
            json.dump(data, f, indent=4)
    except KeyError:
        return redirect(url_for("admin"))
def RemoveNewsFromJson(id):
    try:
        with open("static/data/news_data.json", "r") as f:
            data = json.load(f)
            del data["News"][str(id)]
        with open("static/data/member_data.json", "w") as f:
            json.dump(data, f, indent=4)
    except KeyError:
        return redirect(url_for("admin"))
def GetJsonNews():
    with open("static/data/news_data.json", "r") as f:
        data = json.load(f)["News"]
    return data

def AddTableToJson(id, team, opponent, type, result, difference, tabledate):
    try:
        with open("static/data/table_data.json", "r") as f:
            data = json.load(f)
        dictionary = {
            "ID": id,
            "Team": team,
            "Opponent": opponent,
            "Type": type,
            "Result": result,
            "Difference": difference,
            "Date": tabledate,
            "filepath": f"images/dynamic/images/tables/Table_{id}.png"
        }
        data["Tables"][id] = dictionary
        with open("static/data/table_data.json", "w") as f:
            json.dump(data, f, indent=4)
    except KeyError:
        return redirect(url_for("admin"))
def RemoveTableFromJson(ID):
    try:
        with open("static/data/table_data.json", "r") as f:
            data = json.load(f)
            del data["Tables"][str(ID)]
        with open("static/data/table_data.json", "w") as f:
            json.dump(data, f, indent=4)
    except KeyError:
        return redirect(url_for("admin"))
def GetJsonTable():
    with open("static/data/table_data.json", "r") as f:
        data = json.load(f)["Tables"]
    return data

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.db"
app.config["SECRET_KEY"] = '\x10!\xa5A\xbc\x0f+s\xf7v\x1a\xb4\xd1\x7fy\x9c\xa5 3C\xb7T\xd9\xb6H\xfd\\\x1bsp~\xe2$\xe4\xe5\xef\xea\xaa\x81:\xc5\xa7\xb8'
app.config['UPLOAD_FOLDER'] = folder

@app.errorhandler(404)
def page_not_found(event):
    return render_template("404.html", event=event)

# login
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(10), nullable=False, unique=True)
    password = db.Column(db.String(50))

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=5, max=5)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=12)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

# class RegisterForm(FlaskForm):
#     username = StringField(validators=[InputRequired(), Length(min=5, max=5)], render_kw={"placeholder": "Username"})
#     password = PasswordField(validators=[InputRequired(), Length(min=4, max=12)], render_kw={"placeholder": "Password"})
#     submit = SubmitField("Register")

#     def validate_username(self, username):
#         existing_user_name = User.query.filter_by(
#             username=username.data).first()
#         if existing_user_name:
#             raise ValidationError

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# go to the correct templates -------------------------------------------------
@app.route("/")
def index():
    return render_template("home.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    about_text = GetJsonContent("about_content")
    return render_template("about.html", about_text=about_text)

@app.route("/our-members")
def our_members():
    data = GetJsonMembers()
    Leaders = []
    CoLeaders = []
    Freeze1 = []
    Freeze2 = []
    for i in data:
        if data[i]["Status"] == "Leader":
            Leaders.append(data[i])
        elif data[i]["Status"] == "Co-Leader":
            CoLeaders.append(data[i])
        elif data[i]["Status"] == "Freeze1":
            Freeze1.append(data[i])
        elif data[i]["Status"] == "Freeze2":
            Freeze2.append(data[i])
    return render_template("our-members.html", Leaders=Leaders, CoLeaders=CoLeaders, Freeze1=Freeze1, Freeze2=Freeze2)

@app.route("/tables")
def tables():
    table_bool = request.args.get("table")
    if table_bool is None and len(request.args.getlist("table_list")) == 0:
        raw_table_list = []
        table_list = []
        data = GetJsonTable()
        for i in data:
            table = i
            raw_table_list.append([data[table]["filepath"], data[table]["Date"]])
        raw_table_list.sort(key=OrderTableKeyTime, reverse=True)
        for i in raw_table_list:
            table_list.append(i[0])
    else:
        table_list = request.args.getlist("table_list")

    if table_bool is True:
        table_bool = "True"
    elif table_bool is False:
        table_bool = "False"
    elif table_bool is None:
        table_bool = "None"

    if table_bool in ["True", "None"]:
        table_bool = "Tables"
    else:
        table_bool = "NoTables"
    print(table_list)

    if request.args.get("filtered") is None:
        settings = ['checked', 'checked', 'checked', 'checked',
                    'checked', 'checked', 'checked', 'checked', 'checked', 'checked', 'checked',
                    "2020-08-29", TimeConvert2(TimeConvert()),
                    'checked', 'checked', 'checked', 'checked',
                    'checked', 'checked', 'checked',
                    'checked', '', '', '']
    else:
        settings = request.args.getlist("settings")
    return render_template("tables.html", table=table_bool, tables=table_list, settings=settings, amount=len(table_list))

@app.route("/news")
def news():
    data = GetJsonNews()
    return render_template("news.html", news=data)

@app.route("/impressum")
def impressum():
    return render_template("impressum.html")

@app.route("/admin")
@login_required
def admin():
    return render_template("admin.html")

# uploads -----------------------------------------------------------------------
@app.route("/admin", methods=["GET", "POST"])
def upload_admin():
    if request.method == "POST":
        # home
        formID = request.args.get("formID", 1, type=str)
        if "NewTeamBanner1" in request.files:
            file = request.files["NewTeamBanner1"]
            filename = "frz1-teambanner.png"
        elif "NewTeamBanner2" in request.files:
            file = request.files["NewTeamBanner2"]
            filename = "frz2-teambanner.png"
        elif "NewTeamLogo1" in request.files:
            file = request.files["NewTeamLogo1"]
            filename = "frz1-logo.png"
        elif "NewTeamLogo2" in request.files:
            file = request.files["NewTeamLogo2"]
            filename = "frz2-logo.png"
        # about
        elif "NewAboutText" in request.files:
            file = request.files["NewAboutText"]
            file.save(os.path.join("static/data", "about.txt"))
            SafeContentToJson()
            return redirect(url_for("admin"))
        # members
        elif formID == "AddMember":
            AddMii = request.files["AddMii"]
            AddFlag = request.files["AddFlag"]
            AddName = request.form.getlist("AddName")[0]
            Status = request.form.getlist("Status")[0]
            if anyempty(AddMii, AddFlag, AddName, Status):
                if "AddMii" in request.files:
                    file = request.files["AddMii"]
                    filename = "Mii_" + AddName + ".png"
                    Miifolder = "static/images/dynamic/images/Member/Miis"
                    if file and fileallowed(file.filename):
                        file.save(os.path.join(Miifolder, filename))
                else:
                    return redirect(url_for("admin"))
                if "AddFlag" in request.files:
                    file = request.files["AddFlag"]
                    filename = "Flag_" + AddName + ".png"
                    Flagfolder = "static/images/dynamic/images/Member/Flags"
                    if file and fileallowed(file.filename):
                        file.save(os.path.join(Flagfolder, filename))
                AddMemberToJson(AddName, Status)
            return redirect(url_for("admin"))
        elif formID == "RemoveMember":
            RemoveName = request.form.getlist("RemoveName")[0]
            if anyempty(RemoveName):
                RemoveMemberFromJson(RemoveName)
            return redirect(url_for("admin"))
        # news
        elif formID == "AddNews":
            Title = request.form.getlist("AddNewsTitle")[0]
            Author = request.form.getlist("AddNewsAuthor")[0]
            Color = request.form.getlist("AddNewsColor")[0]
            if anyempty(Title, Author, Color):
                if "AddNewsContent" in request.files:
                    file = request.files["AddNewsContent"]
                    filename = "news.txt"
                    news_folder = "static/data"
                    if file and fileallowed(file.filename):
                        file.save(os.path.join(news_folder, filename))
                    AddNewsToJson(Title, Author, Color)
                    return redirect(url_for("admin"))
            return redirect(url_for("admin"))
        elif formID == "RemoveNews":
            RemoveID = request.form.get("NewsRemoveID")
            if anyempty(RemoveID):
                RemoveNewsFromJson(RemoveID)
            return redirect(url_for("admin"))
        # tables
        elif formID == "AddTable":
            ID = str(request.form.getlist("AddTableID")[0])
            Team = request.form.getlist("Team")[0]
            Opponent = request.form.getlist("Opponent")[0]
            Type = request.form.getlist("Type")[0]
            Result = request.form.getlist("Result")[0]
            Difference = request.form.get("AddDifference")
            TableDate = int(TimeConvert(datetime.strptime(request.form.get("TableDate"), "%Y-%m-%d"))) + 86399
            Date = str(TableDate)
            if anyempty(ID, Team, Opponent, Type, Result, Date):
                if "AddTable" in request.files:
                    file = request.files["AddTable"]
                    filename = f"Table_{ID}.png"
                    table_folder = "static/images/dynamic/images/tables"
                    if file and fileallowed(file.filename):
                        file.save(os.path.join(table_folder, filename))
                    AddTableToJson(ID, Team, Opponent, Type, Result, Difference, Date)
                    return redirect(url_for("admin"))
            return redirect(url_for("admin"))
        elif formID == "RemoveTable":
            ID = request.form.getlist("TableRemoveID")[0]
            if anyempty(ID):
                RemoveTableFromJson(ID)
            return redirect(url_for("admin"))
        # home ~~~
        else:
            return redirect(request.url)
        if file.filename == '':
            return redirect(request.url)
        if file and fileallowed(file.filename):
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return redirect(url_for("admin"))
    return render_template("admin.html")


# login ---------------------------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("admin"))
    return render_template("login.html", form=form)

    # form = RegisterForm()

    # if form.validate_on_submit():
    #     hashed_password = bcrypt.generate_password_hash(form.password.data)
    #     new_user = User(username=form.username.data, password=hashed_password)
    #     db.session.add(new_user)
    #     db.session.commit()
    # return render_template("login.html", form=form)


# tables ---------------------------------------------------------------------
@app.route("/tables", methods=["GET", "POST"])
def data_filter_tables():
    OrderOption = None
    table_bool = None
    ordered_table_list = []
    settings = []

    if request.method == "POST":
        formID = request.args.get("formID", 1, type=str)
        if formID == "FilterTables":
            TeamList = []
            OpponentList = []
            TypeList = []
            ResultList = []

            def CheckForList(var, name, endlist):
                if var == "on":
                    endlist.append(name)
                else:
                    pass

            TeamFRZ1 = request.form.get("TeamFRZ1")
            TeamFRZ2 = request.form.get("TeamFRZ2")
            TeamMixed = request.form.get("TeamMixed")
            TeamOldFreeze = request.form.get("OldFreeze")
            CheckForList(TeamFRZ1, "FRZ1", TeamList)
            CheckForList(TeamFRZ2, "FRZ2", TeamList)
            CheckForList(TeamMixed, "Mixed", TeamList)
            CheckForList(TeamOldFreeze, "OldFreeze", TeamList)

            OpponentNN = request.form.get("OpponentNN")
            OpponentEn = request.form.get("OpponentEn")
            OpponentNANA = request.form.get("OpponentNANA")
            OpponentEt = request.form.get("OpponentEt")
            OpponentLTG = request.form.get("OpponentLTG")
            OpponentHTS = request.form.get("OpponentHTS")

            OpponentOther = request.form.get("OpponentOther")
            CheckForList(OpponentNN, "NN", OpponentList)
            CheckForList(OpponentEn, "En", OpponentList)
            CheckForList(OpponentNANA, "NANA", OpponentList)
            CheckForList(OpponentEt, "Et", OpponentList)
            CheckForList(OpponentLTG, "LTG", OpponentList)
            CheckForList(OpponentHTS, "HTS", OpponentList)
            CheckForList(OpponentOther, "Other", OpponentList)

            TimespanFrom = TimeConvert(datetime.strptime(request.form.get("TimespanFrom"), "%Y-%m-%d"))
            TimespanTo = TimeConvert(datetime.strptime(request.form.get("TimespanTo"), "%Y-%m-%d"))

            Type200L = request.form.get("Type200L")
            TypeScrimm = request.form.get("TypeScrimm")
            TypeInclan = request.form.get("TypeInclan")
            Type150 = request.form.get("Type150")
            CheckForList(Type200L, "200L", TypeList)
            CheckForList(TypeScrimm, "Scrimmage", TypeList)
            CheckForList(TypeInclan, "Inclan", TypeList)
            CheckForList(Type150, "150 War", TypeList)

            ResultWin = request.form.get("ResultWin")
            ResultTie = request.form.get("ResultTie")
            ResultLoss = request.form.get("ResultLoss")
            CheckForList(ResultWin, "Win", ResultList)
            CheckForList(ResultTie, "Tie", ResultList)
            CheckForList(ResultLoss, "Loss", ResultList)


            table_list = []
            data = GetJsonTable()

            OrderNewest = request.form.get("OrderNewest")
            OrderOldest = request.form.get("OrderOldest")
            OrderBest = request.form.get("OrderBest")
            OrderWorst = request.form.get("OrderWorst")
            if OrderNewest == "on":
                OrderOption = "Newest"
            elif OrderOldest == "on":
                OrderOption = "Oldest"
            elif OrderBest == "on":
                OrderOption = "Best"
            elif OrderWorst == "on":
                OrderOption = "Worst"

            c = 0
            for i in data:
                c += 1

                table = i
                table_team = data[table]["Team"]
                table_opponent = data[table]["Opponent"]
                table_time = data[table]["Date"]
                table_type = data[table]["Type"]
                table_result = data[table]["Result"]

                Team = table_team in TeamList
                Opponent = table_opponent in OpponentList
                Timespan = int(table_time) in range(int(TimespanFrom), int(TimespanTo))
                Type = table_type in TypeList
                Result = table_result in ResultList


                if Team and Opponent and Timespan and Type and Result:
                    table = [data[table]["filepath"], data[table]["Date"], data[table]["Difference"]]
                    table_list.append(table)
                if c == len(data) and len(table_list) == 0:
                    table_bool = False
                else:
                    table_bool = True

            function = None
            table_reversed = None

            if OrderOption == "Newest":
                function = OrderTableKeyTime
                table_reversed = False
            elif OrderOption == "Oldest":
                function = OrderTableKeyTime
                table_reversed = True
            elif OrderOption == "Best":
                function = OrderTableKeyDiff
                table_reversed = False
            elif OrderOption == "Worst":
                function = OrderTableKeyDiff
                table_reversed = True


            settings_raw = [TeamFRZ1, TeamFRZ2, TeamMixed, TeamOldFreeze,
                            OpponentNN, OpponentEn, OpponentNANA, OpponentEt, OpponentLTG, OpponentHTS, OpponentOther,
                            TimeConvert2(TimespanFrom), TimeConvert2(TimespanTo),
                            Type200L, TypeScrimm, TypeInclan, Type150,
                            ResultWin, ResultTie, ResultLoss,
                            OrderNewest, OrderOldest, OrderBest, OrderWorst]
            settings = []
            for i in settings_raw:
                if i is None:
                    settings.append("")
                elif i == "on" or i == "checked":
                    settings.append("checked")
                else:
                    settings.append(i)

            try:
                table_list.sort(key=function)
                if table_reversed is True:
                    table_list.reverse()
            except TypeError:
                return redirect(url_for("tables", table=False, table_list=[], settings=settings, Order=None, filtered=True))
            ordered_table_list = []
            for i in table_list:
                ordered_table_list.append(i[0])
            ordered_table_list.reverse()
    return redirect(url_for("tables", table=table_bool, table_list=ordered_table_list, Order=OrderOption, settings=settings, filtered=True))


# nav bar----------------------------------------------------------------------
@app.route('/home', methods=['GET', 'POST'])
def to_home():
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('home.html')

@app.route('/about', methods=['GET', 'POST'])
def to_about():
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('about.html')

@app.route('/our-members', methods=['GET', 'POST'])
def to_our_members():
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('our-members.html')

@app.route('/tables', methods=['GET', 'POST'])
def to_tables():
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('tables.html')

@app.route('/news', methods=['GET', 'POST'])
def to_news():
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('news.html')

@app.route('/impressum', methods=['GET', 'POST'])
def to_impressum():
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('impressum.html')

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def to_admin():
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('admin.html')


if __name__ == "__main__":
    app.run(port=5000, debug=True)
