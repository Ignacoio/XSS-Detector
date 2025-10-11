from flask import Flask, request
#from markupsafe import escape
app= Flask(__name__)
@app.route('/', methods=['GET']) 
def get():
    name= request.args.get('name','Juan')
    #return f"Hola{escape(name)}"
    return f"Hola{name}"
@app.route('/', methods=['POST'])
def post():
    message= request.form.get("message","hola que tal")
    return f"{message}"
if __name__== '__main__':
    app.run(debug=True)
    