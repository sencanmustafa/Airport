from flask import Flask , redirect , render_template,request,session,logging,url_for
from flask_mysqldb import MySQL
from math import radians , cos , sin , asin , sqrt
from wtforms import Form,StringField,TextAreaField,PasswordField,validators




app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "seroskom2001"
app.config["MYSQL_DB"] = "airport"


mysql = MySQL(app)
app.secret_key = ["MUSTAFA"]

class HtmlForm(Form):
    text1 = StringField("Departure",validators=[validators.data_required()])
    text2 = StringField("Arrival",validators=[validators.data_required()])

list = []

def distance(lat1,lat2,lon1,lon2):
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    dlon = lon2-lon1
    dlat = lat2-lat1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return (c*r)

@app.route("/",methods = ["GET","POST"])
def index():
    html_form = HtmlForm(request.form)
    if request.method == "POST":
        txt1 = html_form.text1.data
        txt2 = html_form.text2.data
        cursor = mysql.connection.cursor()
        query = f"SELECT coordinates FROM airport.airport_codes where iata_code='{txt1}' or iata_code='{txt2}' "
        cursor.execute(query)
        rows = []
        for data in cursor:
            rows.append(data)
        a = rows[0]
        c = rows[1]
        d = c[0].split(",")
        b = a[0].split(",")
        lat1 = float(b[0])
        long1 = float(b[1])
        lat2 = float(d[0])
        long2 = float(d[1])
        km = distance(lat1,lat2,long1,long2)
        session["my_list"] = list
        list.append(km)
        return redirect(url_for("index",my_list=list))
    list.clear()
    return render_template("index.html",form = html_form)

if __name__ == "__main__":
    app.run(debug=True)
