import streamlit as st

def search():
    col1, col2 = st.columns([2, 8])
    with col2:
        st.header('Brand New Multilingual Pragmaticon')
    with col1:
        st.image('https://github.com/vantral/pragmaticon/raw/master/static/img/logo.png')
    realisation = st.text_input('Word')
    glosses = st.multiselect('Select glosses: ', ['3sg', 'f'])
    lemmas = st.multiselect('Select lemmas', [])
    inner_structure_type = st.selectbox('Select', [1, 2])
    inner_structure_subtype = st.selectbox('Select', [])
    languages = st.selectbox('Select', [])
    button = st.button('Искать', key='1')
    if button == 1:
        st.subheader('Вот что нам удалось узнать:')


def main():
    search()

if __name__ == '__main__':
    main()
