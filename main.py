import streamlit as st
from datetime import datetime
import random

# ---------------------------------------------------------
# 기본 설정
# ---------------------------------------------------------
st.set_page_config(page_title="BR 키오스크 (고급 버전)", page_icon="🍦", layout="wide")

# ---------------------------------------------------------
# 상수 정의
# ---------------------------------------------------------
CONTAINERS = [
    {"id": "single", "label": "싱글컵 (1가지 맛)", "scoops": 1, "price": 3500},
    {"id": "double", "label": "더블컵 (2가지 맛)", "scoops": 2, "price": 6500},
    {"id": "pint", "label": "파인트 (3가지 맛)", "scoops": 3, "price": 8600},
    {"id": "quarter", "label": "쿼터 (4가지 맛)", "scoops": 4, "price": 11800},
]

CONTAINER_BY_LABEL = {c["label"]: c for c in CONTAINERS}
CONTAINER_OPTIONS = [c["label"] for c in CONTAINERS]

# 아이스크림 맛 정보 (간단 태그 포함)
FLAVORS = [
    {"name": "vanilla", "label": "바닐라 🍯 (기본, 누구나 좋아해요)", "tags": ["basic", "kids", "mild"]},
    {"name": "choco", "label": "초콜릿 🍫 (진한 맛)", "tags": ["classic", "rich"]},
    {"name": "mint", "label": "민트초코 🌿 (호불호 강함)", "tags": ["fresh", "mint"]},
    {"name": "ny_cheese", "label": "뉴욕치즈케이크 🧀", "tags": ["cheese", "rich"]},
    {"name": "strawberry", "label": "딸기 🍓 (상큼 달콤)", "tags": ["fruit", "kids"]},
    {"name": "cookies", "label": "쿠키앤크림 🍪", "tags": ["cookie", "classic"]},
    {"name": "shooting_star", "label": "슈팅스타 💫 (톡톡 튀는 맛)", "tags": ["fun", "kids"]},
    {"name": "almond_bong", "label": "아몬드봉봉 🥜 (견과류 포함)", "tags": ["nut", "rich"]},
    {"name": "berry_straw", "label": "베리베리스트로베리 🍓🍓", "tags": ["fruit"]},
    {"name": "cotton_candy", "label": "이상한나라의솜사탕 🍭", "tags": ["sweet", "kids"]},
]

FLAVOR_OPTIONS = [f["label"] for f in FLAVORS]

TOPPING_OPTIONS = [
    {"id": "rainbow", "label": "레인보우 스프링클 (+500원)", "price": 500},
    {"id": "almond", "label": "아몬드 토핑 (+700원, 견과류)", "price": 700},
    {"id": "choco_syrup", "label": "초코 시럽 (+500원)", "price": 500},
]

MAX_ITEMS = 5  # 최대 메뉴 개수


# ---------------------------------------------------------
# 유틸 함수
# ---------------------------------------------------------
def init_session_state():
    if "item_count" not in st.session_state:
        st.session_state["item_count"] = 1
    if "order_confirmed" not in st.session_state:
        st.session_state["order_confirmed"] = False
    if "order_number" not in st.session_state:
        st.session_state["order_number"] = None


def get_time_based_recommendation():
    hour = datetime.now().hour
    if 10 <= hour < 12:
        return "지금은 늦은 아침 시간이네요. 가볍게 ☕ 바닐라 + 딸기 조합을 추천드려요."
    elif 12 <= hour < 15:
        return "점심 후 디저트 시간입니다. 🍫 초콜릿 + 🍓 딸기 조합으로 달콤하게 마무리해보세요."
    elif 15 <= hour < 18:
        return "간식 시간이네요. 💫 슈팅스타 + 🍭 솜사탕 같이 재미있는 맛은 어떠세요?"
    else:
        return "하루를 마무리하는 시간입니다. 🧀 뉴욕치즈케이크 + 🍪 쿠키앤크림처럼 묵직한 조합도 잘 어울려요."


def build_current_order():
    """세션 상태에 있는 값을 기반으로 현재 장바구니 내용을 구성."""
    items = []
    for i in range(st.session_state.get("item_count", 1)):
        include = st.session_state.get(f"item_{i}_include", True if i == 0 else False)
        if not include:
            continue

        container_label = st.session_state.get(f"item_{i}_container", CONTAINER_OPTIONS[0])
        container_info = CONTAINER_BY_LABEL[container_label]
        scoops = container_info["scoops"]

        flavors = []
        for j in range(scoops):
            key = f"item_{i}_flavor_{j}"
            flavor_label = st.session_state.get(key, FLAVOR_OPTIONS[0])
            flavors.append(flavor_label)

        waffle = st.session_state.get(f"item_{i}_waffle", False)

        topping_states = {}
        for topping in TOPPING_OPTIONS:
            t_key = f"item_{i}_topping_{topping['id']}"
            topping_states[topping["id"]] = st.session_state.get(t_key, False)

        # 가격 계산
        item_price = container_info["price"]
        if waffle:
            item_price += 1000
        for topping in TOPPING_OPTIONS:
            if topping_states[topping["id"]]:
                item_price += topping["price"]

        items.append(
            {
                "index": i,
                "container_label": container_label,
                "scoops": scoops,
                "flavors": flavors,
                "waffle": waffle,
                "toppings": topping_states,
                "base_price": container_info["price"],
                "price": item_price,
            }
        )
    return items


def calculate_totals(items):
    if not items:
        return 0, 0, 0

    subtotal = sum(item["price"] for item in items)

    # 간단한 할인 규칙 예시
    discount = 0
    if len(items) >= 3:
        discount += int(subtotal * 0.10)  # 3개 이상 주문 시 10% 할인
    if subtotal >= 30000:
        discount += 2000  # 3만 원 이상 주문 시 추가 2,000원 할인

    total = max(subtotal - discount, 0)
    return subtotal, discount, total


def generate_order_number():
    now = datetime.now()
    return "BR-" + now.strftime("%H%M%S") + "-" + str(random.randint(100, 999))


def describe_item(item):
    parts = [f"{item['container_label']}"]
    if item["flavors"]:
        parts.append(" / 맛: " + ", ".join(item["flavors"]))
    extra = []
    if item["waffle"]:
        extra.append("와플 변경")
    for topping in TOPPING_OPTIONS:
        if item["toppings"].get(topping["id"], False):
            extra.append(topping["label"].split("(")[0].strip())
    if extra:
        parts.append(" / 추가: " + ", ".join(extra))
    parts.append(f" / 가격: {item['price']:,}원")
    return "".join(parts)


# ---------------------------------------------------------
# 세션 초기화
# ---------------------------------------------------------
init_session_state()

# ---------------------------------------------------------
# 레이아웃: 사이드바(요약) + 본문(탭)
# ---------------------------------------------------------
with st.sidebar:
    st.title("🧾 주문 요약")
    st.caption("오른쪽에서 주문을 진행하면 이곳에서 실시간으로 금액과 구성을 확인할 수 있습니다.")

    current_items = build_current_order()
    subtotal, discount, total = calculate_totals(current_items)

    st.subheader("주문 내역")
    if not current_items:
        st.write("선택된 메뉴가 없습니다.")
    else:
        for idx, item in enumerate(current_items, start=1):
            st.write(f"**메뉴 {idx}**")
            st.write(describe_item(item))

    st.markdown("---")
    st.subheader("금액")
    st.write(f"- 주문 금액: **{subtotal:,}원**")
    st.write(f"- 할인: **-{discount:,}원**")
    st.write(f"- 결제 예정 금액: **{total:,}원**")

    st.markdown("---")
    st.subheader("오늘의 추천")
    st.write(get_time_based_recommendation())

# ---------------------------------------------------------
# 본문
# ---------------------------------------------------------
st.title("🍨 베스킨라빈스 키오스크 (고급 버전)")
st.write("천천히 선택하셔도 괜찮습니다. 안내에 따라 순서대로 선택해 주세요. 😊")

tab1, tab2, tab3 = st.tabs(["1️⃣ 이용 정보 선택", "2️⃣ 메뉴 구성하기", "3️⃣ 결제 및 주문 확정"])


# ---------------------------------------------------------
# 탭 1: 이용 정보
# ---------------------------------------------------------
with tab1:
    st.header("1. 이용 방식을 선택해 주세요 🏠 / 🎁")

    st.radio(
        "매장에서 드실까요, 포장해 가실까요?",
        ["매장에서 먹기", "포장해서 가기"],
        key="dine_option",
    )

    st.number_input(
        "함께 드시는 인원 수를 알려주세요. (본인 포함)",
        min_value=1,
        max_value=10,
        value=1,
        step=1,
        key="people_count",
    )

    st.text_input(
        "호출 시 사용할 이름 또는 별명을 적어주세요. (예: 홍길동 / 15번 등)",
        key="customer_name",
    )

    st.markdown("---")
    st.subheader("알레르기 안내 ⚠️")
    st.checkbox("알레르기가 있어요.", key="has_allergy")
    if st.session_state.get("has_allergy"):
        st.text_area(
            "드시지 못하는 재료를 간단히 적어주세요. (예: 견과류, 우유, 딸기 등)",
            key="allergy_detail",
        )
    st.info("실제 매장에서는 반드시 직원에게 알레르기 정보를 한 번 더 알려 주세요.")


# ---------------------------------------------------------
# 탭 2: 메뉴 구성
# ---------------------------------------------------------
with tab2:
    st.header("2. 아이스크림 메뉴를 구성해 주세요 🍦")

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("메뉴 추가 ➕", use_container_width=True):
            if st.session_state["item_count"] < MAX_ITEMS:
                st.session_state["item_count"] += 1
            else:
                st.warning(f"메뉴는 최대 {MAX_ITEMS}개까지 추가할 수 있습니다.")
    with col_btn2:
        if st.button("마지막 메뉴 삭제 ➖", use_container_width=True):
            if st.session_state["item_count"] > 1:
                st.session_state["item_count"] -= 1
            else:
                st.warning("메뉴는 최소 1개는 있어야 합니다.")

    st.caption("각 메뉴별로 용기, 맛, 토핑을 자유롭게 선택하실 수 있습니다.")

    # 메뉴 카드들 렌더링
    for i in range(st.session_state["item_count"]):
        with st.expander(f"메뉴 {i+1} 설정", expanded=(i == 0)):
            st.checkbox("이번 메뉴를 주문에 포함합니다.", key=f"item_{i}_include", value=True if i == 0 else st.session_state.get(f"item_{i}_include", True))

            st.selectbox(
                "용기 선택",
                CONTAINER_OPTIONS,
                key=f"item_{i}_container",
            )

            container_label = st.session_state.get(f"item_{i}_container", CONTAINER_OPTIONS[0])
            container_info = CONTAINER_BY_LABEL[container_label]
            scoops = container_info["scoops"]

            st.markdown(f"**이 용기에는 최대 {scoops}가지 맛을 담을 수 있습니다. (이하값으로 자동 제한)**")

            for j in range(scoops):
                st.selectbox(
                    f"{j+1}번째 맛 선택",
                    FLAVOR_OPTIONS,
                    key=f"item_{i}_flavor_{j}",
                )

            st.markdown("---")
            st.subheader("추가 옵션")
            st.checkbox("와플콘/와플볼로 변경 (+1,000원)", key=f"item_{i}_waffle")

            st.markdown("**토핑 추가**")
            for topping in TOPPING_OPTIONS:
                st.checkbox(
                    topping["label"],
                    key=f"item_{i}_topping_{topping['id']}",
                )

            st.caption("※ 실제 매장 가격과는 차이가 있을 수 있으며, 예시용 학습 프로그램입니다.")

    # 탭 2 하단 현재 메뉴 요약
    st.markdown("---")
    st.subheader("현재까지 선택한 메뉴 요약")
    current_items = build_current_order()
    if not current_items:
        st.write("아직 선택된 메뉴가 없습니다.")
    else:
        for idx, item in enumerate(current_items, start=1):
            st.write(f"- **메뉴 {idx}**: {describe_item(item)}")


# ---------------------------------------------------------
# 탭 3: 결제 및 주문 확정
# ---------------------------------------------------------
with tab3:
    st.header("3. 결제 방법 선택 및 주문 확정 💳")

    current_items = build_current_order()
    subtotal, discount, total = calculate_totals(current_items)

    st.subheader("결제 금액 요약")
    col1, col2, col3 = st.columns(3)
    col1.metric("주문 금액", f"{subtotal:,}원")
    col2.metric("할인", f"-{discount:,}원")
    col3.metric("결제 예정 금액", f"{total:,}원")

    if not current_items:
        st.warning("먼저 2번 탭에서 메뉴를 최소 1개 이상 선택해 주세요.")
    else:
        st.markdown("---")
        st.subheader("결제 정보 입력")

        with st.form("payment_form"):
            payment_method = st.radio(
                "결제 수단을 선택해 주세요.",
                ["현금 결제 💵", "카드 결제 💳", "기프티콘 결제 🎟️"],
                key="payment_method",
            )

            cash_amount = None
            card_last4 = None
            gift_code = None

            if payment_method == "현금 결제 💵":
                cash_amount = st.number_input(
                    "지불하실 금액을 입력해 주세요.",
                    min_value=0,
                    step=1000,
                    value=total if total > 0 else 0,
                    key="cash_amount",
                )
            elif payment_method == "카드 결제 💳":
                card_last4 = st.text_input(
                    "카드 뒷자리 4자리를 입력해 주세요. (예: 1234)",
                    max_chars=4,
                    key="card_last4",
                )
            elif payment_method == "기프티콘 결제 🎟️":
                gift_code = st.text_input(
                    "기프티콘 번호를 입력해 주세요. (예: 12-AB-34-CD)",
                    key="gift_code",
                )

            agree = st.checkbox("주문 내용을 확인했으며, 결제에 동의합니다.", key="agree_terms")

            submitted = st.form_submit_button("주문 확정하기 ✅")

        if submitted:
            errors = []

            if not current_items:
                errors.append("메뉴가 비어 있습니다. 2번 탭에서 메뉴를 선택해 주세요.")
            if total <= 0:
                errors.append("결제 금액이 0원입니다. 메뉴 및 할인 조건을 다시 확인해 주세요.")
            if not st.session_state.get("agree_terms", False):
                errors.append("결제 동의에 체크해 주세요.")

            if payment_method == "현금 결제 💵":
                if cash_amount is None or cash_amount < total:
                    errors.append("현금 결제 금액이 부족합니다.")
            elif payment_method == "카드 결제 💳":
                if not card_last4 or len(card_last4.strip()) < 4 or not card_last4.strip().isdigit():
                    errors.append("카드 뒷자리 4자리를 정확히 입력해 주세요.")
            elif payment_method == "기프티콘 결제 🎟️":
                if not gift_code or len(gift_code.strip()) < 4:
                    errors.append("기프티콘 번호를 정확히 입력해 주세요.")

            if errors:
                for e in errors:
                    st.error(e)
            else:
                st.session_state["order_confirmed"] = True
                st.session_state["order_number"] = generate_order_number()

                st.success("주문이 정상적으로 완료되었습니다. 감사합니다! 🙏")

                st.subheader("최종 주문 정보")
                order_no = st.session_state.get("order_number")
                if order_no:
                    st.write(f"- 주문 번호: **{order_no}**")

                st.write(f"- 이용 방식: {st.session_state.get('dine_option', '미선택')}")
                st.write(f"- 인원 수: {st.session_state.get('people_count', 1)}명")
                name_display = st.session_state.get("customer_name", "").strip()
                if name_display:
                    st.write(f"- 호출 이름/번호: {name_display}")

                if st.session_state.get("has_allergy"):
                    st.write("- 알레르기 정보가 있습니다. (실제 매장에서는 꼭 다시 한 번 직원에게 알려 주세요.)")

                st.markdown("---")
                st.write("**주문 내역**")
                for idx, item in enumerate(current_items, start=1):
                    st.write(f"- 메뉴 {idx}: {describe_item(item)}")

                st.write(f"**최종 결제 금액: {total:,}원**")
                st.write(f"**결제 수단: {payment_method}**")

                if payment_method == "현금 결제 💵" and cash_amount is not None:
                    change = cash_amount - total
                    st.write(f"- 받으신 금액: {cash_amount:,}원")
                    st.write(f"- 거스름돈: {change:,}원")

                st.markdown("---")
                st.write("맛있게 드시고, 좋은 하루 보내세요! 🍦✨")
