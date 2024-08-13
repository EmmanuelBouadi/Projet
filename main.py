import pandas as pd
import streamlit as st
import matplotlib as plt
from streamlit_extras.metric_cards import style_metric_cards

#Configuration page
st.set_page_config(
    page_title="Complaint dashbord ", 
    page_icon=":bar_chart:", 
    layout="wide")

#Mettre des entêtes ( Le logo et les titres)
def header():
    col1, col2 = st.columns([1,3])
    with col1:
        st.image("./assets/logo.png")

    with col2:
        st.header("CUSTOMER COMPLAINT DASHBOARD")
        st.subheader("Group 6 of Bootcamp")

#Mettre la barre latérale et definir ses éléments 
def sidebar(df):

    with st.sidebar:

        st.header("Filtre Dashboard")

        st.sidebar.subheader("States")

        selected_states =st.sidebar.multiselect(
            "SELECT STATES",
            options= df.state.unique(),
            default= df.state.unique()[0:3],
        )

        for selected in selected_states:

            st.write("L'Etat selectionnée est " + selected)

        df = df[df["state"].isin(selected_states)]

        return df

#Les calculs et affichage 
def metrics(df):
    nb_products  = df['product'].nunique()
    nb_complaint_id = df['complaint_id'].nunique()
    nb_channels = df['submit_via'].nunique()
    nb_issues = df['issue'].nunique()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(label="Total Products", value=nb_products, delta="All products")
    col2.metric(label="Total Complaints", value=nb_complaint_id, delta="All complaints")
    col3.metric(label="Total channels", value=nb_channels, delta="All channels")
    col4.metric(label="Total issues", value=nb_issues, delta="All issue")

    style_metric_cards()

df = pd.read_excel("./datasets/complaints.xlsx")


df.rename(columns={
    "Complaint ID": "complaint_id",
    "Submitted via": "submit_via",
    "Date submitted": "date_submit",
    "Date received": "date_recieve",
    "State": "state",
    "Product": "product", 
    "Sub-product": "sub_product",
    "Issue": "issue",
    "Sub-issue": "sub_issue",
    "Company public response": "company_public_response",
    "Company response to consumer": "company_response_to_consumer",
    "Timely response?": "timely_response",}, inplace=True)

header()

df_filtered = sidebar(df)

metrics(df_filtered)

#Afficher les graphiques 
col1, col2 = st.columns(2)

with col1: 
    complaints_by_submit = df_filtered.groupby(by="submit_via")['complaint_id'].count()
    st.text("Canneaux les plus utilisés")
    st.bar_chart(complaints_by_submit, color="#ffaa00")

with col2:
    st.text("Nombre de plaintes par produits")
    complaints_by_products = df_filtered.groupby(by="product")['complaint_id'].count()
    st.bar_chart(complaints_by_products)




