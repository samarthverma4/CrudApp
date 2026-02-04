from flask import Flask,render_template, request , redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.app_context().push()

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(500), nullable=False)
    def __repr__(self):
        return f"{self.id}-{self.name}"

@app.route("/",methods=['GET','POST'])
def home():
    if request.method == 'POST':
        employee = Employee(name=request.form['fullName'], email=request.form['email'])
        db.session.add(employee)
        db.session.commit()
    
    allemployees = Employee.query.all()
    return render_template("index.html",allemployees=allemployees)
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/delete/<int:sno>")
def delete(sno):
    employee = Employee.query.filter_by(id=sno).first()
    db.session.delete(employee)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        employee = Employee.query.filter_by(id=sno).first()
        employee.name = request.form['fullName']
        employee.email = request.form['email']
        db.session.add(employee)
        db.session.commit()
        return redirect("/")
    
    employee = Employee.query.filter_by(id=sno).first()
    return render_template("update.html", employee=employee)

if __name__ == "__main__":
    app.run(debug=True)