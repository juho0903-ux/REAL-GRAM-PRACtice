import re
from collections import Counter
import streamlit as st

st.set_page_config(
    page_title="퇴계원중 1학년 중간고사 대비 문항 연습",
    page_icon="✏️",
    layout="centered",
)

SENTENCE_1 = "먹구름이 가득 낀 하늘은 늘 철수를 공포에 사로잡히게 하였다."
SENTENCE_2 = "착한 형은 지우개로 낡은 공책의 글씨를 깨끗이 지웠다."
SENTENCE_3 = "어린 동생이 풋사과를 작은 접시에 가지런히 담았다."

# -----------------------------
# 문항 1~3 정답
# -----------------------------
Q1_ANSWERS = {
    "먹구름": {"morphemes": ["먹-", "구름"], "pos": "명사"},
    "사로잡히게": {"morphemes": ["사로잡-", "-히-", "-게"], "pos": "동사"},
}

Q2_ANSWERS = {
    "먹구름": "명사", "이": "조사", "가득": "부사", "낀": "동사",
    "하늘": "명사", "은": "조사", "늘": "부사", "철수": "명사",
    "를": "조사", "공포": "명사", "에": "조사", "사로잡히게": "동사", "하였다": "동사",
}

Q3_ANSWERS = {
    "자립 형태소": ["구름", "가득", "하늘", "늘", "철수", "공포"],
    "의존 형태소": [
        "먹-", "이", "끼-", "-ㄴ", "은", "를", "에",
        "사로잡-", "-히-", "-게", "하-", "-였-", "-다"
    ],
    "실질 형태소": [
        "구름", "가득", "끼-", "하늘", "늘", "철수", "공포",
        "사로잡-", "하-"
    ],
    "형식 형태소": [
        "먹-", "이", "-ㄴ", "은", "를", "에",
        "-히-", "-게", "-였-", "-다"
    ],
}

# -----------------------------
# 문항 4~6 정답
# -----------------------------
Q4_ANSWERS = ["지우개", "깨끗이"]

Q5_ANSWERS = {
    "지우개": ["지우-", "-개"],
    "깨끗이": ["깨끗", "-이"],
}

Q6_ANSWERS = {
    "지우개": "명사",
    "깨끗이": "부사",
}


Q7_ANSWERS = {
    "착한": ["착하-", "-ㄴ"],
    "형": ["형"],
    "은": ["은"],
    "지우개": ["지우-", "-개"],
    "로": ["로"],
    "낡은": ["낡-", "-은"],
    "공책": ["공책"],
    "의": ["의"],
    "글씨": ["글씨"],
    "를": ["를"],
    "깨끗이": ["깨끗", "-이"],
    "지웠다": ["지우-", "-었-", "-다"],
}

Q8_ANSWERS = {
    "착한": "형용사",
    "형": "명사",
    "은": "조사",
    "지우개": "명사",
    "로": "조사",
    "낡은": "형용사",
    "공책": "명사",
    "의": "조사",
    "글씨": "명사",
    "를": "조사",
    "깨끗이": "부사",
    "지웠다": "동사",
}


Q9_TYPE_ANSWERS = {
    "자립 형태소": ["형", "공책", "글씨"],
    "의존 형태소": [
        "착하-", "-ㄴ", "은", "지우-", "-개", "로", "낡-", "-은",
        "의", "를", "깨끗", "-이", "지우-", "-었-", "-다"
    ],
    "실질 형태소": ["착하-", "형", "지우-", "낡-", "공책", "글씨", "깨끗", "지우-"],
    "형식 형태소": ["-ㄴ", "은", "-개", "로", "-은", "의", "를", "-이", "-었-", "-다"],
}

Q14_TYPE_ANSWERS = {
    "자립 형태소": ["동생", "사과", "접시"],
    "의존 형태소": [
        "어리-", "-ㄴ", "이", "풋-", "를", "작-", "-은", "에",
        "가지런", "-히", "담-", "-았-", "-다"
    ],
    "실질 형태소": ["어리-", "동생", "사과", "작-", "접시", "가지런", "담-"],
    "형식 형태소": ["-ㄴ", "이", "풋-", "를", "-은", "에", "-히", "-았-", "-다"],
}

Q9_ANSWERS = ["풋사과", "가지런히"]

Q10_ANSWERS = {
    "풋사과": ["풋-", "사과"],
    "가지런히": ["가지런", "-히"],
}

Q11_ANSWERS = {
    "풋사과": "명사",
    "가지런히": "부사",
}

Q12_ANSWERS = {
    "어린": ["어리-", "-ㄴ"],
    "동생이": ["동생", "이"],
    "풋사과를": ["풋-", "사과", "를"],
    "작은": ["작-", "-은"],
    "접시에": ["접시", "에"],
    "가지런히": ["가지런", "-히"],
    "담았다": ["담-", "-았-", "-다"],
}

Q13_ANSWERS = {
    "어린": "형용사",
    "동생": "명사",
    "이": "조사",
    "풋사과": "명사",
    "를": "조사",
    "작은": "형용사",
    "접시": "명사",
    "에": "조사",
    "가지런히": "부사",
    "담았다": "동사",
}

def normalize_sequence(text: str):
    if not text:
        return []
    cleaned = re.sub(r"[,/·|]+", " ", text)
    return [x.strip() for x in cleaned.split() if x.strip()]

def normalize_set(text: str):
    if not text:
        return []
    parts = re.split(r"[,/·|\n]+", text)
    return [x.strip() for x in parts if x.strip()]

def exact_multiset_match(text: str, answer_list):
    return Counter(normalize_set(text)) == Counter(answer_list)

def reset_all():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

st.markdown("""
<style>
:root {
    --bg: #ffffff;
    --surface: #ffffff;
    --surface-2: #f7f8fa;
    --surface-3: #eef4f3;
    --text: #111827;
    --text-soft: #4b5563;
    --border: #d7dde5;
    --mint: #dff3ee;
    --mint-strong: #70b8a5;
    --coral: #ff9e8f;
    --coral-strong: #ef806e;
    --success-bg: #edf9f1;
    --warning-bg: #fff8e8;
    --error-bg: #fff0f0;
    --info-bg: #eef5ff;
    --shadow: 0 6px 18px rgba(17, 24, 39, 0.06);
}

html, body, .stApp, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
}

html, body, .stApp, button, input, textarea, select, p, span, div, label {
    font-family: "Maplestory", "Maplestory OTF", "Apple SD Gothic Neo",
                 "Noto Sans KR", "Malgun Gothic", system-ui, sans-serif !important;
}

.block-container {
    max-width: 1080px;
    padding-top: 1.6rem;
    padding-bottom: 3rem;
    padding-left: 1rem;
    padding-right: 1rem;
}

h1, h2, h3, h4, p, label, .stCaption {
    color: var(--text) !important;
}

.stCaption, small {
    color: var(--text-soft) !important;
}

h1 {
    font-weight: 800;
    letter-spacing: -0.03em;
}

h2, h3 {
    font-weight: 750;
    letter-spacing: -0.02em;
}

.sentence-box {
    background: var(--surface-3);
    color: var(--text);
    border: 1px solid #cfe1dc;
    border-radius: 20px;
    padding: 18px 20px;
    font-size: 1.08rem;
    line-height: 1.7;
    margin: 10px 0 20px 0;
    box-shadow: var(--shadow);
}

.condition-box {
    background: var(--surface-2);
    color: var(--text);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 15px 18px;
    margin: 10px 0 18px 0;
    line-height: 1.85;
    box-shadow: var(--shadow);
}

/* Tabs */
div[data-baseweb="tab-list"] {
    gap: 0.4rem;
    background: var(--surface-2) !important;
    border: 1px solid var(--border);
    padding: 0.4rem;
    border-radius: 18px;
    overflow-x: auto;
    scrollbar-width: none;
}

div[data-baseweb="tab-list"]::-webkit-scrollbar {
    display: none;
}

button[data-baseweb="tab"] {
    white-space: nowrap;
    border-radius: 14px !important;
    color: var(--text-soft) !important;
    background: transparent !important;
    border: 1px solid transparent !important;
    font-weight: 700 !important;
    padding: 0.62rem 0.9rem !important;
}

button[data-baseweb="tab"]:hover {
    background: #ffffff !important;
    color: var(--text) !important;
    border-color: var(--border) !important;
}

button[aria-selected="true"][data-baseweb="tab"] {
    background: var(--mint) !important;
    color: var(--text) !important;
    border-color: #b9ded4 !important;
}

/* Text inputs / text areas */
div[data-baseweb="input"] > div,
div[data-testid="stTextAreaRootElement"] textarea {
    background: #ffffff !important;
    color: #111827 !important;
    border: 1.5px solid #cfd6df !important;
    border-radius: 16px !important;
    box-shadow: none !important;
}

div[data-baseweb="input"] input,
div[data-testid="stTextAreaRootElement"] textarea {
    color: #111827 !important;
    caret-color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
}

div[data-baseweb="input"] input::placeholder,
div[data-testid="stTextAreaRootElement"] textarea::placeholder {
    color: #8a94a3 !important;
    opacity: 1 !important;
}

div[data-baseweb="input"] > div:focus-within,
div[data-testid="stTextAreaRootElement"] textarea:focus {
    border-color: var(--mint-strong) !important;
    box-shadow: 0 0 0 3px rgba(112, 184, 165, 0.18) !important;
}

label[data-testid="stWidgetLabel"] p {
    color: var(--text) !important;
    font-weight: 700 !important;
}

/* Buttons */
div.stButton > button {
    border-radius: 16px !important;
    min-height: 46px;
    padding: 0.62rem 1.1rem;
    font-weight: 800 !important;
    border: 1px solid transparent !important;
    box-shadow: 0 4px 12px rgba(17, 24, 39, 0.08) !important;
}

div.stButton > button[kind="primary"] {
    background: var(--coral) !important;
    color: #ffffff !important;
}

div.stButton > button[kind="primary"]:hover {
    background: var(--coral-strong) !important;
    color: #ffffff !important;
}

div.stButton > button[kind="secondary"] {
    background: #ffffff !important;
    color: var(--text) !important;
    border-color: var(--border) !important;
}

div.stButton > button[kind="secondary"]:hover {
    background: var(--surface-2) !important;
}

/* Alerts: force readable text in both light/dark themes */
div[data-testid="stAlert"] {
    border-radius: 18px !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    box-shadow: var(--shadow);
}

div[data-testid="stAlert"] * {
    color: var(--text) !important;
}

div[data-testid="stNotification"] {
    color: var(--text) !important;
}

/* Expanders */
div[data-testid="stExpander"] {
    background: #ffffff !important;
    border: 1px solid var(--border) !important;
    border-radius: 18px !important;
    box-shadow: var(--shadow);
    overflow: hidden;
}

div[data-testid="stExpander"] summary,
div[data-testid="stExpander"] summary * {
    color: var(--text) !important;
    font-weight: 700 !important;
}

/* Divider */
hr {
    border-color: var(--border) !important;
    margin: 2rem 0 1.25rem 0;
}

/* Mobile */
@media (max-width: 768px) {
    .block-container {
        padding-top: 1rem;
        padding-left: 0.75rem;
        padding-right: 0.75rem;
        padding-bottom: 2.25rem;
    }

    h1 {
        font-size: 1.72rem !important;
        line-height: 1.28 !important;
    }

    h2, h3 {
        font-size: 1.28rem !important;
        line-height: 1.35 !important;
    }

    .sentence-box,
    .condition-box {
        padding: 15px 15px;
        border-radius: 16px;
    }

    div.stButton > button {
        width: 100% !important;
    }

    button[data-baseweb="tab"] {
        font-size: 0.94rem !important;
        padding: 0.56rem 0.78rem !important;
    }

    div[data-testid="column"] {
        min-width: 0 !important;
    }
}

/* Force readable UI even when Streamlit/browser theme is dark */
@media (prefers-color-scheme: dark) {
    html, body, .stApp, [data-testid="stAppViewContainer"] {
        background: #ffffff !important;
        color: #111827 !important;
    }

    [data-testid="stHeader"] {
        background: rgba(255,255,255,0.96) !important;
    }

    [data-testid="stToolbar"] {
        color: #111827 !important;
    }
}
</style>
""", unsafe_allow_html=True)

st.title("퇴계원중 1학년 중간고사 대비 문항 연습")
st.caption("중간고사에 필요한 국어 문법 개념을 문항별로 연습합니다.")

tabs = st.tabs([
    "1️⃣ 문항 1", "2️⃣ 문항 2", "3️⃣ 문항 3", "4️⃣ 문항 4",
    "5️⃣ 문항 5", "6️⃣ 문항 6", "7️⃣ 문항 7", "8️⃣ 문항 8",
    "9️⃣ 문항 9", "10 문항 10", "11 문항 11", "12 문항 12",
    "13 문항 13", "14 문항 14", "15 문항 15"
])
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12, tab13, tab14, tab15 = tabs

# 문항 1
with tab1:
    st.markdown(f'<div class="sentence-box"><b>문장</b><br>{SENTENCE_1}</div>', unsafe_allow_html=True)
    st.subheader("1. 파생어를 찾아 분석해 보세요.")
    st.markdown("""
    <div class="condition-box">
    ✅ 문장에서 파생어를 모두 찾기<br>
    ✅ 각 파생어를 형태소 단위로 분석하기<br>
    ✅ 형태소 분석 시 접사·어간·어미의 <b>붙임표를 정확하게 표시하기</b><br>
    ✅ 각 파생어의 품사 쓰기
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        w1 = st.text_input("파생어 1", key="q1_w1")
        m1 = st.text_input("형태소 분석 1", key="q1_m1")
        p1 = st.text_input("품사 1", placeholder="예: 명사", key="q1_p1")
    with c2:
        w2 = st.text_input("파생어 2", key="q1_w2")
        m2 = st.text_input("형태소 분석 2", key="q1_m2")
        p2 = st.text_input("품사 2", placeholder="예: 동사", key="q1_p2")

    if st.button("1번 제출", type="primary", key="submit1"):
        entries = [(w1.strip(), m1, p1.strip()), (w2.strip(), m2, p2.strip())]
        seen = set()
        correct = 0
        for idx, (word, morph, pos) in enumerate(entries, 1):
            if word not in Q1_ANSWERS or word in seen:
                st.error(f"{idx}번째 답: 파생어를 다시 확인해 보세요.")
                continue
            seen.add(word)
            ans = Q1_ANSWERS[word]
            ok_m = normalize_sequence(morph) == ans["morphemes"]
            ok_p = pos == ans["pos"]
            if ok_m and ok_p:
                st.success(f"{idx}번째 답: 정확합니다.")
                correct += 1
            else:
                if not ok_m:
                    st.warning(f"{idx}번째 답: 형태소 분석의 순서와 붙임표를 다시 확인해 보세요.")
                if not ok_p:
                    st.warning(f"{idx}번째 답: 품사를 다시 확인해 보세요.")
        if correct == 2:
            st.success("두 파생어를 모두 정확하게 분석했습니다!")

# 문항 2
with tab2:
    st.markdown(f'<div class="sentence-box"><b>문장</b><br>{SENTENCE_1}</div>', unsafe_allow_html=True)
    st.subheader("2. 문장에 쓰인 모든 단어의 품사를 써 보세요.")
    st.info("각 칸에 품사 이름을 직접 입력하세요.")

    q2_user = {}
    words = list(Q2_ANSWERS.keys())
    c1, c2 = st.columns(2)
    for i, word in enumerate(words):
        with (c1 if i % 2 == 0 else c2):
            q2_user[word] = st.text_input(word, placeholder="품사 입력", key=f"q2_{i}").strip()

    if st.button("2번 제출", type="primary", key="submit2"):
        blank, wrong = [], []
        for word, ans in Q2_ANSWERS.items():
            val = q2_user[word]
            if not val:
                blank.append(word)
            elif val != ans:
                wrong.append(word)

        if not blank and not wrong:
            st.success("모든 단어의 품사를 정확하게 썼습니다!")
        else:
            if blank:
                st.warning("아직 쓰지 않은 단어: " + ", ".join(blank))
            if wrong:
                st.warning("다시 확인할 단어: " + ", ".join(wrong))
            if "사로잡히게" in wrong:
                with st.expander("💡 '사로잡히게' 힌트 보기"):
                    st.write("1. 이 말에는 기본형이 있는가?")
                    st.write("2. 기본형이 있어 활용한 것이라면, 움직임이나 작용을 나타내는가, 성질이나 상태를 나타내는가?")
            st.info("정답은 바로 보여주지 않습니다. 해당 단어만 고쳐서 다시 제출해 보세요.")

# 문항 3
with tab3:
    st.markdown(f'<div class="sentence-box"><b>문장</b><br>{SENTENCE_1}</div>', unsafe_allow_html=True)
    st.subheader("3. 형태소를 종류별로 분류해 보세요.")
    st.markdown("""
    <div class="condition-box">
    ✅ 아래 네 칸에 해당 형태소를 직접 쓰세요.<br>
    ✅ 형태소 사이는 <b>쉼표(,)</b>로 구분하세요.<br>
    ✅ 접사·어간·어미의 <b>붙임표 위치까지 정확하게</b> 써야 정답으로 인정합니다.<br>
    ✅ 형태소의 순서는 달라도 됩니다.
    </div>
    """, unsafe_allow_html=True)

    a = st.text_area("자립 형태소", key="q3_a")
    b = st.text_area("의존 형태소", key="q3_b")
    c = st.text_area("실질 형태소", key="q3_c")
    d = st.text_area("형식 형태소", key="q3_d")

    if st.button("3번 제출", type="primary", key="submit3"):
        user_map = {"자립 형태소": a, "의존 형태소": b, "실질 형태소": c, "형식 형태소": d}
        all_ok = True
        for cat, txt in user_map.items():
            if exact_multiset_match(txt, Q3_ANSWERS[cat]):
                st.success(f"{cat}: 정확합니다.")
            else:
                all_ok = False
                st.warning(f"{cat}: 누락·중복 또는 붙임표 위치를 다시 확인해 보세요.")
        if all_ok:
            st.success("네 종류의 형태소를 모두 정확하게 분류했습니다!")

# 문항 4
with tab4:
    st.markdown(f'<div class="sentence-box"><b>문장</b><br>{SENTENCE_2}</div>', unsafe_allow_html=True)
    st.subheader("4. 윗문장에서 파생어를 모두 찾아 쓰세요.")

    q4_1 = st.text_input("파생어 1", key="q4_1")
    q4_2 = st.text_input("파생어 2", key="q4_2")

    if st.button("4번 제출", type="primary", key="submit4"):
        answers = [q4_1.strip(), q4_2.strip()]
        if Counter(answers) == Counter(Q4_ANSWERS):
            st.success("파생어를 모두 정확하게 찾았습니다!")
        else:
            st.warning("파생어를 다시 확인해 보세요.")
            with st.expander("힌트 보기"):
                st.write("어근에 접사가 붙어 새 단어가 된 경우를 찾아보세요.")

# 문항 5
with tab5:
    st.markdown(f'<div class="sentence-box"><b>문장</b><br>{SENTENCE_2}</div>', unsafe_allow_html=True)
    st.subheader("5. 문항 4에서 찾은 파생어를 형태소 단위로 분석하세요.")

    st.markdown("""
    <div class="condition-box">
    ✅ 형태소 분석 시 붙임표를 정확하게 표시하세요.
    </div>
    """, unsafe_allow_html=True)

    q5_1 = st.text_input("지우개", key="q5_1")
    q5_2 = st.text_input("깨끗이", key="q5_2")

    if st.button("5번 제출", type="primary", key="submit5"):
        wrong = []
        if normalize_sequence(q5_1) != Q5_ANSWERS["지우개"]:
            wrong.append("지우개")
        if normalize_sequence(q5_2) != Q5_ANSWERS["깨끗이"]:
            wrong.append("깨끗이")
        if not wrong:
            st.success("두 파생어의 형태소 분석이 모두 정확합니다!")
        else:
            st.warning("다시 확인할 단어: " + ", ".join(wrong))
            st.info("형태소의 순서와 붙임표 위치까지 확인해 보세요.")

# 문항 6
with tab6:
    st.markdown(f'<div class="sentence-box"><b>문장</b><br>{SENTENCE_2}</div>', unsafe_allow_html=True)
    st.subheader("6. 문항 4에서 찾은 각 파생어의 품사를 쓰세요.")

    q6_1 = st.text_input("지우개", placeholder="품사 입력", key="q6_1")
    q6_2 = st.text_input("깨끗이", placeholder="품사 입력", key="q6_2")

    if st.button("6번 제출", type="primary", key="submit6"):
        wrong = []
        if q6_1.strip() != Q6_ANSWERS["지우개"]:
            wrong.append("지우개")
        if q6_2.strip() != Q6_ANSWERS["깨끗이"]:
            wrong.append("깨끗이")
        if not wrong:
            st.success("두 파생어의 품사를 모두 정확하게 썼습니다!")
        else:
            st.warning("다시 확인할 단어: " + ", ".join(wrong))

# 문항 7
with tab7:
    st.markdown(f'<div class="sentence-box"><b>문장</b><br>{SENTENCE_2}</div>', unsafe_allow_html=True)
    st.subheader("7. 문장에 쓰인 모든 단어를 형태소 단위로 분석하세요.")

    st.markdown("""
    <div class="condition-box">
    ✅ 각 단어를 형태소 단위로 분석하세요.<br>
    ✅ 형태소 사이는 <b>쉼표(,)</b> 또는 <b>슬래시(/)</b>로 구분해도 됩니다.<br>
    ✅ 접사·어간·어미의 <b>붙임표 위치까지 정확하게</b> 써야 정답으로 인정합니다.<br>
    ✅ ‘지웠다’는 줄어든 형태이므로 기본 형태를 밝혀 분석하세요.
    </div>
    """, unsafe_allow_html=True)

    q7_user = {}
    words7 = list(Q7_ANSWERS.keys())
    c1, c2 = st.columns(2)

    for i, word in enumerate(words7):
        with (c1 if i % 2 == 0 else c2):
            q7_user[word] = st.text_input(
                word,
                placeholder="형태소 분석",
                key=f"q7_{i}"
            )

    if st.button("7번 제출", type="primary", key="submit7"):
        blank = []
        wrong = []

        for word, answer in Q7_ANSWERS.items():
            user_answer = q7_user[word]
            if not user_answer.strip():
                blank.append(word)
            elif normalize_sequence(user_answer) != answer:
                wrong.append(word)

        if not blank and not wrong:
            st.success("모든 단어의 형태소 분석이 정확합니다!")
        else:
            if blank:
                st.warning("아직 분석하지 않은 단어: " + ", ".join(blank))
            if wrong:
                st.warning("다시 확인할 단어: " + ", ".join(wrong))

            if "지웠다" in wrong:
                with st.expander("💡 '지웠다' 힌트 보기"):
                    st.write("‘지웠다’는 줄어든 형태입니다.")
                    st.write("기본형 ‘지우다’를 떠올리고, 어간과 과거 시제 선어말 어미, 종결 어미로 나누어 보세요.")

            st.info("정답은 바로 보여주지 않습니다. 틀린 단어만 고쳐서 다시 제출해 보세요.")


# 문항 8
with tab8:
    st.markdown(f'<div class="sentence-box"><b>문장</b><br>{SENTENCE_2}</div>', unsafe_allow_html=True)
    st.subheader("8. 문장에 쓰인 모든 단어의 품사를 쓰세요.")
    st.info("각 칸에 품사 이름을 직접 입력하세요.")

    q8_user = {}
    words8 = list(Q8_ANSWERS.keys())
    c1, c2 = st.columns(2)

    for i, word in enumerate(words8):
        with (c1 if i % 2 == 0 else c2):
            q8_user[word] = st.text_input(
                word,
                placeholder="품사 입력",
                key=f"q8_{i}"
            ).strip()

    if st.button("8번 제출", type="primary", key="submit8"):
        blank = []
        wrong = []

        for word, answer in Q8_ANSWERS.items():
            user_answer = q8_user[word]
            if not user_answer:
                blank.append(word)
            elif user_answer != answer:
                wrong.append(word)

        if not blank and not wrong:
            st.success("모든 단어의 품사를 정확하게 썼습니다!")
        else:
            if blank:
                st.warning("아직 쓰지 않은 단어: " + ", ".join(blank))
            if wrong:
                st.warning("다시 확인할 단어: " + ", ".join(wrong))
            st.info("정답은 바로 보여주지 않습니다. 해당 단어만 고쳐서 다시 제출해 보세요.")


# 문항 9
with tab9:
    st.markdown(f'<div class="sentence-box"><b>문장</b><br>{SENTENCE_2}</div>', unsafe_allow_html=True)
    st.subheader("9. 문장의 형태소를 종류별로 분류해 보세요.")

    st.markdown("""
    <div class="condition-box">
    ✅ 아래 네 칸에 해당 형태소를 직접 쓰세요.<br>
    ✅ 형태소 사이는 <b>쉼표(,)</b>로 구분하세요.<br>
    ✅ 접사·어간·어미의 <b>붙임표 위치까지 정확하게</b> 써야 정답으로 인정합니다.<br>
    ✅ 형태소의 순서는 달라도 됩니다.
    </div>
    """, unsafe_allow_html=True)

    q9_self = st.text_area("자립 형태소", key="q9_self")
    q9_dependent = st.text_area("의존 형태소", key="q9_dependent")
    q9_lexical = st.text_area("실질 형태소", key="q9_lexical")
    q9_grammatical = st.text_area("형식 형태소", key="q9_grammatical")

    if st.button("9번 제출", type="primary", key="submit9_types"):
        user_map = {
            "자립 형태소": q9_self,
            "의존 형태소": q9_dependent,
            "실질 형태소": q9_lexical,
            "형식 형태소": q9_grammatical,
        }

        all_ok = True
        for category, user_text in user_map.items():
            if exact_multiset_match(user_text, Q9_TYPE_ANSWERS[category]):
                st.success(f"{category}: 정확합니다.")
            else:
                all_ok = False
                st.warning(f"{category}: 누락·중복 또는 붙임표 위치를 다시 확인해 보세요.")

        if all_ok:
            st.success("네 종류의 형태소를 모두 정확하게 분류했습니다!")


# 문항 10
with tab10:
    st.markdown(f'<div class="sentence-box"><b>문장</b><br>{SENTENCE_3}</div>', unsafe_allow_html=True)
    st.subheader("10. 윗문장에서 파생어를 모두 찾아 쓰세요.")

    q10_find_1 = st.text_input("파생어 1", key="q10_find_1")
    q10_find_2 = st.text_input("파생어 2", key="q10_find_2")

    if st.button("10번 제출", type="primary", key="submit10_find"):
        answers = [q10_find_1.strip(), q10_find_2.strip()]
        if Counter(answers) == Counter(Q9_ANSWERS):
            st.success("파생어를 모두 정확하게 찾았습니다!")
        else:
            st.warning("파생어를 다시 확인해 보세요.")
            with st.expander("힌트 보기"):
                st.write("어근에 접사가 붙어 새 단어가 된 경우를 찾아보세요.")


# 문항 11
with tab11:
    st.markdown(f'<div class="sentence-box"><b>문장</b><br>{SENTENCE_3}</div>', unsafe_allow_html=True)
    st.subheader("11. 파생어를 형태소 단위로 분석하세요.")

    st.markdown("""
    <div class="condition-box">
    ✅ 형태소 분석 시 붙임표를 정확하게 표시하세요.
    </div>
    """, unsafe_allow_html=True)

    q11_m1 = st.text_input("풋사과", key="q11_m1")
    q11_m2 = st.text_input("가지런히", key="q11_m2")

    if st.button("11번 제출", type="primary", key="submit11_morph"):
        wrong = []
        if normalize_sequence(q11_m1) != Q10_ANSWERS["풋사과"]:
            wrong.append("풋사과")
        if normalize_sequence(q11_m2) != Q10_ANSWERS["가지런히"]:
            wrong.append("가지런히")

        if not wrong:
            st.success("두 파생어의 형태소 분석이 모두 정확합니다!")
        else:
            st.warning("다시 확인할 단어: " + ", ".join(wrong))
            st.info("형태소의 순서와 붙임표 위치까지 확인해 보세요.")


# 문항 12
with tab12:
    st.markdown(f'<div class="sentence-box"><b>문장</b><br>{SENTENCE_3}</div>', unsafe_allow_html=True)
    st.subheader("12. 각 파생어의 품사를 쓰세요.")

    q12_p1 = st.text_input("풋사과", placeholder="품사 입력", key="q12_p1")
    q12_p2 = st.text_input("가지런히", placeholder="품사 입력", key="q12_p2")

    if st.button("12번 제출", type="primary", key="submit12_pos"):
        wrong = []
        if q12_p1.strip() != Q11_ANSWERS["풋사과"]:
            wrong.append("풋사과")
        if q12_p2.strip() != Q11_ANSWERS["가지런히"]:
            wrong.append("가지런히")

        if not wrong:
            st.success("두 파생어의 품사를 모두 정확하게 썼습니다!")
        else:
            st.warning("다시 확인할 단어: " + ", ".join(wrong))


# 문항 13
with tab13:
    st.markdown(f'<div class="sentence-box"><b>문장</b><br>{SENTENCE_3}</div>', unsafe_allow_html=True)
    st.subheader("13. 문장에 쓰인 모든 단어를 형태소 단위로 분석하세요.")

    st.markdown("""
    <div class="condition-box">
    ✅ 각 단어를 형태소 단위로 분석하세요.<br>
    ✅ 형태소 사이는 <b>쉼표(,)</b> 또는 <b>슬래시(/)</b>로 구분해도 됩니다.<br>
    ✅ 접사·어간·어미의 <b>붙임표 위치까지 정확하게</b> 써야 정답으로 인정합니다.
    </div>
    """, unsafe_allow_html=True)

    q13_user = {}
    words13 = list(Q12_ANSWERS.keys())
    c1, c2 = st.columns(2)

    for i, word in enumerate(words13):
        with (c1 if i % 2 == 0 else c2):
            q13_user[word] = st.text_input(
                word,
                placeholder="형태소 분석",
                key=f"q13_morph_{i}"
            )

    if st.button("13번 제출", type="primary", key="submit13_morph"):
        blank = []
        wrong = []

        for word, answer in Q12_ANSWERS.items():
            user_answer = q13_user[word]
            if not user_answer.strip():
                blank.append(word)
            elif normalize_sequence(user_answer) != answer:
                wrong.append(word)

        if not blank and not wrong:
            st.success("모든 단어의 형태소 분석이 정확합니다!")
        else:
            if blank:
                st.warning("아직 분석하지 않은 단어: " + ", ".join(blank))
            if wrong:
                st.warning("다시 확인할 단어: " + ", ".join(wrong))
            st.info("정답은 바로 보여주지 않습니다. 틀린 단어만 고쳐서 다시 제출해 보세요.")


# 문항 14
with tab14:
    st.markdown(f'<div class="sentence-box"><b>문장</b><br>{SENTENCE_3}</div>', unsafe_allow_html=True)
    st.subheader("14. 문장의 형태소를 종류별로 분류해 보세요.")

    st.markdown("""
    <div class="condition-box">
    ✅ 아래 네 칸에 해당 형태소를 직접 쓰세요.<br>
    ✅ 형태소 사이는 <b>쉼표(,)</b>로 구분하세요.<br>
    ✅ 접사·어간·어미의 <b>붙임표 위치까지 정확하게</b> 써야 정답으로 인정합니다.<br>
    ✅ 형태소의 순서는 달라도 됩니다.
    </div>
    """, unsafe_allow_html=True)

    q14_self = st.text_area("자립 형태소", key="q14_self")
    q14_dependent = st.text_area("의존 형태소", key="q14_dependent")
    q14_lexical = st.text_area("실질 형태소", key="q14_lexical")
    q14_grammatical = st.text_area("형식 형태소", key="q14_grammatical")

    if st.button("14번 제출", type="primary", key="submit14_types"):
        user_map = {
            "자립 형태소": q14_self,
            "의존 형태소": q14_dependent,
            "실질 형태소": q14_lexical,
            "형식 형태소": q14_grammatical,
        }

        all_ok = True
        for category, user_text in user_map.items():
            if exact_multiset_match(user_text, Q14_TYPE_ANSWERS[category]):
                st.success(f"{category}: 정확합니다.")
            else:
                all_ok = False
                st.warning(f"{category}: 누락·중복 또는 붙임표 위치를 다시 확인해 보세요.")

        if all_ok:
            st.success("네 종류의 형태소를 모두 정확하게 분류했습니다!")


# 문항 15
with tab15:
    st.markdown(f'<div class="sentence-box"><b>문장</b><br>{SENTENCE_3}</div>', unsafe_allow_html=True)
    st.subheader("15. 문장에 쓰인 모든 단어의 품사를 쓰세요.")
    st.info("각 칸에 품사 이름을 직접 입력하세요.")

    q15_user = {}
    words15 = list(Q13_ANSWERS.keys())
    c1, c2 = st.columns(2)

    for i, word in enumerate(words15):
        with (c1 if i % 2 == 0 else c2):
            q15_user[word] = st.text_input(
                word,
                placeholder="품사 입력",
                key=f"q15_pos_{i}"
            ).strip()

    if st.button("15번 제출", type="primary", key="submit15_pos"):
        blank = []
        wrong = []

        for word, answer in Q13_ANSWERS.items():
            user_answer = q15_user[word]
            if not user_answer:
                blank.append(word)
            elif user_answer != answer:
                wrong.append(word)

        if not blank and not wrong:
            st.success("모든 단어의 품사를 정확하게 썼습니다!")
        else:
            if blank:
                st.warning("아직 쓰지 않은 단어: " + ", ".join(blank))
            if wrong:
                st.warning("다시 확인할 단어: " + ", ".join(wrong))
            st.info("정답은 바로 보여주지 않습니다. 해당 단어만 고쳐서 다시 제출해 보세요.")

st.divider()
if st.button("처음부터 다시 풀기"):
    reset_all()
