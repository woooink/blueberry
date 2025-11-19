import streamlit as st

st.set_page_config(page_title="BR 키오스크", page_icon="🍨")

st.title("🍦 베스킨라빈스 키오스크")
st.write("안녕하세요! 주문을 도와드릴게요 😊")

# ----------------------
# 1. 매장/포장 선택
# ----------------------
st.header("1. 드시고 가시나요? 🏠 / 포장해 가시나요? 🎁")
dine_option = st.radio(
    "선택해주세요:",
    ["매장에서 먹기", "포장해서 가기"]
)

# ----------------------
# 2. 용기 선택
# ----------------------
st.header("2. 용기를 선택해주세요 🥄")
container = st.selectbox(
    "용기 종류",
    ["싱글컵 (1가지 맛)", "더블컵 (2가지 맛)", "파인트 (3가지 맛)", "쿼터 (4가지 맛)"]
)

# 용기별 가능 맛 개수
capacity = {
    "싱글컵 (1가지 맛)": 1,
    "더블컵 (2가지 맛)": 2,
    "파인트 (3가지 맛)": 3,
    "쿼터 (4가지 맛)": 4
}

# 가격표
price_table = {
    "싱글컵 (1가지 맛)": 3500,
    "더블컵 (2가지 맛)": 6500,
    "파인트 (3가지 맛)": 8600,
    "쿼터 (4가지 맛)": 11800
}

count = capacity[container]

# ----------------------
# 3. 아이스크림 맛 선택
# ----------------------
st.header(f"3. 아이스크림 맛을 {count}가지 선택해주세요 🍨")

flavors = [
    "바닐라", "초콜릿", "민트초코", "뉴욕치즈케이크", "딸기", "쿠키앤크림",
    "슈팅스타", "아몬드봉봉", "베리베리스트로베리", "이상한나라의솜사탕"
]

selected_flavors = []
for i in range(count):
    flavor = st.selectbox(f"{i+1}번째 맛", flavors, key=f"flavor_{i}")
    selected_flavors.append(flavor)

# ----------------------
# 4. 최종 가격 + 결제 선택
# ----------------------
st.header("4. 결제 방법을 선택해주세요 💳")

price = price_table[container]
st.write(f"### 🧾 총 결제 금액: **{price:,}원**")

payment = st.radio(
    "결제 수단",
    ["현금 결제 💵", "카드 결제 💳", "기프티콘 결제 🎟️"]
)

# ----------------------
# 5. 주문 완료
# ----------------------
if st.button("주문 완료하기 🥰"):
    st.success("주문이 완료되었습니다! 감사합니다 🙏")
    st.write(f"**주문 내역**")
    st.write(f"- 이용 방식: {dine_option}")
    st.write(f"- 용기: {container}")
    st.write(f"- 선택한 맛: {', '.join(selected_flavors)}")
    st.write(f"- 결제 방식: {payment}")
    st.write("맛있게 드세요! 🍦✨")
