import json, requests

def parse(jsn, var=""):
    if isinstance(jsn,dict):
        for row in jsn:
            parse(jsn[row],var=var+"[\""+row+"\"]")
    elif isinstance(jsn,list):
        for i in range(len(jsn)):
            parse(jsn[i],var=var+"["+str(i)+"]")
    else:
        print(var+"="+str(jsn))
        return var

url = "https://www.jma.go.jp/bosai/forecast/data/forecast/130000.json"
res = requests.get(url)
data = json.loads(res.text)
parse(data,"data")