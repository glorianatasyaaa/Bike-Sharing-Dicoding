import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Fungsi untuk membaca file CSV
def load_data(file):
    df = pd.read_csv(file)
    return df


bike_df = pd.read_csv("./dashboard/bike_data.csv")


bike_df['date'] = pd.to_datetime(bike_df['date'])
min_date = bike_df["date"].min()
max_date = bike_df["date"].max()

st.title('Bike Sharing Dashboard 🚲')



# Sidebar 
with st.sidebar:
    st.image("https://emojigraph.org/media/joypixels/bicycle_1f6b2.png")
    # Mengambil start_date & end_date dari date_input

    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    dfDay = bike_df[(bike_df["date"] >= str(start_date)) & 
                (bike_df["date"] <= str(end_date))]

# End Sidebar

col1, col2, col3 = st.columns(3)

with col1:
    total_penyewaan = dfDay["total_day"].sum()
    total_penyewaan = "{:,.0f}".format(total_penyewaan)
    st.metric("Total penyewaan", value=total_penyewaan)

with col2:
    total_casual = dfDay["casual_day"].sum()
    total_casual = "{:,.0f}".format(total_casual)
    st.metric("Casual Riders", value=total_casual)

with col3:
    total_registered = dfDay["registered_day"].sum()
    total_registered = "{:,.0f}".format(total_registered)
    st.metric("Registered Riders", value=total_registered) 

st.markdown("---")

bike_season = bike_df.groupby(by="season_day").agg({
    'total_day' : ['mean','max', 'min'],
})

bike_cuaca = bike_df.groupby(by="weathersit_day").agg({
    'total_day' : ['mean','max', 'min'],
})

col1, col2 = st.columns(2)
with col1 : 
    st.subheader("Data per Season")
    st.dataframe(bike_season)


with col2:
    st.subheader("Data per Cuaca")
    st.dataframe(bike_cuaca)


st.subheader('Distribusi Penyewaan Sepeda per Bulan')
plt.figure(figsize=(12,6))
sns.boxplot(x='month_day', y='total_day', data=bike_df, palette='flare')
plt.title('')
plt.show()
st.pyplot(plt)


st.subheader('Distribusi Penyewaan Sepeda per Hari')
plt.figure(figsize=(12,6))
sns.boxplot(x='weekday_day', y='total_day', data=bike_df, palette='flare')
plt.title('Distribution of bike rentals V/S days of the week')
st.pyplot(plt)

st.subheader('Distribusi Penyewaan Sepeda per Jam')
plt.figure(figsize=(12,6))
sns.boxplot(x='hour', y='total_hour', data=bike_df, palette='flare')
plt.title('Distribution of bike rentals V/S days of the week')
st.pyplot(plt)


st.subheader('Rata-Rata Penyewaan per Bulan')
rental_bulan = bike_df.groupby('month_day')['total_day'].mean()
plt.figure(figsize=(12,6))
plt.bar(rental_bulan.index, rental_bulan.values, color='purple')
plt.title('')
plt.xlabel('Bulan')
plt.ylabel('Rata - Rata Penyewaan')
plt.show()
st.pyplot(plt)


st.subheader('Rata-Rata Penyewaan per Cuaca')
avg_weather = bike_df.groupby('weathersit_day')['total_day'].mean().reset_index().sort_values("total_day")
plt.figure(figsize=(12, 6))
sns.barplot(x='total_day', y='weathersit_day', data=avg_weather, palette='flare')
plt.title('')
plt.xlabel('Average Rentals')
plt.ylabel('Weather Conditions')
plt.show()
st.pyplot(plt)

st.header("Conlusion")
st.subheader("Pertanyaan Bisnis 1 : Berapa jumlah rata-rata persewaan sepeda per hari dan bagaimana variasinya sepanjang bulan?")
st.write("Jumlah rata-rata penyewaan per hari berada di angka 4000an dan cenderung stabil tiap harinya. Namun, jika dilihat dari total penyewaan per bulan terjadi tren yang cendreung meningkat pada bulan Januari-July, stabil pada July-September dan menurun pada September-Desember")

st.subheader("Pertanyaan Bisnis 2 : Bagaimana hubungan kondisi cuaca dengan jumlah rata-rata penyewaan?")
st.write("Kondisi cuaca sangat memengaruhi jumlah penyewaan terlihat pada saat kondisi cerah jumlah penyewaan mencapai 5000 dan mengalami penurunan drastis ketika kondisi hujan ringgan sampai setengahnya yaitu kurang dari 2000.")
