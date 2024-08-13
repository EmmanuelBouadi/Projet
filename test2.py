import pandas as pd
import streamlit as st
import matplotlib as plt
from streamlit_extras.metric_cards import style_metric_cards
import plotly.express as px

#Configuration page
st.set_page_config(
    page_title="Complaint dashbord ", 
    page_icon=":bar_chart:", 
    layout="wide")

#Lire le fichier excel
df = pd.read_excel("./datasets/complaints.xlsx")

#Renommer les entêtes des differentes colonnes
df.rename(columns={
    "Complaint ID": "complaint_id",
    "Submitted via": "channel",
    "Date submitted": "date_submit",
    "Date received": "date_recieve",
    "State": "state",
    "Product": "product", 
    "Sub-product": "sub_product",
    "Issue": "issue",
    "Sub-issue": "sub_issue",
    "Company public response": "public_response",
    "Company response to consumer": "response",
    "Timely response?": "timely_response",}, inplace=True)

#Titre et logo
def header():
    col1, col2 = st.columns([1,3])
    with col1:
        st.image("./assets/logo.png")

    with col2:
        st.header("CUSTOMER COMPLAINT DASHBOARD")
        st.subheader("Group 6 of Bootcamp")

header()

#Afficher les elements sur la barre laterale (les filtres)
state = st.sidebar.multiselect(
    "SELECT STATES",
    options= df.state.unique(),
    default= df.state.unique()[0:3],
)

channel = st.sidebar.multiselect(
    "SELECT CHANNEL",
    options= df.channel.unique(),
    default= df.channel.unique()[0:3],
)

response = st.sidebar.multiselect(
    "SELECT RESPONSES",
    options= df.response.unique(),
    default= df.response.unique()[0:3],
)

#Permettre aux filtres d'agir sur les autres elements
df_filtered = df.query(
    "state == @state and channel == @channel and response == @response"
)

#Afficher des metrics
def metrics(df):
    nb_products  = df['product'].nunique()
    nb_complaint_id = df['complaint_id'].nunique()
    nb_channels = df['channel'].nunique()
    nb_issues = df['issue'].nunique()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(label="Total Products", value=nb_products, delta="All products")
    col2.metric(label="Total Complaints", value=nb_complaint_id, delta="All complaints")
    col3.metric(label="Total channels", value=nb_channels, delta="All channels")
    col4.metric(label="Total issues", value=nb_issues, delta="All issue")

    style_metric_cards()

metrics(df_filtered)

st.dataframe(df)

#Ajouter un nouveau grand titre avec son icone
st.title(":bar_chart: Complaints Graph")
st.markdown("##")

#TOP KPI
nb_products  = df['product'].nunique()
nb_complaint_id = df['complaint_id'].nunique()
nb_channels = df['channel'].nunique()
nb_issues = df['issue'].nunique()
delai = df['date_submit']-df['date_recieve']
delai_moyen = delai.mean

#Faire des graphique (ici c'est bar_chart)
col1, col2 = st.columns(2)

with col1: 
    complaints_by_submit = df_filtered.groupby(by="channel")['complaint_id'].count()
    st.text("Canneaux les plus utilisés")
    st.bar_chart(complaints_by_submit, color="#ffaa00")

with col2:
    st.text("Nombre de plaintes par produits")
    complaints_by_products = df_filtered.groupby(by="product")['complaint_id'].count()
    st.bar_chart(complaints_by_products)

                                                                                                                                                                                                                                                                   