import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration de la page
st.set_page_config(page_title="Analyse des Plaintes Clients", layout="wide")

# Charger les données
@st.cache
def load_data():
    data = pd.read_excel('./datasets/complaints.xlsx')
    return data

data = load_data()

# Barre latérale pour les filtres
st.sidebar.header("Filtres")
product_filter = st.sidebar.multiselect("Produit", options=data['Product'].unique(), default=data['Product'].unique())
state_filter = st.sidebar.multiselect("État", options=data['State'].unique(), default=data['State'].unique())
date_filter = st.sidebar.date_input("Date de soumission", [])

# Application des filtres
filtered_data = data[data['Product'].isin(product_filter) & data['State'].isin(state_filter)]

if date_filter:
    filtered_data = filtered_data[filtered_data['Date received'].dt.date == pd.to_datetime(date_filter).date()]

# Titre de l'application
st.title("Analyse des Plaintes Clients")

# Afficher les données filtrées
st.write("Données filtrées", filtered_data)

# Visualisation 1: Histogramme des plaintes par produit
st.subheader("Histogramme des plaintes par produit")
fig, ax = plt.subplots()
filtered_data['Product'].value_counts().plot(kind='bar', ax=ax)
st.pyplot(fig)

# Visualisation 2: Pie chart des réponses par état
st.subheader("Diagramme circulaire des réponses par état")
fig, ax = plt.subplots()
filtered_data['Company response to consumer'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax)
ax.axis('equal')
st.pyplot(fig)

# Visualisation 3: Box plot des temps de réponse par produit
st.subheader("Box plot des temps de réponse par produit")
fig, ax = plt.subplots()
sns.boxplot(x='Product', y='Timely response?', data=filtered_data, ax=ax)
st.pyplot(fig)