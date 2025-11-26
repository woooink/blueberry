import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta

# ---------------- 기본 설정 ----------------
st.set_page_config(
    page_title="HaToDo - 하나고 일정 관리",
    layout="wide",
)

# --------- 유틸 함수들 ---------
SUBJECT_INFO = {
    "kor": {"label": "국어", "color": "#ef4444"},
    "eng": {"label": "영어", "color": "#3b82f6"},
    "math": {"label": "수학", "color": "#22c55e"},
    "sci": {"label": "과학", "color": "#a855f7"},
    "soc": {"label": "사회", "color": "#f97316"},
    "etc": {"label": "기타", "color": "#6b7280"},
}

TASK_TYPE_LABEL = {
    "assignment": "과제",
    "exam": "시험",
    "performance": "수행평가",
}

IMPORTANCE_LABEL = {"high": "상", "medium": "중", "low": "하"}


def format_dday(d: date) -> str:
    today = date.today()
    delta = (d - today).days
    if delta < 0:
        return f"D+{abs(delta)}"
    elif delta == 0:
        return "D-Day"
    else:
        return f"D-{delta}"


def dday_class(d: date) -> str:
    today = date.today()
    delta = (d - today).days
    if delta <= 1:
        return "🔥 긴급"
    elif delta <= 3:
        return "⚠️ 임박"
    else:
        return "🕒 여유"


def parse_date_str(s: str) -> date:
    return datetime.strptime(s, "%Y-%m-%d").date()


# --------- 세션 상태 초기화 ---------
if "tasks" not in st.session_state:
    st.session_state.tasks = []  # 일정 리스트
if "studies" not in st.session_state:
    st.session_state.studies = []  # 스터디 플래너
if "task_id_seq" not in st.session_state:
    st.session_state.task_id_seq = 1
if "study_id_seq" not in st.session_state:
    st.session_state.study_id_seq = 1


# --------- 스터디 플래너: 미완료 자동 이월 ---------
today = date.today()
for s in st.session_state.studies:
    if (not s["completed"]) and s["planned_date"] < today:
        s["planned_date"] = today  # 오늘로 자동 이동


# --------- 반복 일정 처리 함수 ---------
def create_next_repeated_task(task: dict):
    repeat_type = task.get("repeat_type", "none")
    if repeat_type == "none":
        return
    due = task["due_date"]
    if repeat_type == "weekly":
        next_due = due + timedelta(days=7)
    elif repeat_type == "biweekly":
        next_due = due + timedelta(days=14)
    elif repeat_type == "monthly":
        next_due = due + timedelta(days=30)  # 단순 +30일
    else:
        return

    new_task = task.copy()
    new_task["id"] = st.session_state.task_id_seq
    st.session_state.task_id_seq += 1
    new_task["due_date"] = next_due
    new_task["completed"] = False
    st.session_state.tasks.append(new_task)


# ---------------- 상단 헤더 ----------------
st.markdown(
    """
    <h2 style="margin-bottom:0">HaToDo (하투두)</h2>
    <p style="color:#6b7280;margin-top:4px;">
    하나고 학생을 위한 학교 일정 집중 관리 · 주간 요약 · 스터디 플래너 · 협업 · 반복 일정 지원
    </p>
    """,
    unsafe_allow_html=True,
)

st.write("---")

# ---------------- 레이아웃: 좌/우 ----------------
col_main, col_side = st.columns([2.3, 1.7])

# ========== 왼쪽: 일정 + 스터디 플래너 ==========

with col_main:
    tab_tasks, tab_study = st.tabs(["📅 학교 일정 / 협업", "📖 스터디 플래너"])

    # ---------- 📅 일정 / 협업 탭 ----------
    with tab_tasks:
        st.subheader("학교 일정 등록 (과제 · 수행 · 시험)")

        with st.form("add_task_form", clear_on_submit=True):
            c1, c2, c3, c4 = st.columns([3, 2, 2, 2])
            title = c1.text_input("일정 내용", placeholder="예) 수학 수행평가 문제집 30쪽")
            subject = c2.selectbox(
                "과목",
                options=list(SUBJECT_INFO.keys()),
                format_func=lambda x: SUBJECT_INFO[x]["label"],
            )
            task_type = c3.selectbox(
                "유형",
                options=list(TASK_TYPE_LABEL.keys()),
                format_func=lambda x: TASK_TYPE_LABEL[x],
            )
            due_date = c4.date_input("마감일", value=today)

            c5, c6, c7 = st.columns([1, 2, 2])
            importance = c5.selectbox(
                "중요도", options=["high", "medium", "low"], format_func=lambda x: IMPORTANCE_LABEL[x]
            )
            repeat_type = c6.selectbox(
                "반복 일정",
                options=["none", "weekly", "biweekly", "monthly"],
                format_func=lambda x: {
                    "none": "반복 없음",
                    "weekly": "매주",
                    "biweekly": "격주",
                    "monthly": "매월",
                }[x],
            )
            team_name = c7.text_input("팀 이름(선택)", placeholder="예) 3조, 프로젝트 A")

            c8, c9 = st.columns(2)
            assignee = c8.text_input("담당자 이름(선택)", placeholder="예) 김우인")
            member_due_date = c9.date_input(
                "개인 마감일(선택)", value=due_date, help="팀 내 개인 데드라인이 다를 경우 사용"
            )

            submitted = st.form_submit_button("일정 추가")
            if submitted and title:
                st.session_state.tasks.append(
                    {
                        "id": st.session_state.task_id_seq,
                        "title": title,
                        "subject": subject,
                        "task_type": task_type,
                        "due_date": due_date,
                        "importance": importance,
                        "repeat_type": repeat_type,
                        "team_name": team_name.strip() or None,
                        "assignee": assignee.strip() or None,
                        "member_due_date": member_due_date,
                        "completed": False,
                    }
                )
                st.session_state.task_id_seq += 1
                st.success("일정을 추가했습니다.")

        st.markdown("### 📋 전체 일정 리스트")

        # 정렬: 마감일 → 중요도(상>중>하)
        importance_rank = {"high": 0, "medium": 1, "low": 2}
        tasks_sorted = sorted(
            st.session_state.tasks,
            key=lambda t: (t["due_date"], importance_rank.get(t["importance"], 1)),
        )

        if not tasks_sorted:
            st.info("등록된 일정이 없습니다.")
        else:
            for t in tasks_sorted:
                subj = SUBJECT_INFO[t["subject"]]
                dday = format_dday(t["due_date"])
                dclass = dday_class(t["due_date"])
                col_a, col_b = st.columns([4, 1])
                with col_a:
                    st.markdown(
                        f"""
                        <div style="padding:8px 10px; border-radius:10px; background:#ffffff; margin-bottom:4px; border-left:6px solid {subj['color']};">
                          <div style="font-size:0.8rem; color:#6b7280;">
                            <span style="font-weight:600;color:{subj['color']};">{subj['label']}</span>
                            · {TASK_TYPE_LABEL[t["task_type"]]}
                          </div>
                          <div style="font-size:0.98rem; font-weight:600; margin-top:2px;">
                            {t["title"]}
                          </div>
                          <div style="font-size:0.8rem; color:#6b7280; margin-top:4px;">
                            마감일: {t["due_date"].strftime("%Y-%m-%d")} · 
                            중요도: {IMPORTANCE_LABEL[t["importance"]]}
                            {" · 팀: " + t["team_name"] if t.get("team_name") else ""}
                            {" · 담당: " + t["assignee"] if t.get("assignee") else ""}
                            {" · 개인 마감: " + t["member_due_date"].strftime("%Y-%m-%d") if t.get("member_due_date") else ""}
                          </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with col_b:
                    if not t["completed"]:
                        if st.button(
                            f"완료\n{dday}\n{dclass}",
                            key=f"done_{t['id']}",
                            help="완료 처리 및 반복 일정 생성",
                        ):
                            t["completed"] = True
                            create_next_repeated_task(t)
                            st.experimental_rerun()
                    else:
                        st.markdown(
                            f"✅ 완료됨\n\n{dday}\n\n{dclass}",
                        )

    # ---------- 📖 스터디 플래너 탭 ----------
    with tab_study:
        st.subheader("스터디 플래너 (오늘 중심)")

        with st.form("study_form", clear_on_submit=True):
            c1, c2, c3 = st.columns([2, 3, 2])
            s_subject = c1.selectbox(
                "과목",
                options=list(SUBJECT_INFO.keys()),
                format_func=lambda x: SUBJECT_INFO[x]["label"],
            )
            s_content = c2.text_input("공부 내용", placeholder="예) 영어 단어 Day 15 암기")
            s_date = c3.date_input("계획 날짜", value=today)
            s_ok = st.form_submit_button("스터디 추가")
            if s_ok and s_content:
                st.session_state.studies.append(
                    {
                        "id": st.session_state.study_id_seq,
                        "subject": s_subject,
                        "content": s_content,
                        "planned_date": s_date,
                        "completed": False,
                    }
                )
                st.session_state.study_id_seq += 1
                st.success("스터디 항목을 추가했습니다.")

        st.markdown("### 📆 오늘 기준 스터디 목록")

        todays = [s for s in st.session_state.studies if s["planned_date"] == today]
        if not todays:
            st.info("오늘 날짜 기준 스터디가 없습니다.")
        else:
            for s in todays:
                subj = SUBJECT_INFO[s["subject"]]
                col_a, col_b = st.columns([4, 1])
                with col_a:
                    st.markdown(
                        f"""
                        <div style="padding:8px 10px; border-radius:10px; background:#ffffff; margin-bottom:4px; border-left:6px solid {subj['color']};">
                          <div style="font-size:0.8rem; color:#6b7280;">
                            <span style="font-weight:600;color:{subj['color']};">{subj['label']}</span>
                            · {s['planned_date'].strftime("%Y-%m-%d")} 계획
                          </div>
                          <div style="font-size:0.98rem; font-weight:600; margin-top:2px;">
                            {s["content"]}
                          </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with col_b:
                    if not s["completed"]:
                        if st.button("완료", key=f"study_done_{s['id']}"):
                            s["completed"] = True
                            st.experimental_rerun()
                    else:
                        st.write("✅ 완료됨")

        st.markdown("### 📊 과목별 학습량 분석")

        if st.session_state.studies:
            df = pd.DataFrame(st.session_state.studies)
            df["subject_label"] = df["subject"].map(lambda x: SUBJECT_INFO[x]["label"])
            df["count"] = 1
            grouped = df.groupby("subject_label")["count"].sum().reset_index()
            grouped = grouped.rename(columns={"count": "스터디 횟수"})
            st.bar_chart(
                grouped.set_index("subject_label")["스터디 횟수"]
            )
        else:
            st.info("아직 스터디 데이터가 없어 분석할 수 없습니다.")

# ========== 오른쪽: 주간 요약 + 캘린더 + 접근성 ==========

with col_side:
    tab_weekly, tab_calendar, tab_access = st.tabs(
        ["🟩 주간 일정 요약", "📆 간단 캘린더", "🟦 접근성(음성/볼륨)"]
    )

    # ---------- 🟩 주간 일정 요약 ----------
    with tab_weekly:
        st.subheader("이번 주 마감 일정")
        week_end = today + timedelta(days=7)
        weekly_tasks = [
            t
            for t in st.session_state.tasks
            if today <= t["due_date"] <= week_end
        ]
        weekly_tasks = sorted(
            weekly_tasks,
            key=lambda t: (t["due_date"], importance_rank.get(t["importance"], 1)),
        ) if weekly_tasks else []

        if not weekly_tasks:
            st.info("이번 주에 마감되는 일정이 없습니다.")
        else:
            for t in weekly_tasks:
                subj = SUBJECT_INFO[t["subject"]]
                dday = format_dday(t["due_date"])
                dclass = dday_class(t["due_date"])
                st.markdown(
                    f"""
                    <div style="padding:8px 10px; border-radius:10px; background:#ffffff; margin-bottom:6px; border-left:6px solid {subj['color']};">
                      <div style="font-size:0.8rem; color:#6b7280;">
                        <span style="font-weight:600;color:{subj['color']};">{subj['label']}</span>
                        · {TASK_TYPE_LABEL[t["task_type"]]}
                      </div>
                      <div style="font-size:0.95rem; font-weight:600; margin-top:2px;">
                        {t["title"]}
                      </div>
                      <div style="font-size:0.8rem; color:#6b7280; margin-top:4px;">
                        마감일: {t["due_date"].strftime("%Y-%m-%d")}
                        · <span style="font-weight:600;">{dday}</span>
                        · {dclass}
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # ---------- 📆 간단 캘린더 ----------
    with tab_calendar:
        st.subheader("간단 캘린더 뷰")

        if not st.session_state.tasks:
            st.info("일정이 없어 캘린더를 표시할 수 없습니다.")
        else:
            df = pd.DataFrame(st.session_state.tasks)
            df["subject_label"] = df["subject"].map(lambda x: SUBJECT_INFO[x]["label"])
            df["due_date_str"] = df["due_date"].map(lambda d: d.strftime("%Y-%m-%d"))
            grouped = (
                df.groupby("due_date_str")
                .agg(
                    count=("id", "count"),
                    subjects=("subject_label", lambda x: ", ".join(sorted(set(x)))),
                )
                .reset_index()
            )
            st.caption("날짜별 일정 개수 & 포함된 과목")
            st.dataframe(grouped, hide_index=True, use_container_width=True)

    # ---------- 🟦 접근성 (음성 / 볼륨) ----------
    with tab_access:
        st.subheader("접근성: 음성 안내 & 볼륨 조절")

        st.write(
            "정보 접근성이 떨어지는 이용자를 위해, 일정 안내를 음성으로 들을 수 있고 "
            "아래 슬라이더로 볼륨을 조절할 수 있다고 가정한 데모입니다."
        )

        st.audio(
            "https://www2.cs.uic.edu/~i101/SoundFiles/StarWars3.wav",
            format="audio/wav",
        )

        volume = st.slider("볼륨 (데모용)", 0, 100, 70)
        st.caption(f"현재 데모 볼륨: {volume}%  (실서비스에서는 음성합성 + 볼륨 API와 연동 가능)")

        st.info(
            "발표에서는 ‘시각 정보만으로 일정 확인이 힘든 학생도 HaToDo를 통해\n"
            "음성 안내와 볼륨 조절을 활용해 일정을 확인할 수 있다’는 점을 강조하면 좋아."
        )
