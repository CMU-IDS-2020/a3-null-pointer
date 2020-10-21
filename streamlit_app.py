import streamlit as st
import pandas as pd
import altair as alt

st.title("Let's analyze some Donald Trump's Tweets!")

@st.cache  # add caching so we load the data only once
def load_data():
    # Load the preprocessed data named 'processed_data.csv' and 'word_count.csv'
    return pd.read_csv('month_with_wordcount.csv')


df = load_data()


df_filtered = df.copy()
df_filtered.sentiment = df_filtered.sentiment.map(lambda x: round(x,2))

if st.checkbox('Show Raw Data'):
    st.write(df_filtered)

st.write("Let look at how Trump's sentiment changes over time from 2009-05 to 2020-06")
st.write("Sentiment is a value between -1 and 1, where -1 stand for 100% negative and 1 stands for 100% positive")


brush = alt.selection_interval(encodings = ['x'])

chart = alt.Chart(df_filtered).mark_circle(size=50).encode(
    x = alt.X('date:T', scale=alt.Scale(zero=False)),
    y = alt.Y('sentiment:Q'),
    color = alt.Color('sentiment:Q'),
    tooltip = ['date:T','sentiment:Q']
).properties(
    width=800, height = 600
)

chart = chart.encode(
    color = alt.condition(brush, 'sentiment:Q', alt.value('lightgray'))
).add_selection(brush)


st.write(chart)
# st.write("Hmm 🤔, is there some correlation between body mass and flipper length? Let's make a scatterplot with [Altair](https://altair-viz.github.io/) to find.")
#
# chart = alt.Chart(df).mark_point().encode(
#     x=alt.X("body_mass_g", scale=alt.Scale(zero=False)),
#     y=alt.Y("flipper_length_mm", scale=alt.Scale(zero=False)),
#     color=alt.Y("species")
# ).properties(
#     width=600, height=400
# ).interactive()
#
# st.write(chart)
