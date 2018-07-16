import time
from golfers import golfers
import utils
from flask import Flask, render_template, redirect, request, jsonify, make_response

'''
#################################################################################################
########################################## App Globals ##########################################
#################################################################################################
'''

application = app = Flask(__name__)

utils = utils.Utils()

'''
#################################################################################################
###################################### Application Routes #######################################
#################################################################################################
'''

@application.route("/")
def index():
    return make_response(redirect("/home"), 302)

@application.route("/home")
def home():
    utils.updatePosition()

    return make_response(render_template("home.html", golfers=sorted(golfers, key=lambda k: k['pos'])), 200)

@application.route("/home/update")
def homeUpdate():
    return make_response(redirect("/home"), 302)

###################################
# Main function where app is run. #
###################################
if __name__ == "__main__":
    public = "0.0.0.0"
    local = "127.0.0.1"
    app.secret_key = "something"
    
    application.run(host=public, debug=False)

