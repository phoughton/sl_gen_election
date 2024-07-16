from io import BytesIO
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode


def reset_state():
    st.session_state.selected_rows = None
    df = pd.read_csv("candidate-level-results-general-election-12-12-2019.csv")
    st.session_state['df'] = df


def to_excel(df):
    output = BytesIO()
    df.to_excel(output, index=False, sheet_name='Sheet1')
    output.seek(0)
    return output


def draw_chart(a_df):

    # Grid options for AgGrid
    gb = GridOptionsBuilder.from_dataframe(a_df)
    gb.configure_selection(selection_mode='multiple',
                           use_checkbox=True,
                           suppressRowClickSelection=False)
    gb.configure_grid_options(domLayout='autoHeight',
                              suppressColumnVirtualisation=True)

    gb.configure_grid_options(domLayout='normal',
                              suppressMenuHide=True)

    gb.configure_default_column(groupable=True, value=True,
                                enableRowGroup=True,
                                aggFunc='sum', filter=True)

    grid_opts = gb.build()

    return AgGrid(
        a_df,
        gridOptions=grid_opts,
        enable_enterprise_modules=True,
        fit_columns_on_grid_load=True,
        height=400,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        width='100%'
    )


# Top Level layout setup
st.set_page_config(layout="wide")

selected_rows = None

if 'df' not in st.session_state:
    reset_state()


# Title of the app
st.title("UK General Election 2019")
col_a, col_b = st.columns([0.5, 0.5])
with col_b:
    if st.button('Reset to Defaults'):
        reset_state()
        st.experimental_rerun()


wanted_cols = ['Main party name',
               'Candidate vote count',
               'Majority',
               'Candidate family name',
               'Candidate given name',
               'Constituency name',
               'Country name'
               ]

cols_to_drop = set(st.session_state['df'].columns) - set(wanted_cols)
df_to_show = st.session_state['df'].drop(columns=cols_to_drop)

col1, col2, col3 = st.columns([0.05, 0.9, 0.05])

# Display the table with AgGrid
with col2:
    st.header("Filter or group by columns...")
    response = draw_chart(df_to_show)

    # Display selected row
    selected_rows = response.get('selected_rows', None)
    if selected_rows is not None:
        if len(selected_rows) > 0:
            st.write("You selected:")
            draw_chart(selected_rows)
        
            selected_df = pd.DataFrame(selected_rows)
            excel_data = to_excel(selected_df)
            st.download_button(label='Download Selected Data as Excel',
                               data=excel_data,
                               file_name='selected_data.xlsx',
                               mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
