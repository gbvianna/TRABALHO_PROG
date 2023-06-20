import streamlit as st
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import matplotlib.pyplot as plt
from collections import Counter

def fazer_requisicao(url):
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(url)
        html = driver.page_source
        driver.quit()
        return html
    except Exception as e:
        st.error(f"Ocorreu um erro durante a requisição: {e}")
        return None

def extrair_dados(html):
    soup = BeautifulSoup(html, 'html.parser')
    manchetes = soup.find_all('div', attrs={'class': 'container__headline'})

    palavras = []
    for manchete in manchetes:
        texto = manchete.get_text()
        palavras_chave = texto.split()
        palavras.extend(palavras_chave)

    return palavras

def main():
    st.title("Raspagem de Dados do Site")

    url = st.text_input("Digite a URL do site:")
    if url:
        conteudo_html = fazer_requisicao(url)
        if conteudo_html:
            dados_coletados = extrair_dados(conteudo_html)

            opcao = st.selectbox("Escolha uma opção:", ["Processar palavras mais frequentes", "Contar ocorrência de uma palavra específica", "Visualizar todas as palavras coletadas"])

            if opcao == "Processar palavras mais frequentes":
                if dados_coletados:
                    contagem_palavras = Counter(dados_coletados)
                    palavras_comuns = contagem_palavras.most_common(10)
                    if palavras_comuns:
                        x, y = zip(*palavras_comuns)
                        plt.bar(x, y)
                        plt.xlabel('Palavras')
                        plt.ylabel('Contagem')
                        plt.title('Contagem de Palavras mais Frequentes nas Manchetes')
                        plt.xticks(rotation=45)
                        st.pyplot(plt)
                    else:
                        st.warning("Não foram encontradas palavras mais frequentes para processar.")
                else:
                    st.warning("Não foram encontradas palavras para processar.")

            elif opcao == "Contar ocorrência de uma palavra específica":
                if dados_coletados:
                    palavra = st.text_input("Digite uma palavra para contar sua ocorrência:")
                    ocorrencias = dados_coletados.count(palavra)
                    st.success(f"A palavra '{palavra}' ocorreu {ocorrencias} vezes nas manchetes.")
                else:
                    st.warning("Não foram encontradas palavras para contar ocorrências.")

            elif opcao == "Visualizar todas as palavras coletadas":
                if dados_coletados:
                    st.subheader("Palavras coletadas:")
                    for palavra in dados_coletados:
                        st.write(palavra)
                else:
                    st.warning("Não foram encontradas palavras coletadas.")

if __name__ == "__main__":
    main()
