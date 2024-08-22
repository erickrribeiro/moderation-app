import streamlit as st
from components.moderation import moderation, about


def main():
    st.header("Modelo de Moderação")
    content = st.text_area(
        label="Digite algo:",
    )
    if st.button(label="Analisar"):
        with st.spinner("Analisando mensagem..."):
            info = moderation(expression=content)
            if info.flagged:
                st.write(info)
            else:
                st.success("O conteúdo informado não precisa de moderação.")

    df = about()
    st.header("Categorias de Moderação")
    st.dataframe(df, hide_index=True)


if __name__ == "__main__":
    main()
