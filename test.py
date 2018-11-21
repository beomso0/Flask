
# coding: utf-8

# In[ ]:


from flask import Flask,request,jsonify
app=Flask(__name__)
@app.route('/keyboard')
def keyboard():
    dataSend = {
    "type" : "buttons",
    "buttons":["시작하기"]
    }
    return jsonify(dataSend)

if __name__ == "__main__":
    app.run(host= "0.0.0.0",port = 5000)
