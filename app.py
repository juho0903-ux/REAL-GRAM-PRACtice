import re
from collections import Counter
import streamlit as st

st.set_page_config(
    page_title="퇴계원중 1학년 중간고사 대비 문항 연습",
    page_icon="✏️",
    layout="centered",
)

SENTENCE_1 = "먹구름이 가득 낀 하늘은 늘 철수가 공포에 잡아먹히게 하였다."
SENTENCE_2 = "착한 형은 지우개로 낡은 공책의 글씨를 깨끗이 지웠다."
SENTENCE_3 = "어린 동생이 풋사과를 작은 접시에 가지런히 담았다."

# -----------------------------
# 문항 1~3 정답
# -----------------------------
Q1_ANSWERS = {
    "먹구름": {"morphemes": ["먹-", "구름"], "pos": "명사"},
    "잡아먹히게": {"morphemes": ["잡-", "-아", "먹-", "-히-", "-게"], "pos": "동사"},
}

Q2_ANSWERS = {
    "먹구름": "명사", "이": "조사", "가득": "부사", "낀": "동사",
    "하늘": "명사", "은": "조사", "늘": "부사", "철수": "명사",
    "가": "조사", "공포": "명사", "에": "조사", "잡아먹히게": "동사", "하였다": "동사",
}

Q3_ANSWERS = {
    "자립 형태소": ["구름", "가득", "하늘", "늘", "철수", "공포"],
    "의존 형태소": [
        "먹-", "이", "끼-", "-ㄴ", "은", "가", "에",
        "잡-", "-아", "먹-", "-히-", "-게", "하-", "-였-", "-다"
    ],
    "실질 형태소": [
        "구름", "가득", "끼-", "하늘", "늘", "철수", "공포",
        "잡-", "먹-", "하-"
    ],
    "형식 형태소": [
        "먹-", "이", "-ㄴ", "은", "가", "에",
        "-아", "-히-", "-게", "-였-", "-다"
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

if "q4_correct" not in st.session_state:
    st.session_state.q4_correct = False

if "q9_correct" not in st.session_state:
    st.session_state.q9_correct = False

st.markdown("""
<style>
:root {
    --bg: #fffaf1;
    --surface: #fffdf8;
    --surface-soft: #fff7ef;
    --mint: #d9efe7;
    --mint-deep: #8fbeb0;
    --mint-border: #c7e8dc;
    --coral: #f5a69a;
    --coral-deep: #ea8f81;
    --text-main: #3e4a49;
    --text-soft: #6d7674;
    --line: #efe6da;
    --shadow: 0 8px 24px rgba(96, 88, 72, 0.05);
    --radius-card: 20px;
    --radius-btn: 16px;
}

html, body, [class*="css"] {
    color: var(--text-main);
}

.stApp {
    background:
        radial-gradient(circle at top right, rgba(217, 239, 231, 0.28), transparent 22%),
        radial-gradient(circle at top left, rgba(245, 166, 154, 0.10), transparent 20%),
        var(--bg);
}

.block-container {
    max-width: 1080px;
    padding-top: 2rem;
    padding-bottom: 3.5rem;
    padding-left: 1.1rem;
    padding-right: 1.1rem;
}

h1, h2, h3 {
    color: var(--text-main);
    letter-spacing: -0.02em;
}

h1 {
    font-weight: 800;
    margin-bottom: 0.2rem;
}

h2, h3 {
    font-weight: 750;
}

p, label, .stCaption {
    color: var(--text-soft);
}

div[data-testid="stTabs"] {
    margin-top: 1rem;
}

div[data-baseweb="tab-list"] {
    gap: 0.45rem;
    background: rgba(255, 253, 248, 0.88);
    border: 1px solid var(--line);
    padding: 0.45rem;
    border-radius: 20px;
    box-shadow: var(--shadow);
    overflow-x: auto;
    scrollbar-width: none;
}

div[data-baseweb="tab-list"]::-webkit-scrollbar {
    display: none;
}

button[data-baseweb="tab"] {
    height: auto;
    white-space: nowrap;
    border-radius: 16px !important;
    background: transparent;
    border: 1px solid transparent;
    color: var(--text-soft);
    font-weight: 700;
    padding: 0.65rem 1rem;
    transition: all 0.18s ease;
}

button[data-baseweb="tab"]:hover {
    background: #fffaf4;
    border-color: var(--line);
    color: var(--text-main);
}

button[aria-selected="true"][data-baseweb="tab"] {
    background: var(--mint);
    border-color: var(--mint-border);
    color: var(--text-main);
    box-shadow: 0 4px 14px rgba(143, 190, 176, 0.12);
}

div[data-testid="stVerticalBlock"] > div:has(> .sentence-box),
div[data-testid="stVerticalBlock"] > div:has(> .condition-box) {
    width: 100%;
}

.sentence-box {
    background: linear-gradient(180deg, #f8fffc 0%, #f6fbf8 100%);
    border: 1px solid var(--mint-border);
    border-radius: var(--radius-card);
    padding: 20px 22px;
    font-size: 1.08rem;
    line-height: 1.7;
    margin: 10px 0 22px 0;
    box-shadow: var(--shadow);
}

.sentence-box b {
    display: inline-block;
    font-size: 1rem;
    margin-bottom: 0.35rem;
    color: var(--text-main);
}

.condition-box {
    background: linear-gradient(180deg, #fffdf9 0%, #fff8f2 100%);
    border: 1px solid var(--line);
    border-radius: var(--radius-card);
    padding: 16px 18px;
    margin: 10px 0 20px 0;
    line-height: 1.9;
    box-shadow: var(--shadow);
}

div[data-testid="stTextInputRootElement"] > div,
div[data-testid="stTextAreaRootElement"] textarea,
div[data-baseweb="input"] > div {
    border-radius: 20px !important;
}

div[data-baseweb="input"] > div,
div[data-testid="stTextAreaRootElement"] textarea {
    background: var(--surface) !important;
    border: 1px solid #eadfd2 !important;
    box-shadow: inset 0 1px 2px rgba(120, 105, 88, 0.03);
    color: var(--text-main) !important;
}

div[data-baseweb="input"] > div:hover,
div[data-testid="stTextAreaRootElement"] textarea:hover {
    border-color: var(--mint-border) !important;
}

div[data-baseweb="input"] > div:focus-within,
div[data-testid="stTextAreaRootElement"] textarea:focus {
    border-color: var(--mint-deep) !important;
    box-shadow: 0 0 0 4px rgba(217, 239, 231, 0.55) !important;
}

label[data-testid="stWidgetLabel"] p {
    font-weight: 700;
    color: var(--text-main);
}

button[kind="primary"],
button[kind="secondary"],
div.stButton > button {
    border-radius: var(--radius-btn) !important;
    min-height: 46px;
    padding: 0.62rem 1.15rem;
    font-weight: 700;
    border: 1px solid transparent;
    box-shadow: 0 6px 18px rgba(234, 143, 129, 0.14);
    transition: transform 0.15s ease, box-shadow 0.15s ease, background 0.15s ease;
}

div.stButton > button[kind="primary"] {
    background: var(--coral);
    color: white;
}

div.stButton > button[kind="primary"]:hover {
    background: var(--coral-deep);
    transform: translateY(-1px);
    box-shadow: 0 8px 20px rgba(234, 143, 129, 0.18);
}

div.stButton > button[kind="secondary"] {
    background: var(--surface);
    color: var(--text-main);
    border-color: var(--line);
}

div.stButton > button[kind="secondary"]:hover {
    background: var(--surface-soft);
    border-color: var(--mint-border);
}

div[data-testid="stAlert"] {
    border-radius: var(--radius-card);
    border: none;
    box-shadow: var(--shadow);
}

div[data-testid="stExpander"] {
    border-radius: var(--radius-card);
    border: 1px solid var(--line);
    background: rgba(255, 253, 248, 0.9);
    overflow: hidden;
    box-shadow: var(--shadow);
}

div[data-testid="stExpander"] details summary {
    padding-top: 0.1rem;
    padding-bottom: 0.1rem;
    color: var(--text-main);
    font-weight: 700;
}

hr {
    border-color: var(--line);
    margin-top: 2.2rem;
    margin-bottom: 1.4rem;
}

@media (max-width: 768px) {
    .block-container {
        padding-top: 1.1rem;
        padding-left: 0.85rem;
        padding-right: 0.85rem;
        padding-bottom: 2.5rem;
    }

    h1 {
        font-size: 1.8rem;
        line-height: 1.25;
    }

    h2, h3 {
        font-size: 1.45rem;
        line-height: 1.3;
    }

    .sentence-box,
    .condition-box {
        padding: 16px 16px;
        border-radius: 18px;
    }

    div.stButton > button {
        width: 100%;
    }

    button[data-baseweb="tab"] {
        padding: 0.58rem 0.9rem;
        font-size: 0.96rem;
    }
}
</style>
""", unsafe_allow_html=True)

st.title("퇴계원중 1학년 중간고사 대비 문항 연습")
st.caption("중간고사에 필요한 국어 문법 개념을 문항별로 연습합니다.")

tabs = st.tabs([
    "1️⃣ 문항 1", "2️⃣ 문항 2", "3️⃣ 문항 3", "4️⃣ 문항 4",
    "5️⃣ 문항 5", "6️⃣ 문항 6", "7️⃣ 문항 7", "8️⃣ 문항 8",
    "9️⃣ 문항 9", "🔟 문항 10", "11 문항 11", "12 문항 12", "13 문항 13"
])
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12, tab13 = tabs

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
            if "잡아먹히게" in wrong:
                with st.expander("💡 '잡아먹히게' 힌트 보기"):
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
            st.session_state.q4_correct = True
            st.success("파생어를 모두 정확하게 찾았습니다!")
        else:
            st.session_state.q4_correct = False
            st.warning("파생어를 다시 확인해 보세요.")
            with st.expander("힌트 보기"):
                st.write("어근에 접사가 붙어 새 단어가 된 경우를 찾아보세요.")

# 문항 5
with tab5:
    st.markdown(f'<div class="sentence-box"><b>문장</b><br>{SENTENCE_2}</div>', unsafe_allow_html=True)
    st.subheader("5. 문항 4에서 찾은 파생어를 형태소 단위로 분석하세요.")

    if not st.session_state.q4_correct:
        st.info("문항 4를 먼저 정확하게 해결한 뒤 풀 수 있습니다.")
    else:
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

    if not st.session_state.q4_correct:
        st.info("문항 4를 먼저 정확하게 해결한 뒤 풀 수 있습니다.")
    else:
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
    st.markdown(f'<div class="sentence-box"><b>문장</b><br>{SENTENCE_3}</div>', unsafe_allow_html=True)
    st.subheader("9. 윗문장에서 파생어를 모두 찾아 쓰세요.")

    q9_1 = st.text_input("파생어 1", key="q9_1")
    q9_2 = st.text_input("파생어 2", key="q9_2")

    if st.button("9번 제출", type="primary", key="submit9"):
        answers = [q9_1.strip(), q9_2.strip()]
        if Counter(answers) == Counter(Q9_ANSWERS):
            st.session_state.q9_correct = True
            st.success("파생어를 모두 정확하게 찾았습니다!")
        else:
            st.session_state.q9_correct = False
            st.warning("파생어를 다시 확인해 보세요.")
            with st.expander("힌트 보기"):
                st.write("어근에 접사가 붙어 새 단어가 된 경우를 찾아보세요.")


# 문항 10
with tab10:
    st.markdown(f'<div class="sentence-box"><b>문장</b><br>{SENTENCE_3}</div>', unsafe_allow_html=True)
    st.subheader("10. 문항 9에서 찾은 파생어를 형태소 단위로 분석하세요.")

    if not st.session_state.q9_correct:
        st.info("문항 9를 먼저 정확하게 해결한 뒤 풀 수 있습니다.")
    else:
        st.markdown("""
        <div class="condition-box">
        ✅ 형태소 분석 시 붙임표를 정확하게 표시하세요.
        </div>
        """, unsafe_allow_html=True)

        q10_1 = st.text_input("풋사과", key="q10_1")
        q10_2 = st.text_input("가지런히", key="q10_2")

        if st.button("10번 제출", type="primary", key="submit10"):
            wrong = []
            if normalize_sequence(q10_1) != Q10_ANSWERS["풋사과"]:
                wrong.append("풋사과")
            if normalize_sequence(q10_2) != Q10_ANSWERS["가지런히"]:
                wrong.append("가지런히")

            if not wrong:
                st.success("두 파생어의 형태소 분석이 모두 정확합니다!")
            else:
                st.warning("다시 확인할 단어: " + ", ".join(wrong))
                st.info("형태소의 순서와 붙임표 위치까지 확인해 보세요.")


# 문항 11
with tab11:
    st.markdown(f'<div class="sentence-box"><b>문장</b><br>{SENTENCE_3}</div>', unsafe_allow_html=True)
    st.subheader("11. 문항 9에서 찾은 각 파생어의 품사를 쓰세요.")

    if not st.session_state.q9_correct:
        st.info("문항 9를 먼저 정확하게 해결한 뒤 풀 수 있습니다.")
    else:
        q11_1 = st.text_input("풋사과", placeholder="품사 입력", key="q11_1")
        q11_2 = st.text_input("가지런히", placeholder="품사 입력", key="q11_2")

        if st.button("11번 제출", type="primary", key="submit11"):
            wrong = []
            if q11_1.strip() != Q11_ANSWERS["풋사과"]:
                wrong.append("풋사과")
            if q11_2.strip() != Q11_ANSWERS["가지런히"]:
                wrong.append("가지런히")

            if not wrong:
                st.success("두 파생어의 품사를 모두 정확하게 썼습니다!")
            else:
                st.warning("다시 확인할 단어: " + ", ".join(wrong))


# 문항 12
with tab12:
    st.markdown(f'<div class="sentence-box"><b>문장</b><br>{SENTENCE_3}</div>', unsafe_allow_html=True)
    st.subheader("12. 문장에 쓰인 모든 단어를 형태소 단위로 분석하세요.")

    st.markdown("""
    <div class="condition-box">
    ✅ 각 단어를 형태소 단위로 분석하세요.<br>
    ✅ 형태소 사이는 <b>쉼표(,)</b> 또는 <b>슬래시(/)</b>로 구분해도 됩니다.<br>
    ✅ 접사·어간·어미의 <b>붙임표 위치까지 정확하게</b> 써야 정답으로 인정합니다.
    </div>
    """, unsafe_allow_html=True)

    q12_user = {}
    words12 = list(Q12_ANSWERS.keys())
    c1, c2 = st.columns(2)

    for i, word in enumerate(words12):
        with (c1 if i % 2 == 0 else c2):
            q12_user[word] = st.text_input(
                word,
                placeholder="형태소 분석",
                key=f"q12_{i}"
            )

    if st.button("12번 제출", type="primary", key="submit12"):
        blank = []
        wrong = []

        for word, answer in Q12_ANSWERS.items():
            user_answer = q12_user[word]
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


# 문항 13
with tab13:
    st.markdown(f'<div class="sentence-box"><b>문장</b><br>{SENTENCE_3}</div>', unsafe_allow_html=True)
    st.subheader("13. 문장에 쓰인 모든 단어의 품사를 쓰세요.")
    st.info("각 칸에 품사 이름을 직접 입력하세요.")

    q13_user = {}
    words13 = list(Q13_ANSWERS.keys())
    c1, c2 = st.columns(2)

    for i, word in enumerate(words13):
        with (c1 if i % 2 == 0 else c2):
            q13_user[word] = st.text_input(
                word,
                placeholder="품사 입력",
                key=f"q13_{i}"
            ).strip()

    if st.button("13번 제출", type="primary", key="submit13"):
        blank = []
        wrong = []

        for word, answer in Q13_ANSWERS.items():
            user_answer = q13_user[word]
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
