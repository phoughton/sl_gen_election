import streamlit as st
import pandas as pd
import altair as alt
from data_config import csv_files


parties_2_plot = {
    'Conservative': 'blue',
    'Labour': 'red',
    'Liberal Democrat': 'yellow',
    'Green Party': 'green',
    'UK Independence Party': 'purple',
    'Scottish National Party': 'goldenrod',
    'Plaid Cymru': 'brown',
    'Brexit Party': 'aliceblue',
    'Reform UK': 'aquamarine',
    'Other': 'gray'}


def sort_group(df, column):
    return df.sort_values(by=column, ascending=False)


st.set_page_config(layout="wide")

dfs = []
dfs_grouped = []

for year, file in csv_files.items():
    df = pd.read_csv(file)
    df.rename(columns={'General election polling date': 'Polling date'},
              inplace=True)

    dfs.append(df)

    filter = lambda x: 'Other' if x not in list(parties_2_plot.keys()) else x
    df['Main party name'] = df['Main party name'].apply(filter)

    for party in parties_2_plot.keys():
        if party not in df['Main party name'].unique():
            df.loc[len(df)] = {'Main party name': party,
                               'Candidate vote count': 0,
                               'Polling date': df['Polling date'].max()}

    grouped_df = df.groupby('Main party name').agg({
        'Candidate vote count': 'sum',
        'Polling date': 'first'
        }).reset_index()

    sorted_grouped_df = sort_group(grouped_df, 'Candidate vote count')
    dfs_grouped.append(sorted_grouped_df)

combined_df = pd.concat(dfs_grouped)
combined_df.reset_index(drop=True, inplace=True)

filtered_df = combined_df[combined_df['Main party name'].isin(parties_2_plot.keys())]

filtered_df = sort_group(filtered_df, 'Polling date')
starting = min(map(int, list(csv_files.keys())))
ending = max(map(int, list(csv_files.keys())))
date_range = f"{starting} - {ending}"
msg = "Total Candidate Vote Counts," \
    "by UK Political Party in General Elections"
st.title(f'{msg} {date_range}')
st.write('')

color_scheme = alt.Scale(domain=list(parties_2_plot.keys()),
                         range=list(parties_2_plot.values()))

chart = alt.Chart(filtered_df).mark_line().encode(
    x=alt.X('Polling date:T', axis=alt.Axis(format='%Y')),
    y='Candidate vote count:Q',
    color=alt.Color('Main party name:N',
                    scale=color_scheme)
).properties(
    height=600
)

filtered_df_dates = filtered_df['Polling date'].unique()

rules = alt.Chart(pd.DataFrame({
    'Polling date': filtered_df_dates
    })).mark_rule(color='white', strokeDash=[5, 5]).encode(
    x='Polling date:T'
)
specific_date_df = filtered_df[filtered_df['Polling date'].isin([
    '2024-07-04',
    '2019-12-12',
    '2017-06-08',
    '2015-05-07',
    '2010-05-06',])]
specific_date_df = specific_date_df.drop_duplicates(subset='Polling date')

text = alt.Chart(specific_date_df).mark_text(
            align='right',
            fontSize=18,
            dx=98, color='grey',
    ).encode(
        x=alt.X('Polling date:T', axis=alt.Axis(format='%Y-%m-%d')),
        text='Polling date:T')
final_chart = chart + rules + text

st.altair_chart(final_chart, use_container_width=True)

st.write('')
st.markdown("[Source Data](https://electionresults.parliament.uk/general-elections)")
st.markdown("[My GitHub](https://github.com/phoughton)")
