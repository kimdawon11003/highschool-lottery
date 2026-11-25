import random
import pandas as pd
import streamlit as st

# 2. 리스트 선언: 고등학교 목록 및 우선순위 가중치 리스트 정의
ALL_HIGHSCHOOLS = [
    "고등학교1",
    "고등학교2",
    "고등학교3",
    "고등학교4",
    "고등학교5",
    "고등학교6",
    "고등학교7",
    "고등학교8",
    "고등학교9",
    "고등학교10",
]
WEIGHTS = [30, 25, 20, 15, 10]  # 1순위(30%) ~ 5순위(10%) 확률


# 중학교 내신별 가능한 고등학교를 if-elif-else로 구성
def get_available_schools(grade):
    if grade >= 200:
        return ALL_HIGHSCHOOLS[0:]
    elif grade >= 199.5:
        return ALL_HIGHSCHOOLS[1:]
    elif grade >= 198:
        return ALL_HIGHSCHOOLS[2:]
    elif grade >= 195:
        return ALL_HIGHSCHOOLS[3:]
    elif grade >= 190:
        return ALL_HIGHSCHOOLS[4:]
    elif grade >= 180:
        return ALL_HIGHSCHOOLS[5:]
    elif grade >= 170:
        return ALL_HIGHSCHOOLS[6:]
    elif grade >= 160:
        return ALL_HIGHSCHOOLS[7:]
    elif grade >= 140:
        return ALL_HIGHSCHOOLS[8:]
    elif grade >= 100:
        return ALL_HIGHSCHOOLS[9:]
    else:
        return []


# 성적과 원하는 고등학교 1~5순위를 입력받아 뽑을 고등학교 5개 선정
def check_rist(grade, wanted_hughschool):
    available = get_available_schools(grade)
    selected_5 = []
    for school in wanted_hughschool:
        if school in available and len(selected_5) < 5:
            selected_5.append(school)
    return selected_5


# 버튼 클릭 시 실행되는 추첨 및 테이블 출력 함수
def pick_highschool(grade, available_schools, wanted_highschool):
    # 유효성 검사: 5개 순위가 중복 없이 모두 선택되었는지 확인
    if len(set(wanted_highschool)) < 5:
        st.error(
            "⚠️ 1순위부터 5순위까지 중복되지 않게 서로 다른 고등학교 5개를 선택해주세요."
        )
        return

    # check_rist 함수를 통해 최종 후보 5개 학교 확정
    candidates = check_rist(grade, wanted_highschool)

    # 확률에 따라 최종 고등학교 1개 추첨
    picked_school = random.choices(candidates, weights=WEIGHTS, k=1)[0]

    # 6. 반복 출력: for 구문을 이용해 고등학교 선택목록 리스트를 표(DataFrame) 형태 데이터로 변환
    table_data = []
    max_rows = max(len(available_schools), 5)

    for i in range(max_rows):
        row_grade = f"{grade:.2f}" if i == 0 else ""
        row_avail = available_schools[i] if i < len(available_schools) else ""
        row_priority = (
            f"{i+1}순위={candidates[i]}" if i < len(candidates) else ""
        )
        row_picked = picked_school if i == 0 else ""

        table_data.append({
            "중학교 내신": row_grade,
            "가능한 학교": row_avail,
            "우선순위(1~5)": row_priority,
            "추첨된 고등학교": row_picked,
        })

    df = pd.DataFrame(table_data)

    st.subheader("📊 고등학교 배정 추첨 결과")
    st.table(df)


# --- 1. 시작: 사용자가 앱에 접속 (UI 구성) ---
st.title("🏫 고등학교 진학 확률 추첨 시스템")

# 3. 입력받기: 0에서 200 사이의 소수점 성적 입력
grade = st.number_input(
    "중학교 내신 성적을 입력하세요 (0 ~ 200점, 소수점 입력 가능):",
    min_value=0.0,
    max_value=200.0,
    value=192.42,
    step=0.01,
    format="%.2f",
)

# 5. 조건 판단: 성적이 100 미만일 경우 예외 메시지 출력
if grade < 100:
    st.warning("가능한 학교가 없습니다, 다른 지역에서 찾아가세요")
else:
    available_schools = get_available_schools(grade)
    st.info(
        f"현재 성적({grade:.2f}점)으로 지원 가능한 고등학교:"
        f" **{', '.join(available_schools)}**"
    )

    # 가능한 학교가 5개 미만일 경우 안내
    if len(available_schools) < 5:
        st.error(
            f"지원 가능한 학교가 {len(available_schools)}개뿐이므로 1~5순위를"
            " 모두 채울 수 없습니다. (최소 160점 이상 필요)"
        )
    else:
        st.subheader("🎯 희망 고등학교 우선순위 입력 (1~5순위)")
        wanted_highschool = []
        cols = st.columns(5)

        for i in range(5):
            with cols[i]:
                choice = st.selectbox(
                    f"{i+1}순위 ({WEIGHTS[i]}%)",
                    options=available_schools,
                    index=min(i, len(available_schools) - 1),
                    key=f"rank_{i}",
                )
                wanted_highschool.append(choice)

        # 4. 버튼 클릭 시 'pick_highschool()' 함수 실행
        if st.button("🎲 최종 고등학교 추첨하기", use_container_width=True):
            pick_highschool(grade, available_schools, wanted_highschool)
