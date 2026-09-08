
### Part 1: Import necessary packages #######################################################
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import datetime
import yfinance as yf

### Part 2: Define functions, which are applied by the 3 pages of the web-app ################
def get_stock_data(symbol, period="1y"):
    stock = yf.Ticker(symbol)
    df = stock.history(period=period)
    return df, stock.info

def plot_closing_data(df):
    #st.line_chart(df['Close'], width=0, height=0, use_container_width=True)
    fig = px.line(df, y='Close', orientation='v', title="Closings")
    fig.update_layout(showlegend=False, height=600)
    st.plotly_chart(fig)

def plot_multiple_closing_data(df):
    #st.line_chart(df['Close'], width=0, height=0, use_container_width=True)
    fig = px.line(df, y=df.columns.to_list(), orientation='v', title="Closings of Selected")
    fig.update_layout(showlegend=True, height=600)
    st.plotly_chart(fig)

def plot_volume_data(df):
    #st.bar_chart(df['Volume'], width=0, height=0, use_container_width=True)
    fig = px.bar(df, y='Volume', orientation='v', title="Volumns")
    fig.update_layout(showlegend=False, height=600)
    st.plotly_chart(fig)

def plot_moving_averages(df):
    df['20d MA'] = df['Close'].rolling(window=20).mean()
    df['50d MA'] = df['Close'].rolling(window=50).mean()
    #st.line_chart(df[['Close', '20d MA', '50d MA']], width=0, height=0, use_container_width=True)
    fig = px.line(df, y=['Close','20d MA','50d MA'])
    fig.update_layout(showlegend=True, height=600)
    st.plotly_chart(fig)


### Part 3: Define the functionality of the three different pages - for each page one Python-function #####

###### Page 1: Search Ticker-Symbol of a company
def search_ticker_symbol():
    st.subheader("Search Ticker Symbol")
    query = st.text_input("Enter Company Name", value="NVIDIA").lower()
    foundrows=tickerdf[tickerdf["Name"].str.lower().str.contains(query)]
    #st.dataframe(foundrows[["Symbol","Name","Industry"]])
    st.dataframe(foundrows)


###### Page 2: Analyse stock-development of a single company
def get_single_ticker_data():
    st.subheader("Visualizing Stock Data")

    #symbols,names=get_tickers(tickerfile)
    symbols=tickerdf["Symbol"].to_list()
    names=tickerdf["Name"].to_list()

    # The following replacement is necessary, because tickersymbols of the provided tickerfile
    # slightly vary from tickersymbols required by yahoo-finance
    symbols=[str(s).replace("^","-P") for s in symbols] 

    #nameindex={}
    #for s,n in zip(symbols,names):
    #    nameindex[s]=n

    stock_symbol=st.selectbox("Select one tickersymbol",symbols)

    #st.text("Selected ticker belongs to company %s"%(nameindex[stock_symbol]))

    # Input field for stock symbol
    #stock_symbol = st.text_input("Enter stock symbol", value="NVDA").upper()

    # Fetch stock data
    df, stock_info = get_stock_data(stock_symbol)

    # Display company name and current price
    st.markdown(f"**{stock_info['longName']}**")
    st.markdown(f"**Current Price: ${stock_info['currentPrice']}**")

    # Display stock data charts
    st.subheader("Closing Prices")
    plot_closing_data(df)

    st.subheader("Volume of Trades")
    plot_volume_data(df)

    st.subheader("Closing Price and Moving Averages")
    plot_moving_averages(df)

###### Page 3: Compare Stock development of a set of companies

def select_and_compare():
    selection=tickerdf.copy()
    selection["Relevant"]=[False for i in selection.index]
    st.markdown(f"**Select Companies, which shall be compared:**")
    selecteditor=st.data_editor(selection[["Symbol","Name","Industry","Relevant"]])
    selected = selecteditor.loc[selecteditor["Relevant"]==True]
    st.markdown(f"**Your selection is:**")
    st.dataframe(selected)
    symbollist=selected["Symbol"].to_list()
    FIRST=True
    closings=pd.DataFrame(columns=symbollist)
    for sym in symbollist:
        sym_df,_=get_stock_data(sym, period="1y")
        if FIRST:
            closings=pd.DataFrame(index=sym_df.index, columns=[sym])
            FIRST=False
        closings[sym]=sym_df["Close"].to_list()
    plot_multiple_closing_data(closings)
    st.dataframe(closings)


### Part 4: The main programm

###### a. Read the file, which contains the mapping of company names to ticker-symbols into a pandas datafram
tickerfile="nasdaq_screener.csv"

#def get_tickers(tickerfile):
tickerdf=pd.read_csv(tickerfile)
#    return tickerdf["Symbol"].to_list(), tickerdf["Name"].to_list()

###### b. Define the Navigation in the sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Symbol Search", "Ticker Data","Compare"])

###### c. Depending on the selected page, execute the corresponding function, which defines the functionality of the page
if page == "Symbol Search":
    search_ticker_symbol()
elif page == "Ticker Data":
    get_single_ticker_data()
elif page == "Compare":
    select_and_compare()



