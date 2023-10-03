#Import Libraries
import pickle
import base64
import pandas as pd
import streamlit as st

#Setting the Page title and Page icom
st.set_page_config(page_title="Used Car Price Prediction", page_icon="App_Icon.png")

#Hiding the footer on the website
hide_footer = """
    <style>
    footer {visibility: hidden;}
    </style>
    """
#Markdown is applying the footer(hide_default_format)
st.markdown(hide_footer, unsafe_allow_html=True)

# Loading RF model from the pickle file
with open('random_forest_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Reading the car dataset
car_dataset = pd.read_csv('Cleaned Dataset.csv')

#(1) year_range_getvalid() - It extracts the minimum/maximum value of Year column from the dataset
def year_range_getvalid():
    min_year = car_dataset['Year'].min()
    max_year = car_dataset['Year'].max()
    return min_year, max_year

#(2) car_maker_and_models_getvalid() - It extracts unique car make and model from the dataset
def car_maker_and_models_getvalid():
    valid_maker = car_dataset['Make'].unique()
    valid_models = car_dataset['Model'].unique()
    return valid_maker, valid_models

#(3) car_models_for_make_and_year_get_valid - It extracts the unique car model for specific make and year from the dataset
def car_models_for_make_and_year_get_valid(make, year):
    valid_models = car_dataset[(car_dataset['Make'] == make) & (car_dataset['Year'] == year)]['Model'].unique()
    return valid_models

#(4) check_validmileage(mileage) - It checks if the mileage is +ve number or zero. If it  not a valid number or -ve it will return false.
def check_validmileage(mileage):
    try:
        mileage = float(mileage)
        return mileage >= 0
    except ValueError:
        return False

#(5) predict_car_price(year, mileage, make, car_model)- It predict the price of the car using RF.
def predict_car_price(year, mileage, make, car_model):
    input_data = pd.DataFrame({
        'Year': [year],
        'Mileage': [mileage],
        'Make': [make],
        'Model': [car_model]
    })
    try:
        predicted_price = model.predict(input_data)
        return predicted_price[0]
    except Exception as e:
        return str(e)

#(6) set_background_local_file(image_file) - It read the local image file
def set_background_local_file(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/png;base64,{encoded_string.decode()});
        background-size: cover;
        background-repeat: no-repeat;
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

if __name__ == '__main__':
    set_background_local_file('car_background2.jpg')  # It set the background for the Streamlit.

    if not hasattr(st, 'session_state'):
        st.error("Please upgrade Streamlit to use `st.session_state`!")
        st.stop()

    if not hasattr(st.session_state, 'navigate_to_predict'):
        st.session_state.navigate_to_predict = False

    if st.session_state.navigate_to_predict:
        st.title("Used Car Price Prediction")
        valid_year_range = year_range_getvalid()
        valid_makes, valid_models = car_maker_and_models_getvalid()

        year = st.selectbox("Select the car's year:", range(valid_year_range[0], valid_year_range[1] + 1))
        make = st.selectbox("Select the car's make:", valid_makes)
        valid_car_models = car_models_for_make_and_year_get_valid(make, year)
        car_model = st.selectbox("Select the car's model:", valid_car_models)
        mileage = st.text_input("Enter the car's mileage:")

        if st.button("Predict"):
            if not check_validmileage(mileage):
                popup_color = 'red'
                st.markdown(
                    f"<div style='background-color: {popup_color}; padding: 10px; border-radius: 5px; color: white;'>Error: Mileage must be a non-negative numeric value.</div>",
                    unsafe_allow_html=True
                )
            else:
                mileage = float(mileage)
                predicted_price = predict_car_price(year, mileage, make, car_model)
                if isinstance(predicted_price, (float, int)):

                    popup_color = 'green'
                    st.markdown(
                        f"<div style='background-color: {popup_color}; padding: 10px; border-radius: 5px; color: white;'>Predicted price for the car: ${predicted_price:.2f}</div>",
                        unsafe_allow_html=True
                    )

                else:
                    st.error(f"Error: Unable to calculate the predicted price. {predicted_price}")


    else:
        st.title("Welcome to Used Car Price Prediction!")
        st.write("Get the predicted price of a used car based on various features.")
        if st.button("Let's Predict the Price"):
            st.session_state.navigate_to_predict = True
            st.experimental_rerun()
