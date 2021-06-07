import streamlit as st
import pandas as pd
import altair as alt
import streamlit.components.v1 as components


#lista de emotivons
# https://raw.githubusercontent.com/omnidan/node-emoji/master/lib/emoji.json
st.set_page_config(page_title='Grupo de Python - Visualização de dados', page_icon=':moneybag', layout='wide', )

#pega o dataset completo
data = pd.read_csv('data.csv', sep=";", quotechar='"', dtype='unicode')
# data.info()
data['Valor FOB (US$)'] = (data['Valor FOB (US$)'].astype(str).astype('int64'))

# identificando os estados existentes
todos_estados = data['UF do Produto'].unique().tolist()
todos_estados.sort()

# função para auxiliar na normalização do valor
def f(s):
    return s/s.max()

def funEstadoEscolhido(tabela, estados):
    umEstado = st.selectbox('Choose on state to compare', (estados), index=0 )
    if umEstado != '':
        data_um_estado = data[data['UF do Produto'] == umEstado]
        anoValorUmEstado = data_um_estado.groupby(['Ano'],as_index=False)['Valor FOB (US$)'].agg('sum')

        # prepara a informação do estado escolhido
        max = anoValorUmEstado['Valor FOB (US$)'].max()
        # print(max)
        # cria uma coluna do Brasil
        tabela['FOB ' + umEstado] = anoValorUmEstado['Valor FOB (US$)'].apply(lambda x: x/max)
        # st.dataframe(tabela)
    return tabela



def main():
    st.title("Grupo de Python - Visualização de dados com Streamlit")
    st.subheader("International Trade Monitor for Brazil")
    st.subheader("Trajectory of Brazilian states exports between 1997 to 2020")

    # apresentação do gráfico completo
    anoEstado = data.groupby(['UF do Produto'],as_index=False)['Valor FOB (US$)'].agg('sum')
    # criando um gráfico geral
    c = alt.Chart(anoEstado).mark_circle().encode(
        x='UF do Produto', y='Valor FOB (US$)')
    st.altair_chart(c, use_container_width=True)

    # outros modelos de gráficos    
    # st.line_chart(data=anoEstado, use_container_width=True)
    # fig, ax = plt.subplots()
    # ax.hist(anoEstado, bins=26)
    # st.pyplot(fig)

    # inicia a distribuição por estado
    st.subheader('Total by state')
    # cria 2 colunas
    col1, col2 = st.beta_columns((3,8))
    
    estados = ['All']
    soEstados = ['']
    for i in todos_estados:
        estados.append(i)
        soEstados.append(i)
    estado = col1.radio('State', (estados), index=0 )
    if estado == 'All':
        data_estado = data.copy()
    else:
        data_estado = data[data['UF do Produto'] == estado]

    anoValor = data_estado.groupby(['Ano'],as_index=False)['Valor FOB (US$)'].agg('sum')  
    # st.dataframe(anoValor)  
    grupoValor = data_estado.groupby(['Descrição CGCE Nível 1'], as_index=False)['Valor FOB (US$)'].agg('sum')

    # criando um gráfico de ano x valor por estado ou geral
    c = alt.Chart(anoValor).mark_circle().encode(
        x='Ano', y='Valor FOB (US$)')
    col2.altair_chart(c, use_container_width=True)

    # criando um gráfico de ano x tipo por estado ou geral
    c = alt.Chart(grupoValor).mark_circle().encode(
        x='Descrição CGCE Nível 1', y='Valor FOB (US$)')
    col2.altair_chart(c, use_container_width=True)


    st.subheader('Comparing Brazil with one state (data normalized)')
    # fazendo comparação entre o global e um estado
    # pega o maior valor do geral
    max = anoValor['Valor FOB (US$)'].max()
    # print(max)
    # cria uma coluna do Brasil
    anoValor['FOB Brazil'] = anoValor['Valor FOB (US$)'].apply(lambda x: x/max)
    # st.dataframe(anoValor)
    anoValor = funEstadoEscolhido(anoValor, soEstados)
    # criando um gráfico comparativo entre Brasil e um estado
    # st.dataframe(anoValor)
    anoValor.drop('Valor FOB (US$)', inplace=True, axis='columns')
    anoValor.set_index('Ano', inplace = True)
    st.line_chart(anoValor)

    components.html("""<hr style="height:5px;border:none;color:#333;background-color:#333;" /> """)
    st.write("Git: https://github.com/htsnet/international-trade-monitor-for-brazil")

if __name__ == '__main__':
	main() 