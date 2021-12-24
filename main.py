import streamlit as st
from utils import *


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
    
    button2 = None
    if not realisation:
        placeholder_sql = """SELECT * FROM realisations 
JOIN intonations using(intonation_id) 
WHERE intonations.intonation='statement'"""
        own_query = st.text_area(label='Own SQL query:',
                                 placeholder=placeholder_sql)
        button2 = st.button('Execute', key='2')
    if button == 1:
        st.subheader('Search Results:')
        # exact formula search 
        if realisation:
            cur.execute("""
                WITH found_formulas AS (
                    SELECT formula_id, formula, language
                    FROM formulas
                    LEFT JOIN languages
                    ON formulas.language_id = languages.language_id
                    WHERE formula = %s
                   ), inner_structs AS (
                    SELECT realisation_id, CONCAT(inner_structure_type, ': ', inner_structure_subtype) AS type
                    FROM realisation2inner_structure
                    LEFT JOIN inner_structure_types
                    ON realisation2inner_structure.inner_structure_type_id = inner_structure_types.inner_structure_type_id
                    LEFT JOIN inner_structure_subtypes
                    ON realisation2inner_structure.inner_structure_subtype_id = inner_structure_subtypes.inner_structure_subtype_id
                    GROUP BY realisation_id, type
                   ), full_lemmas AS (
                    SELECT realisation_id, string_agg(lemma, ' ') AS lemmatized
                    FROM realisation2lemma
                    LEFT JOIN lemmas
                    ON realisation2lemma.lemma_id = lemmas.lemma_id
                    GROUP BY realisation_id
                   ), full_sem AS (
                    SELECT realisation_id, primary_sem, string_agg(additional_sem, ' | ') AS add_sem
                    FROM semantics
                    LEFT JOIN primary_semantics
                    ON semantics.primary_sem_id = primary_semantics.primary_sem_id
                    LEFT JOIN additional_semantics
                    ON semantics.additional_sem_id = additional_semantics.additional_sem_id
                    GROUP BY realisation_id, primary_sem
                   ), source_constr AS (
                    SELECT сonstruction_id, construction, construction_syntax, intonation AS sc_intonation
                    FROM source_constructions
                    LEFT JOIN intonations
                    ON source_constructions.intonation_id = intonations.intonation_id
                   ), sa AS (
                    SELECT realisation_id, string_agg(speech_acts.speech_act, ' | ') AS speech_act,
                    string_agg(speech_acts_1.speech_act, ' | ') AS speech_act_1
                    FROM (SELECT * FROM speech_acts) AS speech_acts_1
                    RIGHT JOIN realisation2speech_acts
                    ON realisation2speech_acts.speech_act_1_id = speech_acts_1.speech_act_id
                    LEFT JOIN speech_acts
                    ON realisation2speech_acts.speech_act_id = speech_acts.speech_act_id
                    GROUP BY realisation_id
                   )
                SELECT formula, language, string_agg(CONCAT(realisation, '\n', full_gloss, '\n', 
                lemmatized, '\n\n', examples), '+'), type, primary_sem, string_agg(add_sem, ' | '), intonation, 
                construction, construction_syntax, sc_intonation, structure, speech_act, speech_act_1
                FROM realisations
                JOIN found_formulas
                ON realisations.formula_id = found_formulas.formula_id
                LEFT JOIN inner_structs ON realisations.realisation_id = inner_structs.realisation_id
                LEFT JOIN full_lemmas ON realisations.realisation_id = full_lemmas.realisation_id
                LEFT JOIN full_sem ON realisations.realisation_id = full_sem.realisation_id
                LEFT JOIN intonations ON realisations.intonation_id = intonations.intonation_id
                LEFT JOIN source_constr ON realisations.source_constr_id = source_constr.сonstruction_id
                LEFT JOIN sa ON realisations.realisation_id = sa.realisation_id
                LEFT JOIN structures ON realisations.structure_id = structures.structure_id
                GROUP BY language, formula, type, primary_sem, intonation, construction,
                construction_syntax, sc_intonation, structure, speech_act, speech_act_1
                """, (realisation,))
        else:
            ###########################
            #   TO DO: MAIN SEARCH    # 
            ###########################
        results = cur.fetchall()
        conn.close()
        if results:
            print_results(results)
        else:
            st.text('Nothing found :(')
    else:
    if button2 == 1:
        if 'select' in own_query.lower():
            cur.execute(own_query)
            results = cur.fetchall()
            st.dataframe(data=own_query_results(results))
        else:
            try:
                cur.execute(own_query)
                st.text("Query Succeeded")
            except:
                st.text("Query Failed :(")
            conn.commit()

            
def main():
    search()

    
if __name__ == '__main__':
    main()
