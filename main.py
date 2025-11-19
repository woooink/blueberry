import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="BR 키오스크", page_icon="🍦")

st.title("🍦 베스킨라빈스 키오스크")
st.markdown("어서 오세요! 주문을 천천히 도와드릴게요 😊")

# ----------------------
# 1. 이용 방식 선택
# ----------------------
st.header("1️⃣ 이용 방법을 선택해주세요")

dine_option = st.radio(
    "매장에서 드시겠어요, 포장해 가시겠어요?",
    ("매장에서 먹고 갈게요 🪑", "포장해서 가져갈게요 🛍️"),
)

# ----------------------
# 2. 용기 선택
# ----------------------
st.header("2️⃣ 용기를 선택해주세요 🍨")

container_info = {
    "싱글컵 (최대 1가지 맛)": {"scoops": 1, "price": 3500},
    "더블컵 (최대 2가지 맛)": {"scoops": 2, "price": 6500},
    "파인트 (최대 3가지 맛)": {"scoops": 3, "price": 8600},
    "쿼터 (최대 4가지 맛)": {"scoops": 4, "price": 11800},
}

container = st.selectbox(
    "원하시는 용기를 골라주세요 😊",
    list(container_info.keys())
)

max_scoops = container_info[container]["scoops"]
base_price = container_info[container]["price"]

st.markdown(
    f"➡️ 이 용기에는 **최대 {max_scoops}가지 맛**까지 담으실 수 있어요. "
    f"(그 이하로 선택하셔도 됩니다 😉)"
)

# ----------------------
# 2-1. 담을 맛 개수 선택 (이하값으로)
# ----------------------
st.subheader("2-1️⃣ 담을 아이스크림 맛 개수 선택 ✨")

scoop_count = st.slider(
    "몇 가지 맛을 담을까요?",
    min_value=1,
    max_value=max_scoops,
    value=max_scoops,
    help="용기에 담을 아이스크림 맛의 종류 수를 선택해주세요."
)

# ----------------------
# 3. 아이스크림 맛 선택
# ----------------------
st.header("3️⃣ 아이스크림 맛을 골라주세요 😋")

flavors = [
    "바닐라", "초콜릿", "민트초코", "뉴욕치즈케이크", "딸기",
    "쿠키앤크림", "슈팅스타", "아몬드봉봉",
    "베리베리스트로베리", "이상한나라의솜사탕"
]

selected_flavors = []
for i in range(scoop_count):
    flavor = st.selectbox(
        f"{i + 1}번째 맛을 선택해주세요 🍧",
        flavors,
        key=f"flavor_{i}"
    )
    selected_flavors.append(flavor)

# ----------------------
# 4. 최종 가격 & 결제 수단
# ----------------------
st.header("4️⃣ 결제 정보를 확인해주세요 💳")

st.markdown("### 🧾 주문 금액 안내")
st.markdown(f"**총 결제 금액: {base_price:,}원** 입니다.")

payment_method = st.radio(
    "결제 수단을 선택해주세요:",
    ("현금 결제 💵", "카드 결제 💳")
)

# ----------------------
# 5. 주문 완료 버튼
# ----------------------
if st.button("✅ 이대로 주문할게요!"):
    st.success("주문이 완료되었습니다! 주문해 주셔서 감사합니다 🥰")
    st.markdown("### 📦 주문 내역")
    st.markdown(f"- 이용 방법: **{dine_option}**")
    st.markdown(f"- 용기: **{container}**")
    st.markdown(f"- 선택한 맛({scoop_count}가지): **{', '.join(selected_flavors)}**")
    st.markdown(f"- 결제 수단: **{payment_method}**")
    st.markdown("맛있게 드시고, 달콤한 시간 보내세요 🍦✨")
