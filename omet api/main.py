import os
import json
import random
import platform
from config import *
from selenium import webdriver
from flask import Flask, request, render_template
from flask_restful import Resource, Api
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--disable-infobars") 
options.add_argument("--headless")

driver = webdriver.Chrome("driver\chromedriver.exe", chrome_options=options)
driver.maximize_window()
driver.implicitly_wait(10)

_SYMBOLS  =  "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"

def login(_username, _password) -> ... :
    try:
        pass
    except:
        return {"response": "error"}
    else:

        _token = "".join(

            random.choice(_SYMBOLS)
                for i in range(20))
        
        append_blank = {
            _token: {
                "username": _username,
                "password": _password
            }
        }
        
        data = json.load(
            open("tokens.json"))
        
        data.append(append_blank)
        with open("tokens.json", "w") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

        return _token

class Token:

    def create_token(username, password) -> str:
        _token = login(username,
        password)

        print("был создан токен!")
        return _token
    
    def get_token_info(__token__):
        try:
            with open("tokens.json") as file:
                token_file = json.load(file)

                for username in token_file:

                    users_data = []
                    users_data.append(username)

                    return {"response": users_data}
        except:
            return {"response": "error"}     

        
def textParser(text: str, index: int) -> int:
    return text.split()[index]

app = Flask(__name__, template_folder="site")
api = Api(app)

@app.route('/', methods=["GET"])
def mainPage():
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(error):

    with open("site/errors/notfound.html", "r") as page:
        html = page.read()

    return html, 404

@app.errorhandler(500)
def page_not_found(error):

    with open("site/errors/servererror.html", "r") as page:
        html = page.read()

    return html, 500

@app.route("/getBestDonater", methods=["GET"])
def load_getBestDonater():
    return render_template("methods/getBestDonater.html")

@app.route("/getBestFan", methods=["GET"])
def load_getBestFan():
    return render_template("methods/getBestFan.html")

@app.route("/getDescription", methods=["GET"])
def load_getDescription():
    return render_template("methods/getDescription.html")

@app.route("/getFavoriteCommunity", methods=["GET"])
def load_getFavoriteCommunity():
    return render_template("methods/getFavoriteCommunity.html")

@app.route("/getFollowers", methods=["GET"])
def load_getFollowers():
    return render_template("methods/getFollowers.html")

@app.route("/getFollows", methods=["GET"])
def load_getFollows():
    return render_template("methods/getFollows.html")

@app.route("/getHotness", methods=["GET"])
def load_getHotness():
    return render_template("methods/getHotness.html")

@app.route("/getLevel", methods=["GET"])
def load_getLevel():
    return render_template("methods/getLevel.html")

@app.route("/getStreamName", methods=["GET"])
def load_getStreamName():
    return render_template("methods/getStreamName.html")

@app.route("/getTeam", methods=["GET"])
def load_getTeam():
    return render_template("methods/getTeam.html")

@app.route("/isMinecraftHost", methods=["GET"])
def load_isMinecraftHost():
    return render_template("methods/isMinecraftHost.html")

@app.route("/isOnline", methods=["GET"])
def load_isOnline():
    return render_template("methods/isOnline.html")

@app.route("/isStream", methods=["GET"])
def load_isStream():
    return render_template("methods/isStream.html")

@app.route("/isVerified", methods=["GET"])
def load_isVerified():
    return render_template("methods/isVerified.html")

@app.route("/brawlstars", methods=["GET"])
def load_brawlstars():
    return render_template("rfl.html")

@app.route("/api", methods=["GET"])
def mainApi():
    return render_template("methods/getToken.html")

@app.route("/api/getAdminData", methods=["GET"])
def getAdminData():

    DATA = {
        "result": {
            "SYSTEM":           platform.system(),
            "NODE":             platform.node(),
            "ARCHITECTURE":     platform.architecture(),
            "VERSION":          platform.version(),
            "NAME":             platform.uname()
        }
    }

    return DATA

@app.route("/api/createToken", methods=["GET"])
def create_token():

    username = request.args.get("username")
    password = request.args.get("password")

    if (username == None or password == None):
        return {"response": "token error"}
    else:
        token = Token.create_token(username=username, 
        password=password)

        return {"response": token}
    
@app.route("/api/Fh1Ih59jL", methods=["GET"])
def getToken():

    username = request.args.get("username")
    password = request.args.get("password")

    if (username == None or password == None):
        return {"response": "token error"}
    else:
        token = Token.create_token(username=username, 
        password=password)

        return token
    
@app.route('/api/getFollowers', methods=["GET"])
def followers():

    username = request.args.get("username")

    if (username == None):
        return {"response": "username not found"}
    
    driver.get(URL+username)
    followers = driver.find_element(By.XPATH, '//*[@id="user-profile"]/div/div[2]/div/div[2]/div/div[3]/span/span[1]/span')
        
    return {"response":followers.get_attribute("textContent")}

@app.route('/api/getLevel', methods=["GET"])
def level():

    username = request.args.get("username")

    if (username == None):
        return {"response": "username not found"}
    
    driver.get(URL+username)
    level = driver.find_element(By.XPATH, '//*[@id="user-profile"]/div/div[2]/div/div[2]/div/div[2]/span[1]')
        
    return {"response":textParser(level.get_attribute("textContent"), 1)}

@app.route("/api/getDescription")
def getDescription():

    username = request.args.get("username")

    if (username == None):
        return {"response": "username not found"}
    
    driver.get(URL+username)
    description = driver.find_element(By.XPATH, '//*[@id="user-profile"]/div/div[4]/div[1]/div/div/div[2]/pre/span')

    response = description.get_attribute("textContent")

    return {"response":response}

@app.route("/api/getModerators")
def getModerators():

    username = request.args.get("username")

    list = []

    if (username == None):
        return {"response": "username not found"}
    
    driver.get(URL+username)
    moderators = driver.find_element(By.XPATH, '//*[@id="user-profile"]/div/div[4]/div[2]/div[3]/div[3]/div[3]/div[3]')

    return {"response":moderators.get_attribute("textContent")}

@app.route("/api/getFollows")
def getFollows():

    username = request.args.get("username")

    if (username == None):
        return {"response": "username not found"}
    
    driver.get(URL+username)
    follows = driver.find_element(By.XPATH, '//*[@id="user-profile"]/div/div[2]/div/div[2]/div/div[3]/span/span[2]/span')

    response = follows.get_attribute("textContent")

    return {"response":response}

@app.route("/api/getFavoriteCommunity")
def getFavoriteCommunity():

    username = request.args.get("username")

    if (username == None):
        return {"response":"username not found"}
    
    driver.get(URL+username)

    try:
        community = driver.find_element(By.XPATH, '//*[@id="user-profile"]/div/div[4]/div[1]/div/div/div[8]/div[2]/a/div[3]/h1')
    except:
        return {"response":"user does not have a favorite community"}

    response = community.get_attribute("textContent")

    return {"response":response}

@app.route("/api/getTeam")
def getTeam():

    username = request.args.get("username")

    if (username == None):
        return {"response":"username not found"}
    
    driver.get(URL+username)

    try:
        team = driver.find_element(By.XPATH, '//*[@id="user-profile"]/div/div[4]/div[1]/div/div/div[5]/div[2]/div/div[3]/a/h1')
        status = driver.find_element(By.XPATH, '//*[@id="user-profile"]/div/div[4]/div[1]/div/div/div[5]/div[2]/div/div[3]/div[1]')
    except:
        return {"response":"user does not have a team"}

    response = team.get_attribute("textContent")

    return {"response":response, "status":status.get_attribute("textContent")}

@app.route("/api/isOnline")
def isOnline():

    username = request.args.get("username")

    if (username == None):
        return {"response":"username not found"}
    
    driver.get(URL+username)
    status = driver.find_element(By.XPATH, '//*[@id="user-profile"]/div/div[2]/div/div[3]/div[1]/span[2]')

    response = status.get_attribute("textContent")

    if (response == "Оффлайн"):
        return {"response":False}
    else:
        return {"response":True}
    
@app.route("/api/isStream")
def isStream():

    username = request.args.get("username")

    if (username == None):
        return {"response":"username not found"}
    
    driver.get(URL+username)
    status = driver.find_element(By.XPATH, '//*[@id="user-profile"]/div/div[2]/div/div[3]/div[1]/span[2]')

    try:
        game = driver.find_element(By.XPATH, '//*[@id="user-profile"]/div/div[2]/div/div[3]/div[1]/span[2]/a')
    except:
        return {"response":False}

    return {"response":True, "game":game.get_attribute("textContent")}

@app.route("/api/isVerified")
def isVerified():

    username = request.args.get("username")

    if (username == None):
        return {"response":"username not found"}
    
    driver.get(URL+username)

    try:
        verified = driver.find_element(By.XPATH, '//*[@id="user-profile"]/div/div[2]/div/div[2]/div/div[1]/div/img')
    except:
        return {"response":False}
    
    return {"response":True}

@app.route("/api/getBestFan")
def getBestFan():

    username = request.args.get("username")

    if (username == None):
        return {"response":"username not found"}
    
    driver.get(URL+username)

    try:
        fan = driver.find_element(By.XPATH, '//*[@id="user-profile"]/div/div[4]/div[1]/div/div/div[3]/ol/li/a/p')
    except:
        return {"response": None}
    
    return {"response": fan.get_attribute("textContent")}

@app.route("/api/getBestDonater")
def getBestDonater():

    username = request.args.get("username")

    if (username == None):
        return {"response":"username not found"}
    
    driver.get(URL+username)

    try:
        donate = driver.find_element(By.XPATH, '//*[@id="user-profile"]/div/div[4]/div[1]/div/div/div[4]/ol/li[1]/a/p[1]')
        value = driver.find_element(By.XPATH, '//*[@id="user-profile"]/div/div[4]/div[1]/div/div/div[4]/ol/li[1]/a/p[2]')
    except:
        return {"response": None}
    
    return {"response": donate.get_attribute("textContent"), "value": value.get_attribute("textContent")}

@app.route("/api/getHotness")
def getHotness():

    username = request.args.get("username")

    if (username == None):
        return {"response":"username not found"}
    
    driver.get(STREAM_URL+username)

    try:
        hotness = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[3]/div/div/div/div[3]/div[1]/div/div/div/span')
    except:
        return {"response": None}
    
    return {"response": hotness.get_attribute("textContent")}

@app.route("/api/getStreamName")
def getStreamName():

    username = request.args.get("username")

    if (username == None):
        return {"response":"username not found"}
    
    driver.get(STREAM_URL+username)

    try:
        hotness = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[3]/div/div/div/div[3]/div[1]/div/h1')
    except:
        return {"response": None}
    
    return {"response": hotness.get_attribute("textContent")}
    
@app.route("/api/isMinecraftHost")
def isMinecraftHost():

    username = request.args.get("username")

    if (username == None):
        return {"response":"username not found"}
    
    driver.get(STREAM_URL+username)

    try:
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div[3]/div/div/div/div[3]/div[1]/div/div/div/span[2]')
    except:
        return {"response": False}
    
    return {"response": True} 


@app.route("/api/bot/toStream")
def toStream():
     
    streamer = request.args.get("streamer")
    token = request.args.get("token")

    if (token is None):
        return {"response": "error"}
    else:
        with open("tokens.json", "r") as file:

            content = json.load(file)

            try:
                for _token in content:

                    users_data = []
                    users_data.append(_token)

            except:
                return {"response": "token not found"}
            else:
                driver.get(STREAM_URL+streamer)
                print(STREAM_URL+streamer)
                print(users_data)

                driver.find_element(By.XPATH, '//*[@id="omlet-bar"]/div[2]/div[2]').click()
                driver.find_element(By.XPATH, '//*[@id="btli"]/a').click()
                driver.find_element(By.XPATH, '//*[@id="omid"]').send_keys(users_data[0][token]["username"])
                driver.find_element(By.XPATH, '//*[@id="pass"]').send_keys(users_data[0][token]["password"])
                driver.find_element(By.XPATH, '//*[@id="login-button"]').click()
                
                driver.find_element(By.XPATH, '//*[@id="root"]/div/div[3]/div/div[2]/div/div/div[2]/div[2]/div[2]').send_keys("test")
                driver.find_element(By.XPATH, '//*[@id="root"]/div/div[3]/div/div[2]/div/div/div[2]/div[3]/div').click()

                return {"response": True}

api.init_app(app)

if (__name__ == "__main__"):
    app.run(debug=False, port=PORT, host=HOST)