import streamlit as st

from src.groq import get_groq_completions
from src.ner import NaturalEntityRecognizer
from src.wiki import search_wikipedia


PROMPT_TEMPLATE = """
Tu es un journaliste senior qui aime rétablir la vérité dans les informations.
Répond à la question en français et dit que tu ne sais pas si tu n'as pas l'information. Tu peux t'aider du contexte suivant, qui provient directement de Wikipedia, pour appuyer tes propos :

{context}

Question :

{question}
"""


# Streamlit interface
def main():
    # Intilialisation des variables
    ner = NaturalEntityRecognizer('Clemnt73/RoBERTa-ner')
    wiki = []

    # Initiatilisation de streamlit
    st.title("✅ Fake News Verifier ✅")
    user_content = st.text_input("Votre question", value="François Mitterand a t-il été avocat ?")

    for keyword in ner(user_content):
        wiki.append(search_wikipedia(keyword))

    # Partie BDD vectorielle
    # ...
    try:
        result = wiki[0]
    except IndexError:
        result = ''

    # Partie formatage du prompt
    if result != '':
        user_content = PROMPT_TEMPLATE.format(
            context=result,
            question=user_content
        )

    print(user_content)

    if st.button("Vérifier"):
        if not user_content:
            st.warning("Rentrez un mot clé.")
            return
        with st.spinner('Chargement en cours...'):
            generated_titles = get_groq_completions(user_content)
        st.success("Réponses générés!")

        # Display the generated titles
        st.markdown("### Réponses:")
        st.text_area("", value=generated_titles, height=200)


if __name__ == "__main__":
    main()
