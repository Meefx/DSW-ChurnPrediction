import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import warnings
import plotly.express as px


warnings.filterwarnings('ignore')
model = joblib.load("model.pkl")

def input_csv():
  st.title("2. Predict from CSV")
  st.write("Upload a CSV file to predict the outcome of the customers. [You should upload csv file with this format](https://drive.google.com/file/d/1tXfTBBWnE7Ni4Qai47aRrbnsVRC4_Ji7/view?usp=sharing)")
  st.write("Note: Monthly Purchase and CLTV in [Thou. IDR] format")
  uploaded_file = st.file_uploader("Choose a file", type=["csv"])
  if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    prediction = preprocessing_csv(df)
    df['Churn Label'] = prediction['Churn Label']
    st.write("The uploaded file has been processed and the outcome of the data is predicted.")
    st.dataframe(df)
    # st.dataframe(prediction)
    # Hitung distribusi churn label
    churn_distribution = prediction['Churn Label'].value_counts()
    churn_distribution.index = ["Retain","Churn"]
    churn_distribution = churn_distribution.T.reset_index()

    # Tampilkan pie chart menggunakan matplotlib
    # fig, ax = plt.subplots()
    # # Warna untuk setiap kategori
    # colors = ['lightgrey', 'red']

    # ax.pie(churn_distribution, labels=["Retain", "Churn"], autopct='%1.1f%%', startangle=90, colors=colors, textprops={'fontsize': 14})
    # ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # # Tambahkan judul
    # plt.title('Distribution of Churn Label', fontsize=16) 


    # # Tampilkan di Streamlit
    # st.pyplot(fig)
    # Buat pie chart menggunakan Plotly Express
    fig = px.pie(churn_distribution, values='count', names='index', color='index',
     color_discrete_map={'Retain': 'lightgrey', 'Churn': 'red'},
     title='Retention vs Churn')

    fig.update_traces(textinfo='percent', textfont_size=24)


    # Tampilkan di Streamlit
    st.plotly_chart(fig)

    
    csv = df.to_csv()

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='Prediction Result.csv',
        mime='text/csv',
    )
    # st.write("The outcome of the patient is: ", df.iloc[0, -1])

def preprocessing_csv(df):
  # Set index to Customer ID
  df.dropna(inplace=True)
  df.set_index("Customer ID", inplace=True)

  # Replacing values to numeric
  replace_map = {
      'Yes': 1,
      'No': 0,
      'No internet service': 0
  }

  for col in ["Games Product", "Music Product", "Education Product", "Call Center", "Video Product", "Use MyApp"]:
      df[col] = df[col].replace(replace_map)

  # Ordinal encoding
  device_class_map = {
      'High End': 2,
      'Mid End': 1,
      'Low End': 0
  }
  df['Device Class'] = df['Device Class'].replace(device_class_map)

  # One-Hot Encoding
  df = pd.get_dummies(df, columns=["Location", "Payment Method"])


  # Feature Engineering
  df['number_of_products'] = df[ ["Games Product", "Music Product", "Education Product", "Call Center", "Video Product", "Use MyApp"]].sum(axis=1)

  df = df[['Tenure Months', 'Device Class', 'Games Product', 'Music Product',
     'Education Product', 'Call Center', 'Video Product', 'Use MyApp',
     'Monthly Purchase (Thou. IDR)', 'Longitude', 'Latitude',
     'CLTV (Predicted Thou. IDR)','Location_Bandung', 'Location_Jakarta',
     'Payment Method_Credit', 'Payment Method_Debit',
     'Payment Method_Digital Wallet', 'Payment Method_Pulsa', 'number_of_products']]

  df['Churn Label'] = model.predict(df)

  return df




