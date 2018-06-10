from flask import Flask, render_template, request, redirect, session
from service import db_access
import logging,re,os


def init_config():
    """
    This method is called in beginning, it configures error handling to show CGI errors on UI and
    enables logging in proper format
    """
    log_fname = "logs/my_account_app.log"
    logging.basicConfig(filename=log_fname,
                    filemode='a',
                    level=logging.DEBUG,
                    format='%(asctime)s : %(levelname)s %(filename)s => %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                   )
init_config()
app = Flask(__name__)

dbAccess = db_access.DBAccess()

@app.before_request
def session_management():
    # make the session last indefinitely until it is cleared
    session.permanent = True

@app.route('/')
def login_page():
    # reset the session data
    session.clear()
    return render_template("login.html")

@app.route('/password.reset')
def reset_password():
    return render_template("addpayee.html")

@app.route('/money.transfer')
def transfer_money():
    return render_template("transfermoney.html")

@app.route('/money.deposit')
def deposit_money():
    return render_template("depositmoney.html")

@app.route('/payee.remove',methods=['GET', 'POST'])
def remove_payee():
    return render_template("removepayee.html")

@app.route('/payee.add',methods=['GET', 'POST'])
def add_payee():
    if 'user' in session:
        username = session.get('user')
        if request.method == 'GET':
            return render_template("addpayee.html")
        else:
            pass
    else:
        session['message']="Session invalid"
        return redirect("error", code=400)

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/home')
def homepage():
    if 'user' in session:
        username = session.get('user')
        user_profile=dbAccess.fetch_account_detail(username)
        profile = {}
        profile['Account Name']=user_profile[0]+" "+user_profile[1]
        session['user'] = username
        profile['Bank Name']=user_profile[4]
        profile['Account Number']=user_profile[2]
        profile['Account Balance']=user_profile[3]
        profile['username']=username
        return render_template("home.html",profile=profile)
    else:
        session['message']="Session invalid"
        return redirect("error", code=400)

@app.route('/error')
def error_page():
    if 'user' in session:
        message=session.get('message')
        session.clear()
        return render_template("error.html",message=message)
    else:
        return render_template("login.html")
    

@app.route('/logout')
def logout():
    session.clear()
    return render_template("login.html")
    


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = request.form
        username=form['username']
        password=form.get('password')
        logging.info("login credentials: "+username+" "+password)
        creds = (username,password)
        is_user_valid = dbAccess.validate_login(username,password)
        if(is_user_valid):
            user_profile=dbAccess.fetch_account_detail(username)
            profile = {}
            profile['Account Name']=user_profile[0]+" "+user_profile[1]
            session['user'] = username
            profile['Bank Name']=user_profile[4]
            profile['Account Number']=user_profile[2]
            profile['Account Balance']=user_profile[3]            
	    #return str(user_profile)
            return render_template("home.html",profile=profile)
        else:
            if 'user' in session:
                return session.get('user')
            else:
                return "Invalid credentials"
    else:
        # reset the session data
        #session.clear()
        return render_template("login.html")

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(port=8082,debug=True)
