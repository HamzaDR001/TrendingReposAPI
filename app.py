import requests
import datetime
import dateutil.relativedelta
from flask import Flask, json, jsonify
from datetime import date
from dateutil.relativedelta import relativedelta

app = Flask(__name__)

@app.route("/")
def index():
    #calclating the date: 30 days before today
    reposDate = (date.today() - relativedelta(days=30)).strftime("%Y-%m-%d")
    #getting the data from Gitub and converting it into a dictionary (item)
    data=requests.get('https://api.github.com/search/repositories?q=created:>'+reposDate+'&sort=stars&order=desc&per_page=100').content
    items=json.loads(data)['items']
    #re-orgonasing the data and keeping count of how many repos per langague 
    res = {}
    for item in items:
        if item['language'] is None:
            #some repos do not have a specifiaque langague, let's not forget about them ^_^ 
            item['language'] = 'Not_Specified'
        if item['language'] not in res:
            #first time dealing with this langague ==> prepare a Dics structure
            res[item['language']] = {}
            res[item['language']]['language'] = item['language']
            res[item['language']]['repositories'] = []
            res[item['language']]['count'] = 0
        res[item['language']]['repositories'].append(item)
        res[item['language']]['count'] = len(res[item['language']]['repositories'])
    
    #reformating the result for easy consumption by end user
    result = []
    for item in res:
        result.append(res[item])

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)