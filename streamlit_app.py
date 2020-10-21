import streamlit as st
import pandas as pd
import altair as alt

st.title("Let's analyze some Donald Trump's Tweets!")

@st.cache  # add caching so we load the data only once
def load_data():
    # Load the preprocessed data named 'processed_data.csv' and 'word_count.csv'
    return pd.read_csv('proceed_data_by_month.csv')


df = load_data()


df_filtered = df.copy()
df_filtered.sentiment = df_filtered.sentiment.map(lambda x: round(x,2))

if st.checkbox('Show Raw Data'):
    st.write(df_filtered)

st.write("Let look at how Trump's sentiment changes over time from 2009-05 to 2020-06")
st.write("Sentiment is a value between -1 and 1, where -1 stand for 100% negative and 1 stands for 100% positive")


brush = alt.selection_interval(encodings = ['x'])
chart2 = alt.Chart(df_filtered).mark_bar().encode(
    x = alt.X('date:T'),
    y = alt.Y('sentiment:Q'),
    tooltip= ['date:T','sentiment:Q']
).properties(
    width=800, height = 400
)
chart2 = chart2.encode(
    color = alt.condition(brush, 'favorites:Q', alt.value('lightgray'))
).add_selection(brush)

chart = alt.Chart(df_filtered).mark_circle().encode(
    x = alt.X('date:T'),
    y = alt.Y('sentiment:Q'),
    color = alt.condition(alt.datum.sentiment>.15 , alt.value('red'), alt.value('blue')),
    size = alt.Size('retweets:Q', scale=alt.Scale(range=[20,200])),
    tooltip = ['date:T','sentiment:Q','retweets:Q','favorites:Q']
).properties(
    width=800, height = 400
).transform_filter(brush)





st.write(chart2 & chart)

