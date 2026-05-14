import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import urllib.parse # 한글 시트명 처리를 위해 추가

# ==========================================================
# 1. 여기에 본인의 구글 스프레드시트 주소를 입력하세요!
# ==========================================================
SHEET_URL = "https://docs.google.com/spreadsheets/d/1nyucTUzbpF6NIXYFV3V_mpHWRtf2gkMkKTkS-xwPXNg/edit?usp=sharing"
# ==========================================================

# 페이지 기본 설정
st.set_page_config(
    page_title="KGC 마케팅 전략 대시보드",
    page_icon="🔴",
    layout="wide"
)

# KGC 브랜드 스타일 적용 (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    :root { --kgc-red: #b91c1c; --dark-slate: #1e293b; }
    .main { background-color: #f1f5f9; font-family: 'Noto Sans KR', sans-serif; }
    .kgc-header {
        background-color: var(--dark-slate);
        color: white;
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
    }
    .insight-box {
        background-color: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border-left: 6px solid var(--kgc-red);
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=600) # 10분 캐싱
def load_data(url):
    # 1. 스프레드시트 ID 추출
    try:
        sheet_id = url.split("/d/")[1].split("/")[0]
    except IndexError:
        raise Exception("올바르지 않은 구글 시트 URL 형식입니다.")

    # 2. 공용 CSV 접근 URL 생성 함수 (한글 시트명 인코딩 지원)
    def get_csv_url(sheet_name):
        encoded_name = urllib.parse.quote(sheet_name)
        return f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={encoded_name}"

    # 3. 각 시트 읽기 (GSheetsConnection 대신 Pandas 직접 사용)
    # KPI 시트 읽기
    full_kpi = pd.read_csv(get_csv_url("KPI"))
    kpi_df = full_kpi.head(4) # 상단 4개 지표
    summary = full_kpi.iloc[5, 0] if len(full_kpi) > 5 else "데이터 분석 중..."
    
    # 지역 및 연령 시트 읽기
    region_df = pd.read_csv(get_csv_url("지역"))
    age_df = pd.read_csv(get_csv_url("연령"))
    
    return kpi_df, summary, region_df, age_df

try:
    # 데이터 불러오기 실행
    df_kpi, summary_text, df_region, df_age = load_data(SHEET_URL)

    # [상단 헤더]
    st.markdown(f"""
        <div class="kgc-header">
            <h1 style='margin:0; font-size: 2.2rem;'>정관장 에브리타임 밸런스 <span style='color:#f87171;'>전략 리포트</span></h1>
            <p style='margin:0.5rem 0 0 0; color:#94a3b8;'>기준일: {datetime.now().strftime('%Y.%m.%d')} (Public View 모드)</p>
        </div>
        """, unsafe_allow_html=True)

    # [전략 인사이트 박스]
    st.markdown(f"""
        <div class="insight-box">
            <h4 style='margin-top:0; color:#1e293b;'>📢 Weekly Strategic Insight</h4>
            <p style='margin:0; color:#334155; font-size: 1.1rem; line-height: 1.6;'>{summary_text}</p>
        </div>
        """, unsafe_allow_html=True)

    # [KPI 지표 레이아웃]
    cols = st.columns(4)
    for i, row in df_kpi.iterrows():
        with cols[i]:
            val = row['value']
            # 숫자형 데이터 포맷팅
            if isinstance(val, (int, float)):
                display_val = f"{val*100:.1f}%" if val <= 1 else f"{val:,.0f}"
            else:
                display_val = str(val)
            st.metric(label=row['label'], value=display_val, delta=row['delta'])

    st.write("---")

    # [하단 차트 섹션]
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("📍 지역별 성장률 (편의점 vs 마트)")
        fig_region = px.bar(
            df_region, x='지역', y='성장률', text_auto=True,
            color='성장률', color_continuous_scale=['#fca5a5', '#b91c1c']
        )
        fig_region.update_layout(plot_bgcolor='rgba(0,0,0,0)', yaxis_title="성장률 (%)", xaxis_title=None)
        st.plotly_chart(fig_region, use_container_width=True)

    with col_right:
        st.subheader("👥 구매 연령대별 비중")
        fig_age = px.pie(
            df_age, names='연령대', values='비중', hole=0.4,
            color_discrete_sequence=['#b91c1c', '#334155', '#94a3b8']
        )
        fig_age.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_age, use_container_width=True)

except Exception as e:
    st.error(f"데이터 연동 중 오류가 발생했습니다.")
    st.write(f"상세 에러 내용: {e}")
    st.info("💡 해결 방법: 구글 시트 우상단 [공유] 버튼 클릭 -> [일반 액세스]를 '링크가 있는 모든 사용자'와 '뷰어'로 설정했는지 다시 확인해 주세요.")

st.markdown("<br><p style='text-align:center; color:#94a3b8; font-size:0.75rem;'>본 리포트는 구글 스프레드시트의 공개 데이터를 실시간으로 참조합니다.</p>", unsafe_allow_html=True)
