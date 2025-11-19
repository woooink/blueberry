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
    {"id": "
