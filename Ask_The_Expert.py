import streamlit as st
import pandas as pd
import scipy
import scipy.stats
from scipy.stats import beta
import matplotlib.pyplot as plt
import numpy as np

app_data = pd.read_csv("app_data.csv")

st.sidebar.title("Navigation")

st.sidebar.title("FAQ")
st.sidebar.info(
    "This app is was made to display the effects of bayesian updating & to help fans predict the outcome of the NBA Finals.  \n"
)
st.sidebar.title("Credits")
st.sidebar.info(
    "A big thanks to:  \n"
    "Albert Kuo for creating nba_comeback which is the inspiration for this app & the creators of nba_api \n"
)
#"Big thanks to Albert Kuo who's app this is built off of.")

st.title("Ask The Expert!")
options = ["Athelete, NBA Expert", "NBA fan", "Casual Viewer", "First Time Watcher"]
fan_level = st.radio("I am a ______", options)
game_pick = st.radio("Who thinks the _____ are gonna win", ["Bucks", "Suns"])
certainty = st.slider("With __% certainty", 50, 100)
Quarter = st.slider("What Quarter is it?", 1, 4)
Minute = st.slider("What Minute is it?", 0, 12)
Point_Differential = st.slider("What is the point differential for the Bucks?", -20, 20)
key = str(Quarter) + str(Minute) + str(Point_Differential)
if fan_level == "Athelete, NBA Expert":
    pick_addition = (.01 *certainty * 28) // 1
    pick_not = 28 - pick_addition
if fan_level == "NBA fan":
    pick_addition = (.01*certainty * 8) // 1
    pick_not = 8 - pick_addition
if fan_level == "Casual Viewer":
    pick_addition = (.01*certainty * 4) // 1
    pick_not = 4 - pick_addition

if fan_level == "First Time Watcher":
    pick_addition = (.01* certainty * 2) // 1
    pick_not = int(1 - pick_addition)

if game_pick == "Bucks":
    left = pick_addition
    right = pick_not
else:
    right = pick_addition
    left = pick_not

if Point_Differential == 0:
    Wins = 50
    Losses = 50
    VariantA = beta(Wins + left, Losses + right)
else:
    Wins = app_data[app_data["key"] == key]
    Losses = Wins["Losses"]
    Wins = Wins["Wins"]
    if Quarter < 4:
        Wins = Wins + 1
        Losses = Losses + 1
    VariantA = beta(Wins + left, Losses + right)
st.write(left, right)
x = np.linspace(VariantA.ppf(0.01),
                VariantA.ppf(0.99), 100)
figure = plt.figure()
plt.plot(x, VariantA.pdf(x),
       'r-', lw=5, alpha=0.6, label='VariantA')
st.write("There is a " + str(int(VariantA.ppf(.025)*100)) + "% to " + str(int(VariantA.ppf(.975)*100)) +  "% chance the Bucks will win")
st.pyplot(figure)
