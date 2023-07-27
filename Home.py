import streamlit as st
from PIL import Image


#icone = Image.open('icone.png')

st.set_page_config(
    page_title="Viabilidade",
    page_icon="",
    layout="wide")

#st.image(Image.open("icone.png"), width=180)


import streamlit as st
import pandas as pd
import numpy as np

def calcular_pesos(matriz_comparacao):
    # Normaliza a matriz de comparação
    matriz_normalizada = matriz_comparacao / matriz_comparacao.sum(axis=0)
    # Calcula os pesos dos critérios
    pesos = matriz_normalizada.mean(axis=1)
    return pesos

def calcular_pontuacao_agregada(ponderacao_criterios, matriz_alternativas):
    # Calcula a matriz ponderada das alternativas
    matriz_ponderada = np.dot(matriz_alternativas, ponderacao_criterios)
    return matriz_ponderada

def classificar_alternativas(pontuacao_agregada, alternativas, limiar):
    ranking = pd.Series(pontuacao_agregada, index=alternativas)
    ranking_sorted = ranking.sort_values(ascending=False)

    # Verifica se cada alternativa é viável ou não com base no limiar
    viabilidade = ranking_sorted > limiar
    ranking_sorted = pd.concat([ranking_sorted, viabilidade.rename("Viável")], axis=1)

    return ranking_sorted

def main():
    st.title("Modelo de Apoio à Decisão de Viabilidade de Soluções")

    # Inserir os critérios e as alternativas
    criterios = critérios = [
    "Alinhamento Estratégico",
    "Impacto Financeiro",
    "Viabilidade Técnica",
    "Impacto no Cliente",
    "Riscos Associados",
    "Inovação e Diferenciação",
    "Tempo de Retorno"
]
    alternativas=[]
    n_alter = st.number_input("Nº de Soluções",1,step = 1)
    for i in range(n_alter):
        alternativas.append(st.text_input(f"Solução {i+1}"))

    if not criterios or not alternativas:
        st.warning("Por favor, insira os critérios e as alternativas.")
        return


    # Criar um DataFrame para a matriz de comparação dos critérios
    with st.expander("Matriz de Comparação de Critérios"):
        st.subheader("Matriz de Comparação de Critérios")
        matriz_comparacao_criterios = pd.DataFrame(index=criterios, columns=criterios, dtype=float)

        lis_Pes_Cri = [2, 7, 4, 6, 5, 7, 8, 7, 5, 8, 7, 3, 4, 4, 4, 8, 6, 6, 3, 5, 7]
        cont_Crit = 0
        for i in range(len(criterios)):
            for j in range(i, len(criterios)):
                if i == j:
                    matriz_comparacao_criterios.iloc[i, j] = 1.0
                else:
                    matriz_comparacao_criterios.iloc[i, j] = st.slider(
                        f"{criterios[i]} vs {criterios[j]}", 1, 9, lis_Pes_Cri[cont_Crit])
                    matriz_comparacao_criterios.iloc[j, i] = 1.0 / matriz_comparacao_criterios.iloc[i, j]
                    cont_Crit += 1
        #st.dataframe(matriz_comparacao_criterios)
        # Calcula os pesos dos critérios
        pesos_criterios = calcular_pesos(matriz_comparacao_criterios.values)
        st.dataframe(pd.DataFrame(pesos_criterios, index = criterios,columns=["Pesos"]), use_container_width=True)


    # Criar um DataFrame para a matriz de comparação das alternativas
    st.subheader("Matriz de Comparação de Alternativas")
    matriz_comparacao_alternativas = pd.DataFrame(index=alternativas, columns=criterios, dtype=float)
    
    df = pd.DataFrame(matriz_comparacao_alternativas)
    matriz_comparacao_alternativas = st.data_editor(df, num_rows="dynamic")



    # Calcula a pontuação agregada das alternativas
    pontuacao_agregada = calcular_pontuacao_agregada(pesos_criterios, matriz_comparacao_alternativas.values)

    # Definir o limiar para viabilidade das alternativas
    with st.expander("Limiar para viabilidade"):
        limiar = st.slider("Defina o limiar para viabilidade (0 a 1)", 0.0,10.0, 5.5)


    # Classifica as alternativas por ordem de viabilidade (maior pontuação)
    ranking_alternativas = classificar_alternativas(pontuacao_agregada, alternativas,limiar)

    st.subheader("Resultado do Modelo de Apoio à Decisão")
    st.write(ranking_alternativas)

if __name__ == "__main__":
    main()
