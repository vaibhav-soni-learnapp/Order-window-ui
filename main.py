import streamlit as st
import pandas as pd

def fix_df(df):
    """ Fix database date and time column"""
    df.order_date = pd.to_datetime(df.order_date)
    df.order_time = pd.to_datetime(df.order_time)
    return df

st.title('Trading Book')

tab1,tab2,tab3 = st.tabs(['New Entry','Trade Log','Filter'])

with tab1:
        st.subheader(':green[New Entry]')
        col1,col2,col3 = st.columns(3)
        with col2:
            date = st.date_input('Date')
            time = st.time_input('Time')
        with col1:
            symb = st.text_input('Symbol',).upper()
            order = st.selectbox('Order',options=['BUY','SELL'])
        with col3:
            position = st.number_input('Position')
            price = st.number_input('Price')
            #save button
        st.button('Add Trade') 

with st.spinner('Loading Tradeing Logs'):
    logb = pd.DataFrame()
    try:
        logb = pd.read_csv('base/TradeBook.csv')
        logb= fix_df(logb)
        st.toast('Data Successfully Loaded ',icon='✅')
        
    except:
        file = st.file_uploader(label='Upload Trade Book')
        st.toast('Data Successfully Loaded ',icon='✅')

with tab2:
        st.subheader(':green[Trade Book]')
        if len(logb)>0:
            logb = st.data_editor(logb.sort_values('order_date',ascending=False),
                              hide_index=True,
                              column_config={
                                'trade_id': st.column_config.NumberColumn(
                                    'ID',
                                    format="%d",
                                    width='small'
                                ),
                                'symb':st.column_config.TextColumn(
                                    'Ticker',
                                    width='small',

                                ),
                                'value-usd': st.column_config.NumberColumn(
                                    format="$%.2f"
                                ),
                                'order': st.column_config.SelectboxColumn(
                                    options=['BUY','SELL'],
                                    width='small',
                                ),
                                
                                'order_date':st.column_config.DateColumn(
                                    'Date',
                                    width='small',
                                    format='DD-MM-yyyy'
                                ),
                                'order_time':st.column_config.TimeColumn(
                                    'Time',
                                    width='small',
                                    format='HH:MM',

                                ),
                                'state': st.column_config.SelectboxColumn(
                                    options=['open','closed'],
                                    width='small'
                                ),

                            },use_container_width=True)
        elif file is not None:
             file = pd.read_csv(file)
             file = fix_df(file)
             logb = st.data_editor(file.sort_values('order_date',ascending=False),
                              hide_index=True,
                              column_config={
                                'trade_id': st.column_config.NumberColumn(
                                    'ID',
                                    format="%d",
                                    width='small'
                                ),
                                'symb':st.column_config.TextColumn(
                                    'Ticker',
                                    width='small',

                                ),
                                'value-usd': st.column_config.NumberColumn(
                                    format="$%.2f"
                                ),
                                'order': st.column_config.SelectboxColumn(
                                    options=['BUY','SELL'],
                                    width='small',
                                ),
                                
                                'order_date':st.column_config.DateColumn(
                                    'Date',
                                    width='small',
                                    format='DD-MM-yyyy'
                                ),
                                'order_time':st.column_config.TimeColumn(
                                    'Time',
                                    width='small',
                                    format='HH:MM',

                                ),
                                'state': st.column_config.SelectboxColumn(
                                    options=['open','closed'],
                                    width='small'
                                ),
                            },use_container_width=True)
             
#FILTER
with tab3:
    def filter_ui():
        """
        Draw Filter user elements in the side bar

        Returns":
            choice [str]: stores the user choice of filter type 
            filter [str]: stores choice parameter
        
        """  
        filter = ''
        
        with st.container():
            # st.subheader(':green[Filter Trades]')
            col1,col2= st.columns(2)
            with col1:
                choice= st.selectbox('Filter Trades By',options=[
                    'Ticker','Trade id','Order Type','Date','Order State'
                ])
            with col2:
                if choice == 'Ticker':
                    # Enter Ticker
                    filter = st.text_input('Ticker',max_chars=4,placeholder='Symbol')
                elif choice == 'Trade id':
                    filter = str(st.number_input('Trade ID',min_value=0,key='filter id'))
                    
                elif choice == 'Date':
                    filter = str(st.date_input('Date',key='filter date'))
                elif choice == 'Order Type':
                    filter = st.selectbox('Select state',options=['All','Buy','Sell'])
                elif choice == 'Order State':
                    filter = st.selectbox('Select state',options=['All','Open','Closed'])
            
            return choice, filter
    
    choice,filter = filter_ui()
    #merge df
    st.button('Show Results')
    st.divider()
    st.subheader(':green[Filter Results]')
