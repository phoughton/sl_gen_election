from io import BytesIO
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode


csv_files = {
    '2015': 'data/candidate-level-results-general-election-07-05-2015.csv',
    '2017': 'data/candidate-level-results-general-election-08-06-2017.csv',
    '2019': 'data/candidate-level-results-general-election-12-12-2019.csv',
    '2024': 'data/candidate-level-results-general-election-04-07-2024.csv'
}


def reset_state():
    st.session_state.selected_rows = None
    local_df = pd.read_csv(st.session_state['selected_file'])
    local_df.rename(columns={'General election polling date': 'Polling date'},
                    inplace=True)
    st.session_state['df'] = local_df


def to_excel(df):
    output = BytesIO()
    df.to_excel(output, index=False, sheet_name='Election_Data')
    output.seek(0)
    return output


def draw_chart(a_df):

    gb = GridOptionsBuilder.from_dataframe(a_df)
    gb.configure_selection(selection_mode='multiple',
                           use_checkbox=True,
                           suppressRowClickSelection=False)
    gb.configure_grid_options(suppressColumnVirtualisation=True,
                              domLayout='normal',
                              suppressMenuHide=True,
                              rowHeight="40px")

    gb.configure_default_column(groupable=True, value=True,
                                enableRowGroup=True,
                                aggFunc='sum', filter=True)
    grid_opts = gb.build()

    return AgGrid(
        a_df,
        gridOptions=grid_opts,
        enable_enterprise_modules=True,
        fit_columns_on_grid_load=True,
        height=350,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        width='100%'
    )


# Top Level layout setup
st.set_page_config(layout="wide")


left_border, col_a, col_b, right_border = st.columns([0.05, 0.55, 0.35, 0.05])
with col_a:
    st.title('General Election Results, All Candidates')
    st.write('This app allows you to filter and group the data from the UK General Election results.')
    st.write('Select a file from the dropdown (right) and then filter or group the data.')
    st.write('Click on a row to see the selected data in a separate table below.')
with col_b:
    st.write('')
    st.write('')
    years = list(csv_files.keys())
    selected_file_label = st.selectbox(
        'Select CSV File:',
        years,
        index=years.index(max(years)))
    if st.button('Reset to Defaults'):
        reset_state()
        st.experimental_rerun()
    st.markdown("[Source Data](https://electionresults.parliament.uk/general-elections)")

selected_rows = None

if 'selected_file' not in st.session_state:
    st.session_state['selected_file'] = csv_files[selected_file_label]
    reset_state()

if st.session_state['selected_file'] != csv_files[selected_file_label]:
    st.session_state['selected_file'] = csv_files[selected_file_label]
    reset_state()

if 'df' not in st.session_state:
    reset_state()

wanted_cols = ['Main party name',
               'Candidate vote count',
               'Majority',
               'Candidate family name',
               'Candidate given name',
               'Constituency name',
               'Country name',
               'Polling date'
               ]

cols_to_drop = set(st.session_state['df'].columns) - set(wanted_cols)
df_to_show = st.session_state['df'].drop(columns=cols_to_drop)

col1, col2, col3 = st.columns([0.05, 0.9, 0.05])

with col2:
    st.header("Select, Filter or group by columns...")
    response = draw_chart(df_to_show)

    # Display selected rows
    selected_rows = response.get('selected_rows', None)
    if selected_rows is not None:
        st.write("You selected:")
        draw_chart(selected_rows)

        selected_df = pd.DataFrame(selected_rows)
        excel_data = to_excel(selected_df)
        mime = 'application/' +\
            'vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        st.download_button(label='Download Selected Data as Excel',
                           data=excel_data,
                           file_name='selected_data.xlsx',
                           mime=mime)
