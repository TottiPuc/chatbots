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
    print(json.dumps(req, indent=4))

    res = makeResponse(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def makeResponse(req):
    result = req.get("queryResult")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    date = parameters.get("date")[0:10]
    date= date +' 06:00:00'
    print("esta date ", date)
    r=requests.get('http://api.openweathermap.org/data/2.5/forecast?q='+city+'&appid=2e4a3d6e494776782a45a4a7039ba9d6')
    json_object=r.json()
    weather=json_object['list']

    for i in range(len(weather)):
        print(weather[i])
        print(weather[i]['dt_txt'])
        if date == weather[i]['dt_txt']:
            condition=weather[i]['weather'][0]['description']
            break
    speech = "El clima en la ciudad de " + city + " para la fecha " + date[0:10] + " a las 6:00 am será " + condition
    return {
        "speech": speech,
        "displayText": speech,
        "source": "apiai-weather-webhook"
    }


if __name__=='__main__':

    port = int(os.getenv('PORT',6000))
    print(f"Inicio de la aplicacion en el puerto {port}")
    app.run(debug=True,port=port, host='0.0.0.0')



