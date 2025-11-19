import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 불러오기
df = pd.read_csv("countriesMBTI_16types.csv")

st.title("🌍 국가별 MBTI 비율 대시보드")

# 국가 선택
country_list = df["Country"].sort_values().tolist()
selected_country = st.selectbox("국가를 선택하세요", country_list)

# 선택한 국가의 데이터 추출
row = df[df["Country"] == selected_country].iloc[0]
mbti_values = row.drop("Country")

# 정렬하여 1등 MBTI 찾기
sorted_mbti = mbti_values.sort_values(ascending=False)
top_type = sorted_mbti.index[0]

# 색상 처리: 1등 빨간색, 나머지 파란 계열 그라데이션
colors = []
base_colors = px.colors.sequential.Blues_r  # 연한 → 진한 파란색

for mbti in sorted_mbti.index:
    if mbti == top_type:
        colors.append("red")
    else:
        # MBTI 개수(15개)를 그라데이션에 매핑
        idx = list(sorted_mbti.index).index(mbti)
        color_idx = int((idx / 15) * (len(base_colors) - 1))
        colors.append(base_colors[color_idx])

# Plotly 그래프 생성
fig = px.bar(
    x=sorted_mbti.index,
    y=sorted_mbti.values,
    labels={"x": "MBTI 유형", "y": "비율"},
    title=f"{selected_country} MBTI 유형 비율",
)

# 색 적용
fig.update_traces(marker_color=colors)

# 그래프 출력
st.plotly_chart(fig, use_container_width=True)
