import numpy as np
import pandas as pd
import streamlit as st
from plotly import graph_objs as go
from sqlalchemy import create_engine
from draw_candlestick_complex import *


# Set app config
st.set_page_config(page_title = 'Giá cả tương lai', layout = 'wide', page_icon= '💵' )

# Set app title
st.title('Theo dõi các biểu đồ và dự báo')


### Change sidebar color
st.markdown(
"""
<style>
.sidebar .sidebar-content {
    background-image: linear-gradient(#D6EAF8,#D6EAF8);
    color: black;
     width: 455px;
}
</style>
""",
    unsafe_allow_html=True,
)

### Set bigger font style
st.markdown(
"""
<style>
.big-font {
	fontWeight: bold;
    font-size:22px !important;
}
.block-container {
        margin-top: 0 px;
        margin-right: 0 px;
        margin-left: 0 px;
        margin-bottom: 0 px;
    }
</style>
""", unsafe_allow_html=True)

st.sidebar.subheader("Tùy chọn hiển thị")
cryptos = ["BTC"]

### Select crypto & number of days to predict on
selected_ticker = st.sidebar.selectbox("Lựa chọn mã tiền để theo dõi lịch sử giá và dự đoán giá đóng cửa hôm nay", cryptos)

def get_db_by_crypto():
    if selected_ticker == "BTC":
        trading_table = 'btc_trading_data'
        model_table = 'btc_model_result'
        future_table = 'btc_next24h'
    elif selected_ticker == "ETH":
        trading_table = 'eth_trading_data'
        model_table = 'eth_model_result'
        future_table = 'eth_next24h'
    elif selected_ticker == "USDT":
        trading_table = 'usdt_trading_data'
        model_table = 'usdt_model_result'
        future_table = 'usdt_next24h'
    else:
        trading_table = 'btc_trading_data'
        model_table = 'btc_model_result'
        future_table = 'btc_next24h'
    return trading_table, model_table, future_table

trading_table, model_table,future_table = get_db_by_crypto()

#engine = create_engine('postgresql://postgres:tolavip123@localhost:5432/doan')
engine = create_engine('postgresql://postgres:tolavip123@co.c4gk2383xoxa.ap-northeast-1.rds.amazonaws.com:5432/coindb')

def load_data():
    engine = create_engine('postgresql://postgres:tolavip123@co.c4gk2383xoxa.ap-northeast-1.rds.amazonaws.com:5432/coindb')
    df = pd.read_sql_query('select A.*, B.predict, C.fng_score, D.nlp_compound from %s A left join %s B on A.date = B.date left join fng_index C on A.date = C.date left join twitter_sentiment D on A.date = D.date order by date asc'%(trading_table, model_table),con=engine,parse_dates=["date"])  
    df = df.sort_values(by='date') 
    return df

def load_future_data():
    engine = create_engine('postgresql://postgres:tolavip123@co.c4gk2383xoxa.ap-northeast-1.rds.amazonaws.com:5432/coindb')
    df = pd.read_sql_query('select * from %s'%future_table,con=engine,parse_dates=["date"])  
    df = df.sort_values(by='date',ascending=True) 
    return df


df = load_data()


# Sidebar for chart display setting
st.sidebar.subheader("Thiết lập hiển thị biểu đồ")

days_to_plot = st.sidebar.slider(
    'Số ngày hiển thị', 
    min_value = 1,
    max_value = 365,
    value = 30,
)

ma1 = st.sidebar.number_input(
    'Chu kì đường trung bình trượt 1',
    value = 7,
    min_value = 1,
    max_value = 120,
    step = 1,    
)

ma2 = st.sidebar.number_input(
    'Chu kì đường trung bình trượt 2',
    value = 20,
    min_value = 1,
    max_value = 120,
    step = 1,    
)

    
df_candestick = df[-days_to_plot:]
df_candestick[f'{ma1}_ma'] = df['close'].rolling(ma1).mean()
df_candestick[f'{ma2}_ma'] = df['close'].rolling(ma2).mean()

# Visualization Candlestick chart
st.plotly_chart(
get_candlestick_plot(df_candestick, ma1, ma2),
use_container_width = True,
)

# Visualization trading volume chart
volume = st.sidebar.checkbox("Hiển thị biểu đồ khối lượng giao dịch",0)
if volume:
    df_candestick = df[-days_to_plot:]
    st.plotly_chart(
    get_volume_chart_plot(df_candestick),
    use_container_width = True,
    )

# Visualization FNG chart
fng = st.sidebar.checkbox("Hiển thị biểu đồ chỉ số fng",0)
if fng:
    df_candestick = df[-days_to_plot:]

    st.plotly_chart(
    get_fng_chart_plot(df_candestick),
    use_container_width = True,
    )

# Visualization twitter sentiment chart
twitter = st.sidebar.checkbox("Hiển thị biểu đồ cảm xúc twitter",0)
if twitter:
    df_candestick = df[-days_to_plot:]

    st.plotly_chart(
    get_twitter_chart_plot(df_candestick),
    use_container_width = True,
    )
    

# Visualization final result
def plot_prediction_result():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['date'], y=df['close'], name="giá đóng cửa thực tế", line = dict(color='green',width=1.5)))
    fig.add_trace(go.Scatter(x=df['date'], y=df['predict'], name="giá đóng cửa dự đoán", line = dict(color='blue',width=1.5)))
    fig.layout.update(height=650,title_text='Giá đóng cửa thực tế và dự đoán của model', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig,use_container_width=True)

plot_prediction_result()

futureprice_df = load_future_data()
st.subheader(f'giá đóng cửa dự báo hôm nay là: {futureprice_df["future_price"][futureprice_df.shape[0]-1]:.3f} USD')