from kiwipiepy import Kiwi
from wordcloud import WordCloud
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import pandas as pd
import streamlit as st

st.sidebar.title('Word Cloud 생성하기')
text = st.sidebar.text_area('긴 글을 입력하세요')
create_button = st.sidebar.button("Word Cloud 생성")

font_path = os.path.join(os.getcwd(), "customFonts/NanumGothic-Regular.ttf")

st.header('Word Cloud')
st.markdown('Word Cloud는 글에 포함된 단어의 빈도에 따라 색과 크기를 다르게 하여 시각화하는 방법입니다.')
st.markdown('왼쪽에서 입력창에 긴 글을 입력하고 **Word Cloud 생성** 버튼을 누르면 Word Cloud와 명사들의 빈도표가 생성되고 이미지를 다운로드할 수 있습니다.명사를 추출하는 기능이 완벽하지 않음을 이해해 주기 바랍니다.')

if create_button:
    kiwi = Kiwi()

    def analyze_text(text):  # 텍스트의 형태소 분석 결과를 반환
        result = kiwi.analyze(text)
        return result

    def extract_nouns(text):  # 형태소 분석 결과에서 명사를 추출
        nouns = []
        result = analyze_text(text)
        for token, pos, _, _ in result[0][0]:
            if len(token) != 1 and (pos.startswith('N') or pos.startswith('SL')):
                nouns.append(token)
        return nouns

    nouns = extract_nouns(text)

    words = [n for n in nouns if len(n) > 1]  # 단어의 길이가 1개인 것은 제외

    c = Counter(words) # 단어별 빈도의 딕셔너리
    wc = WordCloud(font_path=font_path, background_color = 'white', width=400, height=400, 
               scale=2.0, max_font_size=250, max_words=408)
    gen = wc.generate_from_frequencies(c)
    plt.figure(figsize=(10,10))
    plt.axis('off')
    plt.imshow(gen)  # useless

    save_path = 'wc.png'
    gen.to_file(save_path)    
    st.image(save_path)

    st.header('단어별 빈도')
    df = pd.DataFrame(c.items(), columns=['단어', '빈도']) 
    st.dataframe(df.sort_values(by=['빈도'], axis=0, ascending=False), hide_index=True)
    
    # 성공 문구 
    st.sidebar.success("생성됨!")
