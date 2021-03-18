from flask import Flask , render_template,flash ,request ,session,url_for ,redirect
from flask_sqlalchemy import SQLAlchemy

import FeatureExtraction
import pickle





app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phishdetect.sqlite3'
app.config['SECRET_KEY'] = "1234"


db = SQLAlchemy(app)

class sites(db.Model):
    id = db.Column('s.n', db.Integer, primary_key=True)
    url = db.Column(db.String(100), nullable=False)



    def __init__(self, url):
        self.url= url




@app.route("/")

def index():
    return render_template("index.html", sites=sites.query.all())

@app.route("/phishing")
def phishing():
    return render_template("phishing.html")
@app.route("/about")
def about():
    return render_template("about.html")



# @app.route('/getURL',methods=['GET','POST'])
# def getURL():
#
#     if request.method == 'POST':
#         if not request.form['url']:
#             flash("please enter url" ,'error')
#         else:
#             url = sites(request.form.get('url'))
#             db.session.add(url)
#             db.session.commit()
#             return render_template('index.html')
#     return render_template('index.html')

@app.route('/getURL', methods=['GET','POST'])
def getURL():
    if request.method == 'POST':
    #     if not request.form['url']:
    #         flash("please enter url" ,'error')
    # else:
        url = sites(request.form['url'])
        data = FeatureExtraction.testData(url)
        model = pickle.load(open('RandomForestModel.sav', 'rb'))
        predicted_value = model.predict(data)
        db.session.add(url)
        db.session.commit()

        #print(predicted_value)
        if (predicted_value==-1):
            return render_template('index.html', prediction_text='This is legit Website!')

        else:


            return render_template('index.html', prediction_text='This website is phishing')
    # return render_template("index.html")






if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)