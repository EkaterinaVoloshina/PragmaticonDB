import psycopg2
import streamlit as st


def connect_to_db():
    conn = psycopg2.connect(dbname=st.secrets['DB_NAME'],
                            user=st.secrets['DB_USER'],
                            password=st.secrets['DB_PASS'],
                            host=st.secrets['DB_HOST'])

    c = conn.cursor()
    return c, conn


def get_options(cur, table):
    query = f"""SELECT * FROM {table}"""
    cur.execute(query)
    return {key[0]: key[1] for key in cur.fetchall()}


def get_realisations(realisations):
    res_string = ''
    examples = []
    realisations = realisations.split('+')[:10]
    for real in realisations:
        real = real.split('\n\n')
        if len(real) == 2:
            rn, exmpl = real
        else:
            rn, exmpl = real[0], ""
        rn = rn.split('\n')
        rn = '\n\n'.join([f'**{r}**' if i == 0 else r for i, r in enumerate(rn)])
        res_string = res_string + rn + '\n\n'
        examples.append(exmpl if exmpl else '')
    examples = list(set(examples))
    if len(examples) >= 1 and examples[0]:
        examples = '\n\n**Examples:**\n\n' + '\n\n'.join(examples)
        examples = examples.replace('{', '**').replace('}', '**')
    else:
        examples = None
    return res_string, examples


def get_speech_acts(structure, sa, sa1, formula):
    out = ''
    if structure == '2':
        out += '👤 ' + sa + '\n👤 ' + formula
    elif structure == '3':
        for act in [sa1, sa, formula]:
            out += '👤 ' + act + '\n'
    return out


def print_results(results):
    # formula, language, realisations+glosses+lemmas, inner_structure, primary_sem,
    # add_sem, intonation, construction, construction_syntax, sc_intonation,
    # structure, speech_act, speech_act_1
    for i, formula in enumerate(results):
        col1, col2 = st.columns([9, 1])
        add_sem = ' | '.join(set(formula[5].split(' | '))) if formula[5] else ''
        with col1:
            header = formula[0] + (' — ' + formula[3].strip(': ') if formula[3] and
                                   formula[3].strip(': ') else '')
            st.markdown(f"""#### {header}""")
        with col2:
            st.markdown(f"#### {formula[1]}")
        card = ('Pragmatics: ' + formula[4].upper() if formula[4] else '') +\
               ('\nAdditional semantics: ' + add_sem) +\
               ('\nIntonation: ' + formula[6] if formula[6] else '')
        st.code(f"""{card}""")
        variants, examples = get_realisations(formula[2])
        if examples:
            st.markdown(f"""{examples}""")
        speech_acts = get_speech_acts(*formula[-3:], formula[0])
        if speech_acts:
            st.code(f"""{speech_acts}""")
        if variants:
            st.markdown(f"""Variants:\n\n{variants}""")
        st.markdown(f"""---""")  
        

def own_query_results(results):
    return pd.DataFrame(results)
