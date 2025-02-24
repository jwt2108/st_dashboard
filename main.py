import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import plotly.io as pio
import pandas as pd
import datetime as dt

st.set_page_config(layout='wide')

# Read in the data and format
df = pd.read_csv('data/all_bulls_new.csv')
print(df.count())

pio.templates.default = "plotly_dark"

del df['Meas_Year']
del df['Unnamed: 0']
# Reorder columns
df = df.reindex(
    columns=['Name', 'DOB', 'Days_Old', 'bull_score', 'REA', 'rea_score', 'REA_per_100', 'rea_ratio_score', 'Weight',
             'ADG', 'adg_score', '%IMF', 'imf_score', 'Backfat', 'Scrotal', 'scrotal_cm_per_day', 'Class'])

# Setup Main Page

st.header('Bull Analysis Dashboard')

st.subheader("Background Information")

notes1 = "<h4>Data</h4><ul> " \
         "<li>All data employed in the analysis was obtained from results posted online on the American Highland Cattle " \
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

colnt1, colnt2, colnt3 = st.columns(3)

with colnt1:
    st.markdown(notes1, unsafe_allow_html=True)
with colnt2:
    st.markdown(notes2, unsafe_allow_html=True)
with colnt3:
    st.markdown(notes3, unsafe_allow_html=True)

st.subheader('All Bulls - Summaries by Division (Count, Age (Days) & Weights)')

div_list = df['Class'].unique()

hist_plot = px.histogram(data_frame=df,
                         x='Class',
                         color='Class',
                         title='Bull Count by Division ',
                         width=1800

                         )
st.plotly_chart(hist_plot)

col_b, col_c = st.columns(2, gap='small')

with col_b:
    box_plot = px.box(data_frame=df,
                      y='Days_Old',
                      x='Class',
                      color='Class',
                      title='Bull Age by Division ')
    st.plotly_chart(box_plot)

with col_c:
    box_plot = px.box(data_frame=df,
                      y='Weight',
                      x='Class',
                      color='Class',
                      title='Bull Weight by Division ')
    st.plotly_chart(box_plot)

#  Dropdown 1
st.subheader('AHCA NWSS Bull Division Selection')

dropdown_1 = st.selectbox(label='Select NWSS Bull Division',
                          key='dd1',
                          options=div_list,
                          help='Select Bull Division for Analysis')
df_plot = df[df['Class'] == dropdown_1]
df_plot = df_plot.reset_index(drop=True)
df_plot.index += 1
# st.write(df_plot)

st.text('Average Values for Selected Bull Division')

# col1, col7 = st.columns([1,1], gap='small')
col1, col7, col2, col3, col4, col5, col6 = st.columns(7, gap='small')  # col4, col5, col6
col1.caption('Average Age(Days)')
col1.subheader(df_plot['Days_Old'].mean().round(2))
col2.caption('Average Weight')
col2.subheader(df_plot['Weight'].mean().round(2))
col3.caption('Average REA')
col3.subheader(df_plot['REA'].mean().round(2))
col4.caption('Average REA per 100')
col4.subheader(df_plot['REA_per_100'].mean().round(2))
col5.caption('Average ADG')
col5.subheader(df_plot['ADG'].mean().round(2))
col6.caption('Average %IMF')
col6.subheader(df_plot['%IMF'].mean().round(2))
col7.caption('Count')
col7.subheader(df_plot['Name'].count())

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

cat_choices = ['bull_score','Weight', 'REA', 'ADG', 'REA_per_100', '%IMF', 'Days_Old', 'Backfat', 'Scrotal']

col_pd1, col_pd2 = st.columns(2, gap='small')

with col_pd1:
    st.caption("Select Category for 'X' Axis")
    cat_x = st.selectbox(label="Select X Category",
                         key='catx',
                         options=cat_choices,

                         help='Select Measurement Category to chart on X Axis')
with col_pd2:
    st.caption("Select Category for 'Y' Axis")
    cat_y = st.selectbox(label="Select Y Category", key='caty',
                         options=cat_choices,
                         help='Select Measurement Category to chart on Y Axis')

print('Selected X Category: {}'.format(cat_x))
print("selected Y Category: {}".format(cat_y))

user_scatter = px.scatter(data_frame=df_plot,
                          x=cat_x,
                          y=cat_y,
                          hover_name='Name',
                          color='Name',
                          size='Weight',
                          width=1800
                          )
st.plotly_chart(user_scatter)

# score_scatter = px.scatter(data_frame=df_plot,
#                            y='Days_Old',
#                            x='bull_score',
#                            size='Weight',
#                            color='Name',
#                            hover_name='Name',
#                            width=1500,
#                            )
#
# st.plotly_chart(score_scatter)
#
# df_plot = df[df['Class'] == dropdown_1]
# df_plot = df_plot.reset_index(drop=True)
# df_plot.index +=

st.subheader('{} Spreadsheet'.format(dropdown_1),
             help='Spreadsheet: Default display is sorted by Bull Score (column 4). The spreadsheet can be '
                  'sorted by any column by clicking on the header for the desired sorting. ')
st.write(df_plot)
