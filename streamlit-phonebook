import streamlit as st
import numpy as np
import pandas as pd
import typing
from sqlalchemy import (
    create_engine,
    Column,
    String,
    Integer,
    Date,
    ForeignKey,
    Boolean,
    and_,
    or_,
    not_,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import query, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = "sqlite:///phonebook.db"
SQLALCHEMY_DATABASE_URL = "postgresql://XXXXXXX:XXXXXXXXX@manager1:5432/phonebook"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
session = Session()


class Contacts(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    firstname = Column(String(25))
    lastname = Column(String(25))


st.header("Phonebook")

menu_option = st.sidebar.selectbox(
    "Menu:",
    (
        "Count Contacts",
        "Search Contact",
        "New Contact",
        "All Contacts",
        "Delete Contact",
        "Update Contact",
    ),
)
# st.write('You selected:', menu_option)


##### Search for contacts
if menu_option == "Search Contact":
    st.write("You selected:", menu_option)

    search_field = st.text_input("Search:")
    print(search_field)
    if st.button("Submit"):
        print(search_field)
        results_search = session.query(Contacts).filter(
            Contacts.firstname.like(search_field)
        )
        for contact in results_search:
            st.write(contact.id, contact.firstname, contact.lastname)


##### All Contacts
if menu_option == "All Contacts":
    st.write("You selected:", menu_option)

    results_contacts = session.query(Contacts).all()
    for contact in results_contacts:
        st.write(contact.id, contact.firstname, contact.lastname)

##### New Contact
if menu_option == "New Contact":
    st.write("You selected:", menu_option)
    firstname = st.text_input("Firstname:")
    lastname = st.text_input("Lastname:")

    if st.button("Submit"):
        # new_contacts = Contacts(firstname, lastname)

        session.add(Contacts(firstname=firstname, lastname=lastname))
        session.commit()
        session.close()
        st.write(firstname, lastname)

##### Delete Contacts ########################################################################
if menu_option == "Delete Contact":
    st.write("You selected:", menu_option)

    contacts_id = st.text_input("id:")

    if st.button("Delete"):
        # results = session.query(Contacts)
        # results = results.filter(Contacts.id == contacts_id)
        # all_results = results.one()
        # session.delete(all_results)
        results = session.query(Contacts)
        results = results.filter(Contacts.id == contacts_id)
        results.delete()
        session.commit()
        session.close()


##### Update Contacts
if menu_option == "Update Contact":
    st.write("You selected:", menu_option)
    contacts_id = st.text_input("id:")
    firstname = st.text_input("Firstname:")
    lastname = st.text_input("Lastname:")
    if st.button("Update"):

        session.query(Contacts).filter(Contacts.id == contacts_id).update(
            {Contacts.firstname: firstname}
        )
        session.query(Contacts).filter(Contacts.id == contacts_id).update(
            {Contacts.lastname: lastname}
        )
        session.commit()
        session.close()
        st.write(firstname, lastname)

##### Count Contacts
if menu_option == "Count Contacts":
    st.write("You selected:", menu_option)

    results_count = session.query(Contacts).count()
    st.write(results_count)
