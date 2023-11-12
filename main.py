import streamlit as st
import streamlit.components.v1 as components
import joblib
import pandas as pd
import processing_df


def predict(tenure,device_class, games_product, music_product, education_product, call_center, video_product, use_myapp, monthly_purchase, 
            longitude, latitude, cltv,location_bandung,
            location_jakarta, method_credit, method_debit, method_ewallet, method_pulsa, number_of_products):
  data = pd.DataFrame([[tenure,device_class, games_product, music_product, education_product, call_center, video_product, use_myapp, monthly_purchase, 
            longitude, latitude, cltv, location_bandung,
            location_jakarta, method_credit, method_debit, method_ewallet, method_pulsa, number_of_products]], columns=['Tenure Months', 'Device Class', 'Games Product', 'Music Product',
       'Education Product', 'Call Center', 'Video Product', 'Use MyApp',
       'Monthly Purchase (Thou. IDR)', 'Longitude', 'Latitude',
       'CLTV (Predicted Thou. IDR)',
       'Location_Bandung', 'Location_Jakarta', 'Payment Method_Credit',
       'Payment Method_Debit', 'Payment Method_Digital Wallet',
       'Payment Method_Pulsa', 'number_of_products'])

  return [model.predict(data),model.predict_proba(data)[:, 1]]

def input_user():
  st.title('Customer Churn Predictor')
  st.header("1. Manual Input Prediction")
  st.write('Enter the characteristics of user:')
  tenure_months = st.number_input('Tenure Months:', min_value=0.0, value=1.0)
  monthly_purchases = st.number_input('Monthly Purchases (Thou. IDR):', min_value=1.0, value=1000.0, step=1000.0) / 1000.0

  cltv = st.number_input('Customer Lifetime Value (Thou. IDR):', min_value=1.0, value=10000.0, step=1000.0) / 1000.0

  location = st.selectbox('Location:', ['Jakarta', 'Bandung'])

  location_jakarta = 0
  location_bandung = 0
  longitude = 0
  latitude = 0
  if (location == "Jakarta"):
    location_jakarta = 1
    longitude = 106.816666	
    latitude = -6.2
  else:
    location_bandung = 1
    longitude = 107.60981
    latitude =  -6.914744

  payment_method = st.selectbox('Payment Method:',
                                ['Digital Wallet',
                                 'Pulsa',
                                 'Debit',
                                 'Credit'])
  method_eWallet = 0
  method_pulsa = 0
  method_debit = 0
  method_credit = 0

  if (payment_method == "Digital Wallet"):
    method_eWallet = 1
  elif (payment_method == "Pulsa"):
    method_pulsa = 1
  elif (payment_method == 'Debit'):
    method_debit = 1
  else:
    method_credit = 1

  device_class = st.selectbox('Device Class:',
                                ['High End',
                                 'Mid End',
                                 'Low End',])

  device_class_map = {
    'High End': 2,
    'Mid End': 1,
    'Low End': 0
 }

  selected_device_class = device_class_map[device_class]

  st.write('Subscribed Products (Can more than one):')
  option_1 = st.checkbox('Games Product')
  option_2 = st.checkbox('Music Product')
  option_3 = st.checkbox('Education Product')
  option_4 = st.checkbox('Call Center')
  option_5 = st.checkbox('Video Product')
  option_6 = st.checkbox('Use MyApp')

  has_games_product = 0
  has_music_product = 0
  has_education_product = 0
  has_call_center = 0
  has_video_product = 0
  has_use_myapp = 0
  # Option configuratio
  if (option_1 == 1):
    has_games_product = 1

  if (option_2 == 1):
    has_music_product = 1

  if (option_3 == 1):
    has_education_product = 1

  if (option_4 == 1):
    has_call_center = 1

  if (option_5 == 1):
    has_video_product = 1

  if (option_6 == 1):
    has_use_myapp = 1

  number_of_products = option_1 + option_2 + option_3 + option_4 + option_5 + option_6

  if st.button('Predict Churn'):
    isChurn, churnProb = predict(tenure_months, selected_device_class, has_games_product, has_music_product, 
                                 has_education_product, has_call_center, has_video_product, has_use_myapp, 
                                 monthly_purchases, longitude, latitude, cltv,
                                 location_bandung, location_jakarta, method_credit,
                                 method_debit, method_eWallet, method_pulsa,number_of_products)
    if (isChurn[0] == 1):
      st.error(f'Customer will churn with probability of {(churnProb[0]):,.2f}', icon="🚨")
    else:
      st.success(f'Customer will not churn with probability of: {(1 - churnProb[0]):,.2f}', icon="✅")

def main():    
  html_temp = """<div class='tableauPlaceholder' id='viz1699061119474' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;ch&#47;churningda8jt&#47;Dashboard&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='churningda8jt&#47;Dashboard' /><param name='tabs' value='yes' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;ch&#47;churningda8jt&#47;Dashboard&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1699061119474');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.minWidth='1600px';vizElement.style.maxWidth='100%';vizElement.style.minHeight='950px';vizElement.style.maxHeight=(divElement.offsetWidth*0.75)+'px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.minWidth='1600px';vizElement.style.maxWidth='100%';vizElement.style.minHeight='950px';vizElement.style.maxHeight=(divElement.offsetWidth*0.75)+'px';} else { vizElement.style.width='100%';vizElement.style.minHeight='4200px';vizElement.style.maxHeight=(divElement.offsetWidth*1.77)+'px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>"""
  components.html(html_temp, width=1700, height=1080, scrolling=True)

if __name__ == "__main__":  
  model = joblib.load("model.pkl")
  input_user()
  processing_df.input_csv()
  st.title("Tableau Dashboard")
  main()