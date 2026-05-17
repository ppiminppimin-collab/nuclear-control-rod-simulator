import streamlit as st
import pandas as pd

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="AI 기반 원자로 자동 제어 시스템",
    page_icon="☢️",
    layout="wide"
)

# -----------------------------
# 상태 저장
# -----------------------------
if "rod" not in st.session_state:
    st.session_state.rod = 50

if "scram" not in st.session_state:
    st.session_state.scram = False

# -----------------------------
# 데이터 테이블
# -----------------------------
power_map = {
    0: 100,
    10: 96,
    20: 89,
    30: 78,
    40: 65,
    50: 50,
    60: 36,
    70: 23,
    80: 12,
    90: 4,
    100: 0
}

reactivity_map = {
    0: 1.00,
    10: 0.96,
    20: 0.89,
    30: 0.78,
    40: 0.65,
    50: 0.50,
    60: 0.36,
    70: 0.23,
    80: 0.12,
    90: 0.04,
    100: 0.00
}

temperature_map = {
    0: 560,
    10: 530,
    20: 500,
    30: 470,
    40: 440,
    50: 400,
    60: 360,
    70: 330,
    80: 300,
    90: 270,
    100: 250
}

# -----------------------------
# 제목
# -----------------------------
st.title("☢️ AI 기반 원자로 자동 제어 시스템")

st.write("""
본 프로그램은 제어봉 삽입률에 따른 원자로 출력 변화를
단순화하여 구현한 교육용 자동제어 시뮬레이터입니다.

사용자가 목표 출력값을 입력하면
AI 기반 자동제어 시스템이 제어봉 삽입률을 자동 조절합니다.
""")

st.markdown("---")

# -----------------------------
# 사이드바
# -----------------------------
st.sidebar.header("⚙️ 자동 제어 패널")

# 목표 출력
target_power = st.sidebar.slider(
    "목표 출력 (%)",
    0,
    100,
    70,
    step=5
)

# -----------------------------
# 자동 제어 시스템
# -----------------------------
if not st.session_state.scram:

    closest_rod = min(
        power_map,
        key=lambda x: abs(power_map[x] - target_power)
    )

    st.session_state.rod = closest_rod

# -----------------------------
# 현재 상태 계산
# -----------------------------
rod = st.session_state.rod

power = power_map[rod]

reactivity = reactivity_map[rod]

temperature = temperature_map[rod]

# -----------------------------
# SCRAM 버튼
# -----------------------------
if st.sidebar.button("☢️ SCRAM 긴급 정지"):

    st.session_state.scram = True
    st.session_state.rod = 100

# -----------------------------
# 재가동 버튼
# -----------------------------
if st.sidebar.button("🔄 원자로 재가동"):

    st.session_state.scram = False
    st.session_state.rod = 50

    st.success("원자로가 정상 운전 상태로 복구되었습니다.")

# -----------------------------
# SCRAM 상태 적용
# -----------------------------
if st.session_state.scram:

    rod = 100
    power = 0
    reactivity = 0.00
    temperature = 250

# -----------------------------
# 자동 제어 상태
# -----------------------------
st.subheader("🤖 AI 자동 제어 상태")

if st.session_state.scram:

    st.error("""
SCRAM 상태입니다.

안전 시스템에 의해
원자로가 긴급 정지되었습니다.
""")

else:

    st.success("AI 자동 제어 시스템 정상 작동 중")

    st.info(f"""
목표 출력:
{target_power}%

현재 시스템이 목표 출력에 가장 가까운 상태로
제어봉 삽입률을 자동 조절하고 있습니다.
""")

st.markdown("---")

# -----------------------------
# 상태 표시
# -----------------------------
st.subheader("📊 원자로 운전 상태")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "제어봉 삽입률",
        f"{rod}%"
    )

with col2:
    st.metric(
        "원자로 출력",
        f"{power}%"
    )

with col3:
    st.metric(
        "반응도",
        f"{reactivity}"
    )

with col4:
    st.metric(
        "냉각수 온도",
        f"{temperature} °C"
    )

st.markdown("---")

# -----------------------------
# 시스템 상태
# -----------------------------
st.subheader("🚨 시스템 상태")

if st.session_state.scram:

    st.error("☢️ 원자로 긴급 정지 상태")

else:

    if power >= 85:
        st.warning("⚠️ 과출력 상태")

    elif power >= 20:
        st.success("🟢 정상 운전 상태")

    else:
        st.error("🔴 출력이 매우 낮습니다")

# -----------------------------
# 출력 진행 바
# -----------------------------
st.subheader("⚡ 현재 출력 수준")

st.progress(power / 100)

st.write(f"현재 출력은 최대 출력의 {power}% 입니다.")

st.markdown("---")

# -----------------------------
# 그래프
# -----------------------------
st.subheader("📈 제어봉 삽입률에 따른 출력 변화")

graph_data = pd.DataFrame({
    "제어봉 삽입률": list(power_map.keys()),
    "원자로 출력": list(power_map.values()),
    "냉각수 온도": list(temperature_map.values())
})

st.line_chart(
    graph_data,
    x="제어봉 삽입률"
)

st.markdown("---")

# -----------------------------
# 제어 원리 설명
# -----------------------------
st.subheader("📚 시스템 설명")

st.write("""
### ☢️ 제어봉(Control Rod)

제어봉은 중성자를 흡수하여
핵분열 반응 속도를 조절하는 장치입니다.

- 제어봉 삽입 증가
→ 핵분열 감소
→ 출력 감소

- 제어봉 삽입 감소
→ 핵분열 증가
→ 출력 증가

---

### 🤖 AI 자동 제어 시스템

사용자가 목표 출력값을 입력하면
시스템이 목표 출력에 가장 가까운 상태가 되도록
제어봉 삽입률을 자동 조절합니다.

이는 전기전자공학의 피드백 제어 시스템 개념을 기반으로 합니다.

---

### ☢️ SCRAM 긴급 정지 시스템

SCRAM은 원자로 이상 상황 발생 시
제어봉을 즉시 삽입하여
핵분열 반응을 긴급 차단하는 안전 시스템입니다.

---

### 📊 데이터 기반 출력 모델

출력, 반응도, 냉각수 온도는
구간별 데이터를 직접 지정하여
비선형 특성을 반영하였습니다.
""")

st.markdown("---")

st.caption("AI 코딩(ChatGPT, Cursor)을 활용한 전기전자 응용 프로그램 개발")