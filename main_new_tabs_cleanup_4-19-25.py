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
df = pd.read_csv('data/all_bulls_newest.csv')
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

tab1, tab2, tab3, tab4 = st.tabs(['NWSS Highland Bull Background Information    ',
                                  'NWSS Highland Bull Trends by Division     ',
                                  'NWSS Bull Division Analysis       ',
                                  'NWSS Selected Bull Analysis'])

with tab1:
    # st.subheader("Background Information")
    st.markdown("<h1 style='text-align: center; color: CornflowerBlue;'>Background Information</h1>", unsafe_allow_html=True)
    notes1 = "<h4>Data</h4><ul> " \
             "<li>All data employed in the analysis was obtained from results posted publicly online on the American Highland Cattle " \
             "Association (AHCA) website: (""http://www.highlandcattleusa.org/)</li>" \
             "<li>Unable to read year 2017</li> <li>Data – 319 Bulls Compared</li><li>2021 was cancelled due to COVID</li>" \
             "<li>Each year's measurements document was converted to .csv and read into a JUPYTER notebook</li>" \
             "<li>2014 – 2025 with the above exceptions</li><li>Only bulls with all measurements were included in " \
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

    notes_REA = "<i>REA (Ribeye Area) in cattle refers to the size of the muscle cross-section from the ribeye steak " \
                "(located between the 12th and 13th ribs). <br>It is a key measurement used in cattle grading and " \
                "evaluation, especially when assessing the quality and yield of meat.</i>"
    REA_how = "<li>Location: The REA is measured between the 12th and 13th ribs, as this area provides a representative " \
              "sample of the overall muscle development and fat coverage in the animal.</li>" \
              "<li>Measurement Method: The measurement is typically taken using an ultrasound or a ribeye scanner. " \
              "A scan is done on the carcass, and the area is calculated as the total surface area of the ribeye " \
              "muscle in square inches or square centimeters. It can also be estimated by visual assessment in live " \
              "cattle, although ultrasound technology is more accurate.</li>"
    REA_why = "<li>Meat Yield: The size of the ribeye muscle directly correlates with the amount of muscle and " \
              "therefore the potential yield of meat. A larger REA indicates a larger muscle mass, which often results in higher meat yield and " \
              "higher-quality cuts from the ribeye.</li><br>" \
              "<li>Carcass Quality: REA is an indicator of the overall muscle development and condition of the animal. " \
              "A large ribeye area generally suggests a well-developed muscle mass, which is a positive trait for beef producers aiming for " \
              "high-quality, well-marbled beef.</li><br>" \
              "<li>Genetic Selection: In cattle breeding, REA is often used as a selection criterion to identify animals with " \
              "superior muscling and growth potential. Cattle with a larger ribeye area tend to have better feed efficiency and greater " \
              "lean meat production.</li><br>" \
              "<li>Carcass Grading: REA plays a role in the USDA grading system for beef. A larger ribeye area can help " \
              "improve the USDA Quality Grade (which measures marbling and tenderness) and Yield Grade (which measures the " \
              "amount of usable meat on the carcass). A larger REA tends to lower the Yield Grade, indicating a higher yield of " \
              "lean meat from the carcass.</li>"


    imf_info = "IMF (Intramuscular Fat) Percentage in cattle refers to the amount of fat that is deposited within the muscle tissue, " \
               "specifically within the muscle fibers themselves. This fat is commonly known as marbling, and it plays a " \
               "crucial role in determining the quality of beef, including tenderness, flavor, and juiciness."
    imf_methods_1 = "<li>Visual Assessment: In some cases, trained professionals can visually estimate the amount of " \
                    "marbling in a carcass by inspecting the muscle. However, this method is less precise than other technologies.<br><br></li>" \
                    "<li>Ultrasound Technology: Similar to how REA is measured, ultrasound can be used to scan live " \
                    "cattle and estimate IMF. " \
                    "It provides a non-invasive and fairly accurate way of assessing the marbling in the muscle.<br><br></li>" \
                    "<li>Chemical or Laboratory Analysis: The most accurate way to measure IMF is by collecting a muscle " \
                    "sample after " \
                    "slaughter and conducting a chemical analysis in a laboratory. This can be done using " \
                    "near-infrared spectroscopy (NIR) " \
                    "or other specialized methods to measure the fat content directly.<br><br></li>"
    imf_methods_2 = "<li>Dual-Energy X-ray Absorptiometry (DEXA): This technology uses x-rays to precisely measure fat, " \
                    "lean tissue, and bone content in carcasses, including the amount of intramuscular fat.<br><br></li>" \
                    "<li>Calculation: The IMF percentage is typically expressed as a percentage of fat in the muscle tissue, " \
                    "and the level of IMF is often assessed as a marbling score (e.g., Low, Modest, Moderate, High, Very High). " \
                    "In beef grading systems, marbling scores are used to classify the level of intramuscular fat.</li>"

    imf_column1 = "<h3>1. Meat Quality:</h3>"\
                  "<li>Flavor: Intramuscular fat is crucial for the flavor of beef. It contributes to a rich, buttery flavor because fat " \
                  "is where many of the flavor compounds are stored. Beef with higher IMF tends to be more flavorful.</li>"\
                  "<li>Tenderness: IMF also plays a significant role in the tenderness of meat. Fat acts as a lubricant between muscle" \
                  "fibers, making the beef more tender. This is why high-marbling beef is often prized for its melt-in-your-mouth texture.</li>" \
                  "<li>Juiciness: The fat within the muscle helps retain moisture during cooking, leading to more juicy meat. Without" \
                  "sufficient IMF, beef can become dry, particularly when cooked at higher temperatures."

    imf_column2 = "<h3>2. Grading and Market Value:</h3>" \
                  "<li>USDA Grading: The USDA Beef Quality Grades, such as Prime, Choice, and Select, are based partly on the amount of " \
                  "IMF present in the muscle. Beef with higher levels of IMF (such as Prime) is generally considered of higher quality and " \
                  "can command a higher price on the market. Prime beef typically has an IMF percentage of around 8-12%, while " \
                  "Choice is generally around 4-7%, and Select is lower than that.</li>" \
                  "<li>Consumer Preference: High marbling is often a mark of higher consumer satisfaction, especially in premium " \
                  "cuts like steaks (ribeye, strip loin, etc.). Beef with higher IMF is typically preferred in restaurants and by " \
                  "consumers who are looking for a premium eating experience.</li>"
    imf_column3 = "<h3>3. Breeding and Selection:</h3>" \
                  "<li>Genetics: IMF percentage is often used in genetic selection. Cattle with higher marbling are selectively " \
                  "bred to pass on the trait to offspring, which is particularly important for premium beef production. Advances in " \
                  "genomic testing now allow producers to select animals with higher genetic potential for marbling.</li>" \
                  "<h3>4. Market Differentiation:</h3>" \
                    "Beef with higher IMF is often marketed as premium beef (e.g., Wagyu, Angus, and other high-marbling breeds) and " \
                    "may be sold at a premium price. In some markets, beef with specific IMF thresholds may be part of certified beef programs " \
                    "or other value-added marketing initiatives."

    adg_c1 = "<h3>1. Efficiency of Production:</h3>" \
             "<li>Growth Monitoring: ADG provides a clear picture of how quickly cattle are growing, " \
             "which is crucial for producers aiming to maximize production efficiency. Faster-growing cattle generally result in " \
             "quicker time-to-market, leading to more efficient operations.</li>" \
             "<li>Feed Efficiency: A higher ADG generally correlates with better feed conversion — meaning the animal is converting feed " \
             "into weight gain more efficiently. This is important because feed costs typically represent a significant portion of total production costs.</li>" \
             "<h3>2.Profitability:</h3>" \
             "<li>Cost vs. Gain: If cattle are growing too slowly, the producer might need to feed them longer, increasing feed costs and" \
             " extending the time before the animal is ready for market. Conversely, rapid growth (high ADG) allows cattle to reach market " \
             "weight sooner, improving the producer's turnover and profitability</li>" \
             "<li>Market Timing: For cattle that are being raised for beef, especially in high-quality or premium markets, " \
             "reaching a certain weight quickly can help meet specific market requirements, such as carcass weight or fat content." \
             "Health Indicators: Consistent, healthy weight gain often indicates that the cattle are in good health, receiving proper " \
             "nutrition, and not suffering from diseases or stress that could stunt growth.</li>"

    adg_c2 = "<h3>3. Breeding Selection</h3>" \
             "Breeders use ADG to evaluate genetics. Cattle with superior ADG can pass on desirable traits like " \
             "faster growth and efficiency to offspring, enhancing herd quality over time." \
             "<h3>4. Meat Quality and Market Readiness</h3>" \
             "Animals with optimal ADG are more likely to reach ideal weights and fat composition for premium meat grades, " \
             "aligning with market demands." \
             "<h3>5. Health and Welfare Indicator</h3>" \
             "Poor ADG can signal health issues, poor nutrition, or suboptimal environmental " \
             "conditions. Monitoring ADG helps producers identify and address these problems early." \
             "<h3>6. Competitive Advantage</h3>" \
             "Whether selling seedstock or commercial beef, showcasing high ADG in your cattle can be a " \
             "selling point to buyers looking for productivity and efficiency."

    adg_3 = "<h3>1. Genetics</h3>" \
            "<li>Breed: Different breeds have varying growth potentials. For instance, Continental breeds like Charolais " \
            "often exhibit higher ADG compared to British breeds like Angus.</li>" \
            "<li>Lineage/Parentage: Animals from sires and dams with superior growth traits tend to have better ADG.</li>" \
            "<li>Selection for Traits: Selecting cattle with high Expected Progeny Differences (EPD) for growth can significantly improve ADG.</li>"\
            ""\
            "<h3>2. Nutrition</h3>" \
            "<li>Energy Intake: Diets with adequate energy (calories) are critical for weight gain. High-energy grains or " \
            "well-balanced forages improve ADG.</li>" \
            "<li>Protein Levels: Sufficient protein is essential for muscle growth and overall development.</li>" \
            "<li>Feed Quality: High-quality forages and feedstuffs result in better feed efficiency and ADG.</li>" \
            "<li>Minerals and Vitamins: Proper supplementation of minerals (e.g., calcium, phosphorus) and vitamins (e.g., A, D, E) " \
            "ensures optimal growth and health.</li>" \
            "<li>Feed Additives: Additives like ionophores (e.g., monensin) can enhance feed efficiency and ADG.</li>"\
            "<h3>3. Management</h3>" \
            "<li>Weaning Practices: Stress-free weaning and proper post-weaning nutrition boost growth rates.</li>" \
            "<li>Health Protocols: Vaccinations and parasite control prevent diseases that can reduce ADG. " \
            "<br>Stocking Density: Overcrowding can reduce feed access and increase stress, negatively impacting ADG.</li>" \
            "<li>Castration and Implants: Timing of castration and use of growth-promoting implants can influence growth rates.</li>" \


    adg_4 = "<h3>4. Environment</h3>" \
            "<li>Temperature: Extreme cold or heat can reduce feed intake and energy available for growth.</li>" \
            "<li>Housing and Shelter: Comfortable, clean housing minimizes stress and supports optimal growth.</li>" \
            "<li>Pasture Quality: Good pasture management ensures consistent access to nutritious forage.</li>"\
        "<h3>5. Behavior and Social Dynamic</h3>" \
            "<li>Feed Access: Dominant animals may outcompete others for feed, affecting the ADG of less aggressive individuals.</li>" \
            "<li>Stress Levels: Low-stress handling practices improve cattle performance</li>" \
            "<h3>6. Age and Stage of Growth</h3>" \
            "Younger cattle generally have a higher potential for ADG compared to mature animals, as they are in a more active growth phase." \
            "<h3>7. Feed Conversion Efficiency (FCE)</h3>" \
            "Some cattle convert feed to body weight more efficiently than others, affecting ADG. Feedlot monitoring helps track and optimize FCE." \
            "<h3>8. Water Quality and Availability</h3>" \
            "Access to clean and adequate water is critical for digestion and metabolism, directly affecting ADG"


    colnt1, colnt2, colnt3 = st.columns(3, gap='large')

    with colnt1:
        st.markdown(notes1, unsafe_allow_html=True)
    with colnt2:
        st.markdown(notes2, unsafe_allow_html=True)
    with colnt3:
        st.markdown(notes3, unsafe_allow_html=True)

    # REA Information
    st.divider()
    st.markdown("<h1 style='text-align: center; color: CornflowerBlue;'>REA Information</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)

    with c2:
        st.markdown(notes_REA, unsafe_allow_html=True)
    # with c3:
    #     st.write('')

    rea_col1, rea_col2 = st.columns(2, gap='large')

    with rea_col1:
        st.subheader(':blue[How REA is Measured]')
        st.markdown(REA_how, unsafe_allow_html=True)
    with rea_col2:
        st.subheader(':blue[Why REA Measurement is Important]')
        st.markdown(REA_why, unsafe_allow_html=True)

    st.divider()
    # IMF Information

    # st.markdown("<h1 style='text-align: center; color: grey;'>Big headline</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: CornflowerBlue;'>IMF Explained</h1>", unsafe_allow_html=True)

    c = st.container()
    # c1a, c2a = st.columns(2)
    with c:
        st.subheader(':blue[Measurement Methods]')
        imf_c1, imf_c2 = st.columns(2, gap='large')
        with imf_c1:
            st.markdown(imf_methods_1, unsafe_allow_html=True)
        with imf_c2:
            st.markdown(imf_methods_2, unsafe_allow_html=True)

    with c:
        st.subheader(':blue[Why IMF Percentage is Important]')
        imf_c1a, imf_c1b, imf_c1c = st.columns(3, gap='medium')
        with imf_c1a:
            st.markdown(imf_column1, unsafe_allow_html=True)
        with imf_c1b:
            st.markdown(imf_column2, unsafe_allow_html=True)
        with imf_c1c:
            st.markdown(imf_column3, unsafe_allow_html=True)

    st.divider()

    # ADG Information
    c2 = st.container()
    with c2:
        st.markdown("<h1 style='text-align: center; color: CornflowerBlue;'>Average Daily Gain (ADG)</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: CornflowerBlue;'>Why is ADG Important?</h3>",
                    unsafe_allow_html=True)
        adg1, adg2 = st.columns(2, gap='large')
        with adg1:
            st.markdown(adg_c1, unsafe_allow_html=True)
        with adg2:
            st.markdown(adg_c2,unsafe_allow_html=True)
    st.divider()
    c3 = st.container()
    with c3:
        st.markdown("<h3 style='text-align: center; color: CornflowerBlue;'>Influences on ADG</h3>",
                    unsafe_allow_html=True)
        adg3, adg4 = st.columns(2, gap='large')
        with adg3:
            st.markdown(adg_3,unsafe_allow_html=True)
        with adg4:
            st.markdown(adg_4, unsafe_allow_html=True)




with tab2:
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

with tab3:
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

with tab4:
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
