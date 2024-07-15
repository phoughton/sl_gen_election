import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode


df = pd.read_csv("candidate-level-results-general-election-12-12-2019.csv")

# df_gb = df.groupby('Main party name')['Candidate vote count'].sum().reset_index()
# # party_totals.columns = ['Main party name']['All Candidate vote count']
# df_sorted = party_totals.sort_values(by='Candidate vote count',
#                                      ascending=False)
# df_sorted.rename(columns={
#     'Candidate vote count':
#     'All Candidate (for a given party) vote count'},
#                    inplace=True)

# df_renamed = df_sorted

# print("Party Totals")
print(df.head())

# Title of the app
st.set_page_config(layout="wide")
st.title("UK General Election 2019")

# # Creating two columns
# col1, col2 = st.columns(2)

# # Column 1 content
# with col1:
#     st.header("All data")
#     st.write("...in one place")

# # Column 2 content
# with col2:
#     st.header("Explore the data")
#     st.write("...on a web page")


wanted_cols = ['Main party name',
               'Candidate vote count',
               'Majority',
               'Candidate family name',
               'Candidate given name'
               ]

cols_to_drop = set(df.columns) - set(wanted_cols)
df_to_show = df.drop(columns=cols_to_drop)

# Grid options for AgGrid
gb = GridOptionsBuilder.from_dataframe(df_to_show)
gb.configure_selection(selection_mode='single', use_checkbox=True)
gb.configure_grid_options(domLayout='autoHeight', suppressColumnVirtualisation=True)

# for col in wanted_cols:
#     gb.configure_column(col, groupable=True, value=True, enableRowGroup=True, sortable=True, filter=True)
gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', filter=True)

gridOptions = gb.build()
col1, col2, col3 = st.columns([0.05, 0.9, 0.05])

print(df_to_show.head(10))

# Display the table with AgGrid
with col2:
    st.header("Click to choose a party")
    response = AgGrid(
        df_to_show,
        gridOptions=gridOptions,
        enable_enterprise_modules=True,
        fit_columns_on_grid_load=True,
        update_mode=GridUpdateMode.NO_UPDATE,
        width='100%'
    )

    # Display selected row
    if response['selected_rows']:
        st.write("You selected:")
        st.json(response['selected_rows'][0])
