import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import plotly.io as pio
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import datetime as dt

st.set_page_config(layout='wide')

# Read in the data and format
df = pd.read_csv('data/all_bulls_new.csv')
print(df.count())

pio.templates.default = "plotly_dark"

del df['Unnamed: 0']
# Reorder columns
df = df.reindex(
    columns=['Name', 'DOB', 'Days_Old', 'bull_score', 'REA', 'rea_score', 'REA_per_100', 'rea_ratio_score', 'Weight',
             'ADG', 'adg_score', '%IMF', 'imf_score', 'Backfat', 'Scrotal', 'scrotal_cm_per_day', 'Class', 'Meas_Year'])

# Setup Main Page


st.header('Bull Analysis Dashboard')
st.markdown('National Western Stock Show(NWSS) - American Highland Cattle Association(AHCA) Show Bulls')

# Set up tabs

tab1, tab2, tab3 = st.tabs(['NWSS Bull Background Information & Trends      ',
                            'NWSS Bull Division Analysis       ',
                            'NWSS Selected Bull Analysis'])

with tab1:
    st.subheader("Background Information")

    notes1 = "<h4>Data</h4><ul> " \
             "<li>All data employed in the analysis was obtained from results posted publicly online on the American Highland Cattle " \
             "Association (AHCA) website: (""http://www.highlandcattleusa.org/)</li>" \
             "<li>Unable to read year 2017</li> <li>Data – 255 Bulls Compared</li><li>2021 was cancelled due to COVID</li>" \
             "<li>Each year's measurements document was converted to .csv and read into a JUPYTER notebook</li>" \
             "<li>2016 – 2025 with the above exceptions</li><li>Only bulls with all measurements were included in " \
             "the analysis</li><li>Weight only, Scratch, etc were dropped</li></ul>"
    notes2 = "<h4>Bulls Sorted into Age Groups based on NWSS Division Ages</h4><ul><li>A quick observation of the data in " \
             "the spreadsheets quickly reveals that comparing bulls across ages makes no sense. </li><li>For this analysis, " \
             "bulls were sorted by NWSS Division. In order to do this, the age in " \
             "days (Days_Old) was obtained based on the difference in days between the NWSS measurement date for each " \
             "year's show and the Date of Birth (DOB).</li>" \
             "<li>A 50 pound constant was subtracted from the Measurement Weight since birth weights are not reported. " \
             "This impacted ADG, which was calculated by dividing the reported NWSS weight measurement by the newly " \
             "created 'Days_Old' metric.</li></ul>"
    notes3 = "<h4>NWSS Divisions</h4>" \
             " <ul><li>Intermediate Bull Calf (1 May – 31 Dec) --> (DOB Year = Show year - 1)" \
             "<li>Junior Bull Calf (1 Jan – 30 Apr)   -->              (DOB Year = Show year - 1)</li>" \
             "<li>Senior Bull Calf (1 Sep – 31 Dec)  -->            (DOB Year = Show year - 2)</li>" \
             "<li>Intermediate Yearling Bull (1 May – 31 Aug) --> (DOB Year = Show year -  2)</li>" \
             "<li>Junior Yearling Bull (1 Jan – 30 Apr)    -->  (DOB Year = Show year - 2)</li>" \
             "<li>Senior Bull (1 Jan – 31 Dec)            -->             (DOB Year = Show year - >2)</li></ul><br><br>"

    correlation_observations = "Bull categories were correlated against each other to evaluate if there were " \
                               "relationships between the various metrics. The only correlations noted here " \
                               "seem to be obvious growth related age(age v weight, age v REA size, age v scrotal size, " \
                               "weight v REA size, etc)."

    colnt1, colnt2, colnt3 = st.columns(3, gap='large')

    with colnt1:
        st.markdown(notes1, unsafe_allow_html=True)
    with colnt2:
        st.markdown(notes2, unsafe_allow_html=True)
    with colnt3:
        st.markdown(notes3, unsafe_allow_html=True)

    st.divider()

    st.subheader('All Bulls - Summaries by NWSS Division (Count, Age (Days) & Weights)')

    div_list = df['Class'].unique()

    hist_plot = px.histogram(data_frame=df,
                             x='Class',
                             color='Class',
                             title='Bull Count by NWSS Division',
                             width=1800
                             )
    st.plotly_chart(hist_plot)

    col_b, col_c = st.columns(2, gap='small')

    checkbox1 = st.checkbox(label='Show Age Trend Chart by Division')
    if checkbox1:
        box_plot = px.box(data_frame=df,
                          y='Days_Old',
                          x='Class',
                          color='Class',
                          title='Bull Age (Days) by NWSS Division ')
        st.plotly_chart(box_plot)

    checkbox2 = st.checkbox(label='Show Bull Weight Trends by Division')
    if checkbox2:
        box_plot = px.box(data_frame=df,
                          y='Weight',
                          x='Class',
                          color='Class',
                          title='Bull Weights by NWSS Division ')
        st.plotly_chart(box_plot)

    checkbox3 = st.checkbox(label='Show %IMF Trends by Division')
    if checkbox3:
        box_plot = px.box(data_frame=df,
                          y='%IMF',
                          x='Class',
                          color='Class',
                          title='%IMF by NWSS Division ')
        st.plotly_chart(box_plot)
    checkbox4 = st.checkbox(label='Show REA per 100 trends by Division')
    if checkbox4:
        box_plot = px.box(data_frame=df,
                          y='REA_per_100',
                          x='Class',
                          color='Class',
                          title='Bull REA per 100 by NWSS Division ')
        st.plotly_chart(box_plot)

    checkbox5 = st.checkbox(label='Show REA Size trends by Division')
    if checkbox5:
        box_plot = px.box(data_frame=df,
                          y='REA',
                          x='Class',
                          color='Class',
                          title='REA Size by NWSS Division ')
        st.plotly_chart(box_plot)

    checkbox6 = st.checkbox(label='Show Scrotal trends by Division')
    if checkbox6:
        box_plot = px.box(data_frame=df,
                          y='Scrotal',
                          x='Class',
                          color='Class',
                          title='Bull Scrotal by NWSS Division ')
        st.plotly_chart(box_plot)

    checkbox7 = st.checkbox(label='Show Backfat trends by Division')
    if checkbox7:
        box_plot = px.box(data_frame=df,
                          y='Backfat',
                          x='Class',
                          color='Class',
                          title='Backfat by NWSS Division ')
        st.plotly_chart(box_plot)

    checkbox8 = st.checkbox(label='Show ADG trends by Division')
    if checkbox8:
        box_plot = px.box(data_frame=df,
                          y='ADG',
                          x='Class',
                          color='Class',
                          title='Bull ADG by NWSS Division ')
        st.plotly_chart(box_plot)

    st.divider()

with tab2:
    st.subheader('AHCA NWSS Bull Division Selection')

    dropdown_1 = st.selectbox(label=':green[Select NWSS Bull Division]',
                              key='dd1',
                              options=div_list,
                              help='Select Bull Division for Analysis')
    df_plot = df[df['Class'] == dropdown_1]
    df_plot = df_plot.reset_index(drop=True)
    df_plot.index += 1

    st.text('Average Values for Selected Bull Division')

    # col1, col7 = st.columns([1,1], gap='small')
    col1, col7, col2, col3, col4, col5, col6 = st.columns(7, gap='small')

    col1.caption(f'Average Age(Days Old)')
    text = df_plot['Days_Old'].mean().round(2)
    col1.subheader(f':violet[{text}]')

    col2.caption('Average Weight')
    text2 = df_plot['Weight'].mean().round(2)
    col2.subheader(f':violet[{text2}]')

    col3.caption('Average REA')
    text3 = df_plot['REA'].mean().round(2)
    col3.subheader(f':violet[{text3}]')

    col4.caption('Average REA per 100')
    text4 = df_plot['REA_per_100'].mean().round(2)
    col4.subheader(f':violet[{text4}]')

    col5.caption('Average ADG')
    text5 = df_plot['ADG'].mean().round(2)
    col5.subheader(f':violet[{text5}]')

    col6.caption('Average %IMF')
    text6 = df_plot['%IMF'].mean().round(2)
    col6.subheader(f':violet[{text6}]')

    col7.caption('Count')
    text7 = df_plot['Name'].count()
    col7.subheader(f':violet[{text7}]')

    st.subheader('Bull Scatterplot for {}'.format(dropdown_1), help='Bull Scores: '
                                                                    'Bull Score is calculated based on the '
                                                                    'sum of rankings when the division is '
                                                                    'sorted incrementally by ADG, REA, '
                                                                    'REA per 100 and %IMF. Each category '
                                                                    'ranking is scored from highest to '
                                                                    'lowest based on the sort. Highest '
                                                                    'number (ranking)'
                                                                    'being the best value for the category.'
                                                                    'The Bull Score is the sum of the 4 '
                                                                    'rankings (ADG,'
                                                                    'REA, REA per 100, & %IMF). Since Bull '
                                                                    'Scores are calculated based on '
                                                                    'Division, the scores are'
                                                                    'only relevant to that class. ')

    cat_choices = ['bull_score', 'Weight', 'REA', 'ADG', 'REA_per_100', '%IMF', 'Days_Old', 'Backfat', 'Scrotal']

    col_pd1, col_pd2 = st.columns(2, gap='small')

    with col_pd1:
        st.caption("Select Category for 'X' Axis")
        cat_x = st.selectbox(label=":green[Select X Category]",
                             key='catx',
                             options=cat_choices,
                             help='Select Measurement Category to chart on X Axis')
    with col_pd2:
        st.caption("Select Category for 'Y' Axis")
        cat_y = st.selectbox(label=":green[Select Y Category]",
                             key='caty',
                             options=cat_choices,
                             help='Select Measurement Category to chart on Y Axis')

    print('Selected X Category: {}'.format(cat_x))
    print("selected Y Category: {}".format(cat_y))

    user_scatter = px.scatter(data_frame=df_plot,
                              x=cat_x,
                              y=cat_y,
                              hover_name='Name',
                              color='Meas_Year',
                              size='Weight',
                              width=1800
                              )
    st.plotly_chart(user_scatter)

    # Displays the data for selected division in a spreadsheet

    st.subheader('{} Spreadsheet'.format(dropdown_1),
                 help='Spreadsheet: Default display is sorted by Bull Score (column 4). The spreadsheet can be '
                      'sorted by any column by clicking on the header for the desired sorting. ')
    st.write(df_plot)
    st.divider()

    # PLOT TRENDS FOR SELECTED DIVISION

    st.subheader('{} Division Trends by Year'.format(dropdown_1))
    div_cb1 = st.checkbox(label='{} Weight Trends'.format(dropdown_1))
    if div_cb1:
        plot = px.box(data_frame=df_plot.sort_values('Meas_Year'),
                      title='Weight Trends',
                      x='Meas_Year',
                      y='Weight',
                      color='Meas_Year')
        st.plotly_chart(plot)

    div_cb2 = st.checkbox(label='{} REA Size Trends'.format(dropdown_1))
    if div_cb2:
        plot = px.box(data_frame=df_plot.sort_values('Meas_Year'),
                      title='REA Size Trends',
                      x='Meas_Year',
                      y='REA',
                      color='Meas_Year')
        st.plotly_chart(plot)

    div_cb3 = st.checkbox(label='{} REA per 100 Trends'.format(dropdown_1))
    if div_cb3:
        plot = px.box(data_frame=df_plot.sort_values('Meas_Year'),
                      title='REA per 100 Trends',
                      x='Meas_Year',
                      y='REA_per_100',
                      color='Meas_Year')
        st.plotly_chart(plot)

    div_cb4 = st.checkbox(label='{} ADG Trends'.format(dropdown_1))
    if div_cb4:
        plot = px.box(data_frame=df_plot.sort_values('Meas_Year'),
                      title='ADG Trends',
                      x='Meas_Year',
                      y='ADG',
                      color='Meas_Year')
        st.plotly_chart(plot)

    div_cb5 = st.checkbox(label='{} %IMF Trends'.format(dropdown_1))
    if div_cb5:
        plot = px.box(data_frame=df_plot.sort_values('Meas_Year'),
                      title='%IMF Trends',
                      x='Meas_Year',
                      y='%IMF',
                      color='Meas_Year')
        st.plotly_chart(plot)

with tab3:
    st.header('Individual Bull Analysis')

    # Add Dropdown Menu - Select Bull by Name and Division(Class)
    # - Division is needed to separate duplicate entries for same name in different divisions
    bull_list = (df['Name'] + ' - ' + df['Class']).sort_values()

    bull_dropdown = st.selectbox(label_visibility='visible',
                                 label='Select Bull for Analysis',
                                 key='bull_sel1',
                                 options=bull_list)
    st.markdown(bull_dropdown)

    # bull_list is a list of strings with Name & Class - Now you need to split into a list
    # and the select for name and then division(class)

    bull_split = bull_dropdown.split(' - ')

    # Get the correct selection
    bull = df[df['Name'] == bull_split[0]]  # Get the bull name
    bull = bull[bull['Class'] == bull_split[1]]
    # Because some bulls are shown multiple
    #  times get the selected bull and then the division
    st.write(bull)

    # Get the division metrics max, min, median for REA, REA per 100, %IMF, Weight, ADG
    # div = bull_split[1]
    bull_name = bull_split[0]
    div = df[df['Class'] == bull_split[1]]

    st.divider()

    st.markdown('Bull Score Comparisons')
    st.caption('{} & Division Bull Scores'.format(bull_name))

    score_trace1 = go.Scatter(
        y=bull['bull_score'],
        x=bull['Name'],
        name='Selected Bull {}'.format('bull_score'),
        mode='markers',
        marker=dict(size=20))
    score_trace2 = go.Box(
        y=div['bull_score'],
        name='{} Division Bull Scores'.format(bull_split[1])
    )
    fig = go.Figure()
    fig.add_trace(score_trace1).update_layout(xaxis_title='Bull Scores', yaxis_title="Score")
    fig.add_trace(score_trace2)

    st.plotly_chart(fig)

    st.divider()

    col5, col6, col7 = st.columns(3, gap='medium')

    with col5:
        st.markdown('REA Size')
        st.caption('{} & Division Metrics'.format(bull_name))
        trace1 = go.Scatter(
            y=bull['REA'],
            x=bull['Name'],
            name='Selected Bull {}'.format('REA'),
            mode='markers',
            marker=dict(size=20),

        )
        trace2 = go.Box(
            y=div['REA'],
            name='{} Division Metrics'.format(bull_split[1])
        )

        fig = go.Figure()
        fig.add_trace(trace1).update_layout(xaxis_title='REA Size', yaxis_title="Inches")
        fig.add_trace(trace2)

        st.plotly_chart(fig)

    with col6:
        st.markdown('REA_per_100')
        st.caption('{} & Division Metrics'.format(bull_name))
        trace1 = go.Scatter(
            y=bull['REA_per_100'],
            x=bull['Name'],
            name='Selected Bull {}'.format('REA_per_100'),
            mode='markers',
            marker=dict(size=20)
        )

        trace2 = go.Box(
            y=div['REA_per_100'],
            name='{} Division Metrics'.format(bull_split[1])
        )

        fig = go.Figure()
        fig.add_trace(trace1).update_layout(xaxis_title='REA per 100', yaxis_title="Inches")
        fig.add_trace(trace2)

        st.plotly_chart(fig)

    with col7:
        st.markdown('%IMF')
        st.caption('{} & Division Metrics'.format(bull_name))
        trace1 = go.Scatter(
            y=bull['%IMF'],
            x=bull['Name'],
            name='Selected Bull {}'.format('%IMF'),
            mode='markers',
            marker=dict(size=20)
        )

        trace2 = go.Box(
            y=div['%IMF'],
            name='{} Division Metrics'.format(bull_split[1],
                                              )
        )

        fig = go.Figure()
        fig.add_trace(trace1).update_layout(xaxis_title='%IMF', yaxis_title="%")
        fig.add_trace(trace2)

        st.plotly_chart(fig)
        st.divider()
        with col5:
            st.markdown('ADG')
            st.caption('{} & Division Metrics'.format(bull_name))
            trace1 = go.Scatter(
                y=bull['ADG'],
                x=bull['Name'],
                name='Selected Bull {}'.format('ADG'),
                mode='markers',
                marker=dict(size=20)
            )

            trace2 = go.Box(
                y=div['ADG'],
                name='{} Division Metrics'.format(bull_split[1],
                                                  )
            )

            fig = go.Figure()
            fig.add_trace(trace1).update_layout(xaxis_title='ADG', yaxis_title="lb")
            fig.add_trace(trace2)

            st.plotly_chart(fig)

            with col6:
                st.markdown('Weight')
                st.caption('{} & Division Metrics'.format(bull_name))
                trace1 = go.Scatter(
                    y=bull['Weight'],
                    x=bull['Name'],
                    name='Selected Bull {}'.format('Weight'),
                    mode='markers',
                    marker=dict(size=20)
                )

                trace2 = go.Box(
                    y=div['Weight'],
                    name='{} Division Metrics'.format(bull_split[1],
                                                      )
                )

                fig = go.Figure()
                fig.add_trace(trace1).update_layout(xaxis_title='Weight', yaxis_title="lb")
                fig.add_trace(trace2)

                st.plotly_chart(fig)

            with col7:
                st.markdown('Days Old')
                st.caption('{} & Division Metrics'.format(bull_name))
                trace1 = go.Scatter(
                    y=bull['Days_Old'],
                    x=bull['Name'],
                    name='Selected Bull {}'.format('Days_Old'),
                    mode='markers',
                    marker=dict(size=20)
                )

                trace2 = go.Box(
                    y=div['Days_Old'],
                    name='{} Division Metrics'.format(bull_split[1],
                                                      )
                )

                fig = go.Figure()
                fig.add_trace(trace1).update_layout(xaxis_title='Days_Old', yaxis_title="Age in Days")
                fig.add_trace(trace2)

                st.plotly_chart(fig)
