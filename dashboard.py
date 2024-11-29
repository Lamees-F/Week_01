# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="KSA Job Compass",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded")

#######################
# Load data
df_reshaped = pd.read_csv('processed_dataset.csv')
df_reshaped['region'].replace(to_replace='Others', value='Riyadh', inplace=True)
df_reshaped['region'].replace(to_replace="'مكة المكرمة'", value='Makkah', inplace=True)

with st.sidebar:
    st.title('🧭 KSA Job Compass Dashboard')
    

    region_list = sorted(list(df_reshaped.region.unique()))
    
    selected_region = st.selectbox('Select Region', region_list)
    df_selected_region = df_reshaped[df_reshaped.region == selected_region]


# map
def make_map():
    x = df_reshaped['region'].value_counts().values
    data = {
    'region': [
        'الرياض', 'المنطقة الشرقية', 'مكة المكرمة', 'حائل', 'المدينة المنورة', 
        'الباحة', 'عسير', 'القصيم', 'تبوك', 'جازان', 'الحدود الشمالية', 
        'نجران', 'الجوف'
    ],
    'latitude': [
        24.7136,  # الرياض 
        26.8200,  # المنطقة الشرقية 
        21.4225,  # مكة المكرمة 
        27.5110,  # حائل 
        24.4686,  # المدينة المنورة 
        19.9992,  # الباحة 
        18.2176,  # عسير 
        26.3500,  # القصيم 
        28.3834,  # تبوك 
        16.8895,  # جازان 
        30.1054,  # الحدود الشمالية 
        17.4923,  # نجران 
        29.7740   # الجوف 
    ],
    'longitude': [
        46.6753,  # الرياض 
        49.8000,  # المنطقة الشرقية 
        39.8262,  # مكة المكرمة 
        41.7128,  # حائل 
        39.6117,  # المدينة المنورة 
        41.6245,  # الباحة 
        42.5087,  # عسير 
        43.9667,  # القصيم 
        36.5665,  # تبوك 
        42.5596,  # جازان 
        41.0017,  # الحدود الشمالية
        44.1484,  # نجران
        40.0517   # الجوف 
    ],
    'size' : x*500,
    }
    df = pd.DataFrame(data)

    return st.map(df,latitude='latitude',longitude='longitude',size='size',color='#00b30088')

def get_most_demanded_jobs(region_name = 'Makkah'):

    region_counts = df_reshaped.groupby(['region', 'eco_activity']).size().reset_index(name='count')
    region_data = region_counts[region_counts['region'] == region_name]
    # print('--------------',len(region_data))  

    region_data = region_data.sort_values(by='count',ascending=False)
      
    return region_data



######         Main Panel
col = st.columns((2, 4.5, 1.5), gap='medium')

with col[0]:
    
    st.markdown('#### Jobs based on Gender')
    gender_count = df_selected_region['gender'].value_counts()
    st.bar_chart(gender_count,color='#00b30095')
  
    st.markdown('#### Contract Type')
    job_status_count = df_selected_region['contract'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(job_status_count, labels=job_status_count.index, autopct='%1.1f%%', startangle=90, colors=['#00b30095', '#00660095'])
    ax.axis('equal')
    st.pyplot(fig)


with col[1]:
    st.markdown('#### Job Distribuation in KSA')
    make_map()

    st.markdown('#### Company size in '+ selected_region)
    comp_size_counts = df_selected_region['comp_size'].value_counts()
    st.bar_chart(comp_size_counts,color='#00b30095')

      
with col[2]:
    st.markdown('#### Demand Econemy Activity in '+ selected_region)

    demand_jobs = get_most_demanded_jobs(selected_region)
    st.dataframe(
        demand_jobs,
        column_order=("eco_activity", "count"),
        hide_index=True,
        width=None,
        column_config={
            "eco_activity": st.column_config.TextColumn(
                "Economy Activity",
                 width='medium',
            ),
            "count": st.column_config.ProgressColumn(
                "Demand ",
                format = "%d", 
                min_value = 0,
                max_value = 130,

            ),
        }
    )
    with st.expander('About', expanded=True):
        st.write('''
            - Data: [JDarat 2020](https:).
            - :green[**Job Distribuation in KSA**]: General overview of data distribuion as clusters
            - :green[**Demands Economy Activity**]: shows the highest Economy Activity in a region 
            - :green[**Jobs based on Gender**]: shows jobs number based on gender 
            - :green[**Contract Type**]: shows jobs contract in a region    
            - :green[**Company size**]: shows company size distribution on a region    
            ''')
        
st.markdown("<hr>", unsafe_allow_html=True)  # Horizontal line for visual separation
st.markdown("<p style='text-align: center;'>Made by Group 04 @ Tuwaiq Academy</p>", unsafe_allow_html=True)
