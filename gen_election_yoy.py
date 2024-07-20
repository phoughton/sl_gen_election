import streamlit as st
import pandas as pd
import altair as alt


csv_files = {
    '2015': 'data/candidate-level-results-general-election-07-05-2015.csv',
    '2017': 'data/candidate-level-results-general-election-08-06-2017.csv',
    '2019': 'data/candidate-level-results-general-election-12-12-2019.csv',
    '2024': 'data/candidate-level-results-general-election-04-07-2024.csv'
}

parties_to_plot_all = {
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

    df['Main party name'] = df['Main party name'].apply(lambda x: 'Other' if x not in list(parties_to_plot_all.keys()) else x)

    for party in parties_to_plot_all.keys():
        if party not in df['Main party name'].unique():
            df.loc[len(df)] = {'Main party name': party, 'Candidate vote count': 0, 'Polling date': df['Polling date'].max()}

    grouped_df = df.groupby('Main party name').agg({
        'Candidate vote count': 'sum',
        'Polling date': 'first'
        }).reset_index()

    sorted_grouped_df = sort_group(grouped_df, 'Candidate vote count')
    dfs_grouped.append(sorted_grouped_df)

combined_df = pd.concat(dfs_grouped)
combined_df.reset_index(drop=True, inplace=True)

filtered_df = combined_df[combined_df['Main party name'].isin(parties_to_plot_all.keys())]

filtered_df = sort_group(filtered_df, 'Polling date')
st.title('Time Series Line Chart of Total Candidate Vote Counts, by Party')

color_scheme = alt.Scale(domain=list(parties_to_plot_all.keys()),
                         range=list(parties_to_plot_all.values()))

chart = alt.Chart(filtered_df).mark_line().encode(
    x=alt.X('Polling date:T', axis=alt.Axis(format='%Y-%m-%d')),
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

final_chart = chart + rules

st.altair_chart(final_chart, use_container_width=True)
