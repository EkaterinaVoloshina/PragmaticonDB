import streamlit as st
import psycopg2


def connect_to_db():
    """
    Connect to database
    """
    conn = psycopg2.connect(dbname=st.secrets['DB_NAME'],
                            user=st.secrets['DB_USER'],
                            password=st.secrets['DB_PASS'],
                            host=st.secrets['DB_HOST'])

    c = conn.cursor()
    return c


def get_options(cur, table):
    """
    Get search options from db by property
    """
    query = f"""SELECT * FROM {table}"""
    cur.execute(query)
    return {key[0]: key[1] for key in cur.fetchall()}


def search():
    # display header
    col1, col2 = st.columns([2, 8])
    with col2:
        st.header('Brand New Multilingual Pragmaticon')
    with col1:
        st.image('https://github.com/vantral/pragmaticon/raw/master/static/img/logo.png')
    # connect to db
    cur = connect_to_db()
    # realisation search 
    realisation = st.text_input(
        label='Word',
        placeholder='Use the Latin script'
    )
    # display search options if realisation search is not active
    if not realisation:
        col1, col2 = st.columns([5, 5])
        with col1:
            options = get_options(cur, 'primary_semantics')
            primary_sem = st.multiselect(
                label='Pragmatics',
                options=options.keys(),
                format_func=lambda x: options[x]
            )
        with col2:
            options = get_options(cur, 'additional_semantics')
            add_sem = st.multiselect(
                label='Additional semantics',
                options=options.keys(),
                format_func=lambda x: options[x]
            )
        options = get_options(cur, 'lemmas')
        lemmas = st.multiselect(
            label='Lemma',
            options=options.keys(),
            format_func=lambda x: options[x]
        )
        col1, col2 = st.columns([5, 5])
            with col1:
                options = get_options(cur, 'glosses')
                glosses = st.multiselect(
                    label='Glosses',
                    options=options.keys(),
                    format_func=lambda x: options[x]
                )
            with col2:
                options = get_options(cur, 'languages')
                languages = st.multiselect(
                    label='Language',
                    options=options.keys(),
                    format_func=lambda x: options[x]
                )
            synt_structure = st.text_input(
                label='Syntactic Structure',
                placeholder='VERB'
            )
            col1, col2 = st.columns([5, 5])
            with col1:
                options = get_options(cur, 'inner_structure_types')
                inner_struc_type = st.multiselect(
                    label='Inner Structure',
                    options=options.keys(),
                    format_func=lambda x: options[x]
                )
                options = get_options(cur, 'structures')
                structure = st.multiselect(
                    label='Structure',
                    options=options.keys(),
                    format_func=lambda x: options[x]
                )
            with col2:
                options = get_options(cur, 'inner_structure_subtypes')
                inner_struc_subtype = st.multiselect(
                    label='Inner Structure Subtype',
                    options=options.keys(),
                    format_func=lambda x: options[x]
                )
                options = get_options(cur, 'speech_acts')
                speech_act = st.multiselect(
                    label='Speech Act',
                    options=options.keys(),
                    format_func=lambda x: options[x]
                )
            options = get_options(cur, 'intonations')
            intonations = st.multiselect(
                label='Intonation',
                options=options.keys(),
                format_func=lambda x: options[x]
            )
    button = st.button('Search', key='1')
    if button == 1:
        st.subheader('Search Results:')


def main():
    search()

if __name__ == '__main__':
    main()
