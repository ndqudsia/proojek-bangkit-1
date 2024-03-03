import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

# load dataset

days_df = pd.read_csv("day_data.csv")
hours_df = pd.read_csv("hour_data.csv")

days_df['dteday'] = pd.to_datetime(days_df['dteday'])

st.set_page_config(page_title="Capital Bikeshare: Pink Bike-sharing Dashboard :heart:",
                   page_icon="bar_chart:",
                   layout="wide")

# create helper functions

def create_monthly_users_df(days_df):
    monthly_users_df = days_df.resample(rule='M', on='dteday').agg({
        "casual": "sum",
        "registered": "sum",
        "count_cr": "sum"
    })
    monthly_users_df.index = monthly_users_df.index.strftime('%b-%y')
    monthly_users_df = monthly_users_df.reset_index()
    monthly_users_df.rename(columns={
        "dteday": "yearmonth",
        "count_cr": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    return monthly_users_df

def create_seasonly_users_df(days_df):
    seasonly_users_df = days_df.groupby("season").agg({
        "casual": "sum",
        "registered": "sum",
        "count_cr": "sum"
    })
    seasonly_users_df = seasonly_users_df.reset_index()
    seasonly_users_df.rename(columns={
        "count_cr": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    seasonly_users_df = pd.melt(seasonly_users_df,
                                      id_vars=['season'],
                                      value_vars=['casual_rides', 'registered_rides'],
                                      var_name='type_of_rides',
                                      value_name='count_rides')
    
    seasonly_users_df['season'] = pd.Categorical(seasonly_users_df['season'],
                                             categories=['Spring', 'Summer', 'Fall', 'Winter'])
    
    seasonly_users_df = seasonly_users_df.sort_values('season')
    
    return seasonly_users_df

def create_weekday_users_df(days_df):
    weekday_users_df = days_df.groupby("one_of_week").agg({
        "casual": "sum",
        "registered": "sum",
        "count_cr": "sum"
    })
    weekday_users_df = weekday_users_df.reset_index()
    weekday_users_df.rename(columns={
        "count_cr": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    weekday_users_df = pd.melt(weekday_users_df,
                                      id_vars=['one_of_week'],
                                      value_vars=['casual_rides', 'registered_rides'],
                                      var_name='type_of_rides',
                                      value_name='count_rides')
    
    weekday_users_df['one-of_week'] = pd.Categorical(weekday_users_df['one_of_week'],
                                             categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    
    weekday_users_df = weekday_users_df.sort_values('one_of_week')
    
    return weekday_users_df

def create_hourly_users_df(hours_df):
    hourly_users_df = hours_df.groupby("hours").agg({
        "casual": "sum",
        "registered": "sum",
        "count_cr": "sum"
    })
    hourly_users_df = hourly_users_df.reset_index()
    hourly_users_df.rename(columns={
        "count_cr": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    return hourly_users_df

# make filter components (komponen filter)

min_date_days = days_df["dteday"].min()
max_date_days = days_df["dteday"].max()

min_date_hours = hours_df["dteday"].min()
max_date_hours = hours_df["dteday"].max()

# ----- SIDEBAR -----

with st.sidebar:
    # add capital bikeshare logo
    st.image("https://raw.githubusercontent.com/ndqudsia/proojek-bangkit-1/main/SAPERE%20AUDE.jpeg")


    # mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label="Date Filter", min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days]
    )


# hubungkan filter dengan main_df

main_days_df = days_df[
    (days_df["dteday"] >= str(start_date)) &
    (days_df["dteday"] <= str(end_date))
]

main_hours_df = hours_df[
    (hours_df["dteday"] >= str(start_date)) &
    (hours_df["dteday"] <= str(end_date))
]

# assign main_df ke helper functions yang telah dibuat sebelumnya

monthly_users_df = create_monthly_users_df(main_days_df)
weekday_users_df = create_weekday_users_df(main_days_df)
seasonly_users_df = create_seasonly_users_df(main_days_df)
hourly_users_df = create_hourly_users_df(main_hours_df)

# ----- MAINPAGE -----
st.title(":heart: Capital Bikeshare: Pink Bike-Sharing Dashboard")
st.markdown("##")

col1, col2, col3 = st.columns(3)

with col1:
    total_all_rides = main_days_df['count_cr'].sum()
    st.metric("Rides", value=total_all_rides)
with col2:
    total_casual_rides = main_days_df['casual'].sum()
    st.metric("Casual Rides", value=total_casual_rides)
with col3:
    total_registered_rides = main_days_df['registered'].sum()
    st.metric("Registered Rides", value=total_registered_rides)

st.markdown("---")

# ----- CHART -----
season_users_df = days_df.groupby("season").agg({
    "casual": "sum",
    "registered": "sum",
    "count_cr": "sum"
})

season_users_df

fig=plt.figure(figsize=(10,6))

sns.lineplot(x='season', y='casual', data=season_users_df, label='Casual')
sns.lineplot(x='season', y='registered', data=season_users_df, label='Registered')

plt.xlabel("Season")
plt.ylabel("Total Rides")
plt.title("Count of casual and registered bikeshare rides by Season")

plt.legend(loc='upper right', fontsize=14)

plt.tight_layout()
st.pyplot(fig)

daily_users_df = days_df.groupby("one_of_week").agg({
    "casual": "sum",
    "registered": "sum",
    "count_cr": "sum"
})

daily_users_df.head()

fig2=plt.figure(figsize=(16,6))

# Create a line plot using the sns.lineplot() function
sns.lineplot(x="one_of_week", y="casual", data=daily_users_df, label='Casual')
sns.lineplot(x="one_of_week", y="registered", data=daily_users_df, label='Registered')

plt.xlabel("Day")
plt.ylabel("Total Rides")
plt.title("Count of bikeshare rides by day")

# Add a legend to the plot
plt.legend(loc='upper right', fontsize=14)

# Show the plot
plt.tight_layout()
st.pyplot(fig2)


# ----- HIDE STREAMLIT STYLE -----
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)