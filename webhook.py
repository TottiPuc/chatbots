import json
import os
import requests

from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print(json.dumps(req, ident=4))

    res = makeResponse(req)
    res = json.dumps(res, ident=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def makeResponse(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    date = parameters.get("date")
    r=requests.get('api.openweathermap.org/data/2.5/forecast?q='+city+'&appid=2e4a3d6e494776782a45a4a7039ba9d6')
    json_object=r.json()
    weather=json_object['list']
    for i in range(len(weather)):
        if date in weather[i]['dt_txt']:
            condition=weather[i]['weather'][0]['description']
            break
    speech = "El climar para" + city + "para la fecha " + date + " is "+condition
    return {
        "speech": speech,
        "displayText": speech,
        "source": "apiai-weather-webhook"
    }


if __name__=='__main__':

    port = int(os.getenv('PORT',6000))
    print(f"Inicio de la aplicacion en el puerto {port}")
    app.run(debug=False,port=port,host='0.0.0.0')



