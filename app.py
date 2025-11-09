from flask import Flask, request
from markupsafe import escape
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
    #return f"{escape(message)}"


#@app.after_request
#def security_headers(response):
    response.headers['Content-Security-Policy'] = (
        "default-src 'none'; "
        "script-src 'none'; "
        "style-src 'none' data:; "
        "img-src 'none' data:; "
        "object-src 'none'; "
        "frame-ancestors 'none'; "
        "base-uri 'none';"
    )
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

if __name__== '__main__':
    app.run(debug=True)
    
