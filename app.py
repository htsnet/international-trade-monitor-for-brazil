import streamlit as st
import pandas as pd
import altair as alt
import streamlit.components.v1 as components


    #lista de emotivons
    # https://raw.githubusercontent.com/omnidan/node-emoji/master/lib/emoji.json
st.set_page_config(page_title='Grupo de Python - Visualização de dados', page_icon=':moneybag', layout='centered', )

def main():
    st.title("Grupo de Python - Visualização de dados com Streamlit")
    st.subheader("International Trade Monitor for Brazil")
    st.subheader("Trajectory of Brazilian states exports between 1997 to 2020")

    #pega o dataset completo
    data = pd.read_csv('data.csv', sep=";", quotechar='"', dtype='unicode')
    # data.info()
    data['Valor FOB (US$)'] = (data['Valor FOB (US$)'].astype(str).astype('int64'))
    # data.info()
    # st.table(data=data[0:10])
    # prepara a tela para 2 colunas

    # apresentação do gráfico completo
    anoEstado = data.groupby(['UF do Produto'],as_index=False)['Valor FOB (US$)'].agg('sum')
    # print(anoEstado)

    c = alt.Chart(anoEstado).mark_circle().encode(
        x='UF do Produto', y='Valor FOB (US$)')

    st.altair_chart(c, use_container_width=True)

    st.subheader('Total by state')
    col1, col2 = st.beta_columns((3,8))

    todos_estados = data['UF do Produto'].unique().tolist()
    todos_estados.sort()
    estados = ['All']
    for i in todos_estados:
        estados.append(i)
    estado = col1.radio('State', (estados), index=0 )
    if estado == 'All':
        data_estado = data.copy()
    else:
        data_estado = data[data['UF do Produto'] == estado]

    anoValor = data_estado.groupby(['Ano'],as_index=False)['Valor FOB (US$)'].agg('sum')    
    grupoValor = data_estado.groupby(['Descrição CGCE Nível 1'], as_index=False)['Valor FOB (US$)'].agg('sum')

    c = alt.Chart(anoValor).mark_circle().encode(
        x='Ano', y='Valor FOB (US$)')
    col2.altair_chart(c, use_container_width=True)


    c = alt.Chart(grupoValor).mark_circle().encode(
        x='Descrição CGCE Nível 1', y='Valor FOB (US$)')
    col2.altair_chart(c, use_container_width=True)
    

    components.html("""<hr style="height:5px;border:none;color:#333;background-color:#333;" /> """)
    st.write("Git: https://github.com/htsnet/international-trade-monitor-for-brazil")

if __name__ == '__main__':
	main() 