import utils
from golfers import golfers
from flask import Flask, render_template, redirect, request, jsonify, make_response, url_for

'''
#################################################################################################
########################################## App Globals ##########################################
#################################################################################################
'''

app = Flask(__name__)

utils = utils.Utils()

'''
#################################################################################################
###################################### Application Routes #######################################
#################################################################################################
'''

@app.route('/')
def index():
    return make_response(redirect(url_for('home')), 302)

@app.route('/home')
def home():
    utils.updatePosition()
    
    return make_response(render_template('home.html', golfers=sorted(golfers, key=lambda k: k['pos'])), 200)

@app.route('/home/update')
def homeUpdate():
    print "Refreshing page!"
    return make_response(redirect(url_for('home')), 302)

###################################
# Main function where app is run. #
###################################
if __name__ == "__main__":
    public = "0.0.0.0"
    local = "127.0.0.1"
    app.secret_key = "something"
    
    # app.run(host=local, debug=True)
    app.run()

