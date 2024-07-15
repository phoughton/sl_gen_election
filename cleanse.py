import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode


df = pd.read_csv("candidate-level-results-general-election-12-12-2019.csv")


def draw_chart(a_df):

    # Grid options for AgGrid
    gb = GridOptionsBuilder.from_dataframe(a_df)
    gb.configure_selection(selection_mode='multiple', use_checkbox=True, suppressRowClickSelection=True)
    gb.configure_grid_options(domLayout='autoHeight', suppressColumnVirtualisation=True)

    gb.configure_grid_options(domLayout='normal')

    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', filter=True)

    grid_opts = gb.build()

    return AgGrid(
        a_df,
        gridOptions=grid_opts,
        enable_enterprise_modules=True,
        fit_columns_on_grid_load=True,
        height=500,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        width='100%'
    )


print(df.head())

# Title of the app
st.set_page_config(layout="wide")
st.title("UK General Election 2019")

wanted_cols = ['Main party name',
               'Candidate vote count',
               'Majority',
               'Candidate family name',
               'Candidate given name'
               ]

cols_to_drop = set(df.columns) - set(wanted_cols)
df_to_show = df.drop(columns=cols_to_drop)

col1, col2, col3 = st.columns([0.05, 0.9, 0.05])

print(df_to_show.head(10))

# Display the table with AgGrid
with col2:
    st.header("Click to choose a party")
    response = draw_chart(df_to_show)

    # Display selected row
    selected_rows = response.get('selected_rows', None)
    if selected_rows is not None:
        if len(selected_rows) > 0:
            st.write("You selected:")
            draw_chart(selected_rows)
