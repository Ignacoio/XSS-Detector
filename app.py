from flask import Flask, request
#from markupsafe import escape
app= Flask(__name__)
@app.route('/') 
def index():
    name= request.args.get('name','Juan')
    #return f"Hola{escape(name)}"
    return f"Hola{name}"
if __name__== '__main__':
    app.run(debug=True)
    