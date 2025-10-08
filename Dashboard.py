
### Library
import pandas as pd
import yfinance as yf
import streamlit as st
import altair as alt

### Raw_data
# Calculate the date one year ago from today
end_date = pd.Timestamp.today()
start_date = end_date - pd.DateOffset(years=1)

# Define a function to fetch data
def fetch_data(ticker):
    data = yf.download(ticker, start=start_date, end=end_date)
    data.reset_index(inplace=True)
    return data
# Fetch data for NASDAQ and S&P 500
nasdaq_data = fetch_data('^IXIC')
sp500_data = fetch_data('^GSPC')

# Function to create moving average
def add_moving_averages(data):
    data['MA_5'] = data['Close'].rolling(window=5).mean()
    data['MA_20'] = data['Close'].rolling(window=20).mean()
    data['MA_40'] = data['Close'].rolling(window=40).mean()
    data['MA_60'] = data['Close'].rolling(window=60).mean()
    return data

nasdaq_data = add_moving_averages(nasdaq_data)
sp500_data = add_moving_averages(sp500_data)

# Function to create candlestick chart with moving averages
def create_candlestick_chart(data, title):
    base = alt.Chart(data).encode(
        alt.X('Date:T', title='Date')
    )

    open_close_color = alt.condition(
        "datum.Open <= datum.Close",
        alt.value("#FF0000"),  # Red for increasing
        alt.value("#0000FF")   # Blue for decreasing
    )

    rule = base.mark_rule().encode(
        alt.Y('Low:Q', title='Price', scale=alt.Scale(zero=False)),
        alt.Y2('High:Q'),
        color=open_close_color
    )

    bar = base.mark_bar().encode(
        alt.Y('Open:Q'),
        alt.Y2('Close:Q'),
        color=open_close_color
    )

    ma5 = base.mark_line(color='green').encode(
        alt.Y('MA_5:Q', title='Price')
    )

    ma20 = base.mark_line(color='orange').encode(
        alt.Y('MA_20:Q', title='Price')
    )

    ma40 = base.mark_line(color='purple').encode(
        alt.Y('MA_40:Q', title='Price')
    )

    ma60 = base.mark_line(color='brown').encode(
        alt.Y('MA_60:Q', title='Price')
    )

    chart = (rule + bar + ma5 + ma20 + ma40 + ma60).properties(
        width=800,
        height=400,
        title=title
    )

    return chart


### Settings
st.set_page_config(page_title="DK Portfolio")
st.title("📈 Portfolio Dashboard (DK)")
# 사이드바
with st.sidebar:
    st.sidebar.header("Settings")
    # Slider for selecting time period in months
    months = st.slider("Select Time Period (months)", 1, 12, 4)
    
# Function to filter data based on the selected period
def filter_data(data, months):
    start_filter_date = end_date - pd.DateOffset(months=months)
    filtered_data = data[data["Date"] >= start_filter_date.strftime("%Y-%m-%d")]
    return filtered_data

nasdaq_data_filtered = filter_data(nasdaq_data, months)
sp500_data_filtered = filter_data(sp500_data, months)

# 탭 생성
tab1, = st.tabs(["📈 차트"])

with tab1:
    st.header("차트")

   # Create and display NASDAQ chart
    st.subheader('NASDAQ Index')
    nasdaq_chart = create_candlestick_chart(nasdaq_data_filtered, 'NASDAQ Index')
    st.altair_chart(nasdaq_chart, use_container_width=True)

    # Create and display S&P 500 chart
    st.subheader('S&P 500 Index')
    sp500_chart = create_candlestick_chart(sp500_data_filtered, 'S&P 500 Index')
    st.altair_chart(sp500_chart, use_container_width=True)



# # 탭 1: 개요
# with tab1:
#     # st.subheader("시장 개요")
    
#     # col1, col2 = st.columns(2)
    
#     # with col1:
#     #     st.metric(
#     #         label="NASDAQ Composite",
#     #         value=f"{nasdaq_data['Close'].iloc[-1]:,.2f}",
#     #         delta=f"{((nasdaq_data['Close'].iloc[-1] / nasdaq_data['Close'].iloc[0] - 1) * 100):.2f}%"
#     #     )
        
#     # with col2:
#     #     st.metric(
#     #         label="S&P 500",
#     #         value=f"{sp500_data['Close'].iloc[-1]:,.2f}",
#     #         delta=f"{((sp500_data['Close'].iloc[-1] / sp500_data['Close'].iloc[0] - 1) * 100):.2f}%"
#     #     )
    
#     # st.info(f"📅 분석 기간: {nasdaq_data['Date'].iloc[0].strftime('%Y-%m-%d')} ~ {nasdaq_data['Date'].iloc[-1].strftime('%Y-%m-%d')}")

# # 탭 2: 차트
# with tab2:
#     # st.subheader("가격 추이")
    
#     # fig = go.Figure()
#     # fig.add_trace(go.Scatter(
#     #     x=nasdaq_data['Date'], 
#     #     y=nasdaq_data['Close'],
#     #     mode='lines', 
#     #     name='NASDAQ',
#     #     line=dict(color='#00D9FF', width=2)
#     # ))
#     # fig.add_trace(go.Scatter(
#     #     x=sp500_data['Date'], 
#     #     y=sp500_data['Close'],
#     #     mode='lines', 
#     #     name='S&P 500',
#     #     line=dict(color='#FF6B6B', width=2)
#     # ))
    
#     # fig.update_layout(
#     #     xaxis_title="날짜",
#     #     yaxis_title="가격",
#     #     hovermode='x unified',
#     #     height=500,
#     #     template='plotly_dark'
#     # )
    
#     # st.plotly_chart(fig, use_container_width=True)
    
#     # # 거래량 차트
#     # st.subheader("거래량")
#     # fig2 = go.Figure()
#     # fig2.add_trace(go.Bar(
#     #     x=nasdaq_data['Date'],
#     #     y=nasdaq_data['Volume'],
#     #     name='NASDAQ 거래량',
#     #     marker_color='#00D9FF'
#     # ))
#     # fig2.update_layout(height=300, template='plotly_dark')
#     # st.plotly_chart(fig2, use_container_width=True)


# # 탭 3: 데이터 테이블
# with tab3:
#     # col1, col2 = st.columns(2)
    
#     # with col1:
#     #     st.subheader("NASDAQ 데이터")
#     #     st.dataframe(nasdaq_data, use_container_width=True, height=400)
        
#     # with col2:
#     #     st.subheader("S&P 500 데이터")
#     #     st.dataframe(sp500_data, use_container_width=True, height=400)

# # 탭 4: 비교 분석
# with tab4:
#     # st.subheader("성과 비교")
    
#     # # 수익률 계산
#     # nasdaq_return = (nasdaq_data['Close'].iloc[-1] / nasdaq_data['Close'].iloc[0] - 1) * 100
#     # sp500_return = (sp500_data['Close'].iloc[-1] / sp500_data['Close'].iloc[0] - 1) * 100
    
#     # # 변동성 계산
#     # nasdaq_volatility = nasdaq_data['Close'].pct_change().std() * 100
#     # sp500_volatility = sp500_data['Close'].pct_change().std() * 100
    
#     # col1, col2, col3, col4 = st.columns(4)
    
#     # with col1:
#     #     st.metric("NASDAQ 수익률", f"{nasdaq_return:.2f}%")
#     # with col2:
#     #     st.metric("S&P 500 수익률", f"{sp500_return:.2f}%")
#     # with col3:
#     #     st.metric("NASDAQ 변동성", f"{nasdaq_volatility:.2f}%")
#     # with col4:
#     #     st.metric("S&P 500 변동성", f"{sp500_volatility:.2f}%")
    
#     # # 정규화된 수익률 비교
#     # st.subheader("정규화된 수익률 비교 (시작점=100)")
    
#     # nasdaq_normalized = (nasdaq_data['Close'] / nasdaq_data['Close'].iloc[0]) * 100
#     # sp500_normalized = (sp500_data['Close'] / sp500_data['Close'].iloc[0]) * 100
    
#     # fig3 = go.Figure()
#     # fig3.add_trace(go.Scatter(
#     #     x=nasdaq_data['Date'],
#     #     y=nasdaq_normalized,
#     #     mode='lines',
#     #     name='NASDAQ',
#     #     line=dict(color='#00D9FF', width=2)
#     # ))
#     # fig3.add_trace(go.Scatter(
#     #     x=sp500_data['Date'],
#     #     y=sp500_normalized,
#     #     mode='lines',
#     #     name='S&P 500',
#     #     line=dict(color='#FF6B6B', width=2)
#     # ))
    
#     # fig3.update_layout(
#     #     xaxis_title="날짜",
#     #     yaxis_title="정규화된 가격 (시작=100)",
#     #     hovermode='x unified',
#     #     height=400,
#     #     template='plotly_dark'
#     # )
    
#     # st.plotly_chart(fig3, use_container_width=True)












# # 데이터 로드
# @st.cache_data
# def fetch_data(ticker, years):
#     end_date = pd.Timestamp.today()
#     start_date = end_date - pd.DateOffset(years=years)
#     data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True, progress=False)
#     data.reset_index(inplace=True)
#     return data

# with st.spinner('데이터 로딩 중...'):
#     nasdaq_data = fetch_data('^IXIC', years)
#     sp500_data = fetch_data('^GSPC', years)


