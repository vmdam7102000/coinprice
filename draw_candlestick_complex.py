
import pandas as pd
from plotly import graph_objs as go
import plotly.io as pio
from plotly.subplots import make_subplots
pio.renderers.default='browser'

def get_candlestick_plot(
        df: pd.DataFrame,
        ma1: int,
        ma2: int
):
    '''
    Create the candlestick chart with two moving avgs + a plot of the volume
    Parameters
    ----------
    df : pd.DataFrame
        The price dataframe
    ma1 : int
        The length of the first moving average (days)
    ma2 : int
        The length of the second moving average (days)
    '''
    
    fig = make_subplots(
        rows = 1,
        cols = 1,
        shared_xaxes = True,
        vertical_spacing = 0.15,
        row_width = [1]
    )

    fig.add_trace(
        go.Candlestick(
            x = df['date'],
            open = df['open'], 
            high = df['high'],
            low = df['low'],
            close = df['close'],
            name = 'biểu đồ nến'
        ),
        row = 1,
        col = 1,
    )
    
    fig.add_trace(
        go.Line(x = df['date'], y = df[f'{ma1}_ma'], name = f'{ma1} SMA'),
        row = 1,
        col = 1,
    )
    
    fig.add_trace(
        go.Line(x = df['date'], y = df[f'{ma2}_ma'], name = f'{ma2} SMA'),
        row = 1,
        col = 1,
    )
    
    fig['layout']['xaxis']['title'] = 'Ngày'
    fig['layout']['yaxis']['title'] = 'Giá'
    
    fig.update_xaxes(
        rangeslider_visible = False,
    )
    
    fig.layout.update(width=1080,height=450,title_text='Biểu đồ nến theo giá và các chỉ số tương quan khác')

    return fig

def get_volume_chart_plot(
        df: pd.DataFrame
):
    '''
    Create the chart correlate with candlestick price chare
    Parameters
    ----------
    df : pd.DataFrame
        The price dataframe
    '''
    
    fig = make_subplots(
        rows = 1,
        cols = 1,
        shared_xaxes = True,
        vertical_spacing = 0.15,
        row_width = [1]
    )

    fig.add_trace(
        go.Bar(x = df['date'], y = df['volume'], name = 'Khối lượng'),
        row = 1,
        col = 1,
    )  

    fig['layout']['xaxis1']['title'] = 'Ngày'
    fig['layout']['yaxis1']['title'] = 'Khối lượng'  

    fig.update_xaxes(
        rangeslider_visible = False,
    )
    
    fig.layout.update(width=950,height=350,title_text='Khối lượng giao dịch')

    return fig

def get_fng_chart_plot(
        df: pd.DataFrame
):
    '''
    Create the chart correlate with candlestick price chare
    Parameters
    ----------
    df : pd.DataFrame
        The price dataframe
    '''
    
    fig = make_subplots(
        rows = 1,
        cols = 1,
        shared_xaxes = True,
        vertical_spacing = 0.15,
        row_width = [1]
    )

    fig.add_trace(
        go.Scatter(x = df['date'], y = df['fng_score'], name = 'FNG'),
        row = 1,
        col = 1,
    )  

    fig['layout']['xaxis1']['title'] = 'Ngày'
    fig['layout']['yaxis1']['title'] = 'FNG'  

    fig.update_xaxes(
        rangeslider_visible = False,
    )
    
    fig.layout.update(width=950,height=350,title_text='Chỉ số FNG')

    return fig

def get_twitter_chart_plot(
        df: pd.DataFrame
):
    '''
    Create the chart correlate with candlestick price chare
    Parameters
    ----------
    df : pd.DataFrame
        The price dataframe
    '''
    
    fig = make_subplots(
        rows = 1,
        cols = 1,
        shared_xaxes = True,
        vertical_spacing = 0.15,
        row_width = [1]
    )

    fig.add_trace(
        go.Bar(x = df['date'], y = df['nlp_compound'], name = 'Chỉ số cảm xúc'),
        row = 1,
        col = 1,
    )  

    fig['layout']['xaxis1']['title'] = 'Ngày'
    fig['layout']['yaxis1']['title'] = 'Chỉ số cảm xúc'  

    fig.update_xaxes(
        rangeslider_visible = False,
    )
    
    fig.layout.update(width=950,height=350,title_text='Chỉ số cảm xúc twitter')

    return fig