from flask import Flask,redirect,url_for,render_template,request
global user
app=Flask(__name__)
@app.route("/")
def home():
	return render_template("test.html")
@app.route("/login",methods=["POST","GET"])
def login():
	global user
	if request.method == "POST":
		user = request.form["pname"]
		return redirect(url_for("user",usr=user))
	else:
		f = open("parrot1.txt","w+")
		pn = request.form["pname"]
		f.write(pn)
		a = request.form["age"]
		f.write(pn)
		w = request.form["weight"]
		f.write(pn)
		g = request.form["gender"]
		f.write(pn)
		p_no=request.form["pno"]
		f.write(pn)
		pr =request.form["problem"]
		f.write(pn)
		f.write("trying1111")
		f.close()
		return render_template("login.html")
@app.route("/<usr>")
def user(usr):
	return f"<h1>{usr}</h1>"
if __name__=="__main__":
	app.run(debug=True)