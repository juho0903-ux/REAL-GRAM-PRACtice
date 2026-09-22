import re
from collections import Counter
import streamlit as st

st.set_page_config(
    page_title="퇴계원중 1학년 중간고사 대비 문항 연습",
    page_icon="📝",
    layout="centered",
)

SENTENCE_1 = "먹구름이 가득 낀 하늘은 늘 철수가 공포에 잡아먹히게 하였다."
SENTENCE_2 = "착한 형은 지우개로 낡은 공책의 글씨를 깨끗이 지웠다."

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

st.markdown("""
<style>
.block-container {max-width: 980px; padding-top: 2rem; padding-bottom: 3rem;}
.sentence-box {
    background: #eef6ff;
    border: 1px solid #b8d8ff;
    border-radius: 14px;
    padding: 18px 20px;
    font-size: 1.08rem;
    margin: 10px 0 20px 0;
}
.condition-box {
    background: #f5f5f5;
    border-radius: 12px;
    padding: 14px 18px;
    margin: 8px 0 18px 0;
    line-height: 1.85;
}
</style>
""", unsafe_allow_html=True)

st.title("📝 퇴계원중 1학년 중간고사 대비 문항 연습")
st.caption("중간고사에 필요한 국어 문법 개념을 문항별로 연습합니다.")

tabs = st.tabs(["1️⃣ 문항 1", "2️⃣ 문항 2", "3️⃣ 문항 3", "4️⃣ 문항 4", "5️⃣ 문항 5", "6️⃣ 문항 6"])
tab1, tab2, tab3, tab4, tab5, tab6 = tabs

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

st.divider()
if st.button("처음부터 다시 풀기"):
    reset_all()
