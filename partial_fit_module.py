# FETCH THE MODEL
import pickle
import requests
import io
import streamlit as st

#LIST OF MODELS TO UPDATE
tickers = ['AAPL','GOOG','MSFT','TSLA','IBM','ACN']


#UPDATING ALL MODELS ONE BY ONE
for ticker in tickers:
    #LOADING THE MODEL FROM GITHUB
    repo = "Testing"
    url = "https://github.com/darshi24/"+repo+"/blob/main/"+ticker+".p?raw=true"
    byte_content = requests.get(url).content
    model = io.BytesIO(byte_content)
    reg = pickle.load(model)

    #FETCHING NEW DATA TO FIT
    from sklearn.preprocessing import MinMaxScaler
    import yfinance as yf
    yf_data = yf.download(tickers=ticker, period='1d', interval='1m')
    yf_data.reset_index(inplace=True,drop=False)
    X = yf_data[['Open', 'High', 'Low', 'Volume']]
    y = yf_data[['Close']]

    scaler = MinMaxScaler()
    scaler = scaler.fit(X)
    X_scaled = scaler.transform(X)

    scaler = MinMaxScaler()
    scaler = scaler.fit(y)
    y_scaled = scaler.transform(y)

    #APPLYING PARTIAL FIT METHOD
    reg.partial_fit(X_scaled,y_scaled)

    #UPDATING THE MODEL ON GITHUB

    from github import Github
    pickled_model = pickle.dumps(reg)
    access_token = "***************************************"
    g = Github(access_token)
    user = g.get_user()
    repo = user.get_repo('test')
    contents = repo.get_contents(ticker+".p")

    import datetime
    repo.update_file(ticker+".p","commit on "+datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),pickled_model, contents.sha)
    st.write("Updated "+ticker+" model")
