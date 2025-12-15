"""
바이오가스 사업성 종합 분석 대시보드 v3.0
Biogas Feasibility Comprehensive Analysis Dashboard
- 수도권 음식물쓰레기 발생량 지도
- 지역별 처리업체 현황
- 데이터 다운로드 기능
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from io import BytesIO

# ============================================================
# 페이지 설정
# ============================================================
st.set_page_config(
    page_title="바이오가스 사업성 종합 분석",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CSS 스타일
# ============================================================
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: bold;
        color: #1B5E20;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #E8F5E9 0%, #C8E6C9 100%);
        border-radius: 10px;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #BBDEFB 100%, #BBDEFB 100%);
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 5px solid #1976D2;
        margin: 0.5rem 0;
        color: #333333;
    }
    .revenue-card {
        background: linear-gradient(135deg, #C8E6C9 100%, #C8E6C9 100%);
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin: 0.5rem 0;
        color: #333333;
    }
    .highlight-box {
        background: linear-gradient(135deg, #FFECB3 100%, #FFECB3 100%);
        padding: 1.2rem;
        border-radius: 10px;
        border: 2px solid #FF8F00;
        margin: 1rem 0;
        color: #333333;
    }
    .saf-box {
        background: linear-gradient(135deg, #B3E5FC 100%, #B3E5FC 100%);
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 5px solid #0288D1;
        margin: 0.5rem 0;
        color: #333333;
    }
    .carbon-box {
        background: linear-gradient(135deg, #E1BEE7 100%, #E1BEE7 100%);
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 5px solid #7B1FA2;
        margin: 0.5rem 0;
        color: #333333;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 상수 정의
# ============================================================
KWH_TO_MJ = 3.6
MJ_TO_KWH = 0.27778
BIOGAS_ENERGY_KWH_NM3 = 6
BIOGAS_ENERGY_MJ_NM3 = 21.6
METHANE_ENERGY_KWH_NM3 = 10
METHANE_ENERGY_MJ_NM3 = 35.8
METHANE_ENERGY_MJ_KG = 50
METHANE_DENSITY_KG_NM3 = 0.717
SAF_DENSITY_KG_L = 0.8
SAF_MASS_PER_BARREL_KG = 127.2
SAF_ENERGY_MJ_KG = 43
CO2_REDUCTION_PER_TON_WASTE = 0.18
BIOGAS_YIELD_FOOD_WASTE = 130
BIOGAS_YIELD_LIVESTOCK = 20

# ============================================================
# 서울시 자치구별 음식물쓰레기 데이터 (톤/일, 2023년)
# ============================================================
SEOUL_FOOD_WASTE_DATA = {
    '종로구': {'발생량': 79.9, '사료화': 65.0, '퇴비화': 14.0, '기타': 0.9, 'lat': 37.5735, 'lon': 126.9790},
    '중구': {'발생량': 101.7, '사료화': 47.2, '퇴비화': 30.4, '기타': 24.0, 'lat': 37.5640, 'lon': 126.9975},
    '용산구': {'발생량': 63.2, '사료화': 55.9, '퇴비화': 7.0, '기타': 0.2, 'lat': 37.5326, 'lon': 126.9909},
    '성동구': {'발생량': 75.8, '사료화': 41.1, '퇴비화': 7.0, '기타': 27.7, 'lat': 37.5634, 'lon': 127.0369},
    '광진구': {'발생량': 83.4, '사료화': 72.9, '퇴비화': 8.8, '기타': 1.7, 'lat': 37.5384, 'lon': 127.0822},
    '동대문구': {'발생량': 85.8, '사료화': 6.6, '퇴비화': 3.8, '기타': 75.4, 'lat': 37.5744, 'lon': 127.0400},
    '중랑구': {'발생량': 79.9, '사료화': 25.1, '퇴비화': 4.2, '기타': 50.7, 'lat': 37.6063, 'lon': 127.0928},
    '성북구': {'발생량': 92.4, '사료화': 3.3, '퇴비화': 71.3, '기타': 17.9, 'lat': 37.5894, 'lon': 127.0167},
    '강북구': {'발생량': 60.6, '사료화': 1.9, '퇴비화': 21.0, '기타': 37.8, 'lat': 37.6396, 'lon': 127.0257},
    '도봉구': {'발생량': 74.0, '사료화': 67.6, '퇴비화': 5.1, '기타': 1.2, 'lat': 37.6688, 'lon': 127.0471},
    '노원구': {'발생량': 111.2, '사료화': 5.3, '퇴비화': 61.6, '기타': 44.3, 'lat': 37.6542, 'lon': 127.0568},
    '은평구': {'발생량': 72.6, '사료화': 47.0, '퇴비화': 8.0, '기타': 17.6, 'lat': 37.6027, 'lon': 126.9291},
    '서대문구': {'발생량': 61.0, '사료화': 4.3, '퇴비화': 55.2, '기타': 1.4, 'lat': 37.5791, 'lon': 126.9368},
    '마포구': {'발생량': 78.8, '사료화': 3.1, '퇴비화': 73.7, '기타': 2.0, 'lat': 37.5663, 'lon': 126.9014},
    '양천구': {'발생량': 82.1, '사료화': 62.2, '퇴비화': 19.4, '기타': 0.5, 'lat': 37.5170, 'lon': 126.8667},
    '강서구': {'발생량': 122.3, '사료화': 49.4, '퇴비화': 70.3, '기타': 2.6, 'lat': 37.5509, 'lon': 126.8495},
    '구로구': {'발생량': 77.4, '사료화': 53.5, '퇴비화': 22.1, '기타': 1.8, 'lat': 37.4954, 'lon': 126.8874},
    '금천구': {'발생량': 53.1, '사료화': 44.7, '퇴비화': 7.1, '기타': 1.3, 'lat': 37.4569, 'lon': 126.8955},
    '영등포구': {'발생량': 133.2, '사료화': 89.5, '퇴비화': 42.4, '기타': 1.3, 'lat': 37.5264, 'lon': 126.8963},
    '동작구': {'발생량': 78.8, '사료화': 70.1, '퇴비화': 8.5, '기타': 0.2, 'lat': 37.5124, 'lon': 126.9393},
    '관악구': {'발생량': 86.0, '사료화': 80.1, '퇴비화': 5.6, '기타': 0.3, 'lat': 37.4784, 'lon': 126.9516},
    '서초구': {'발생량': 138.1, '사료화': 87.2, '퇴비화': 14.1, '기타': 36.9, 'lat': 37.4837, 'lon': 127.0324},
    '강남구': {'발생량': 235.3, '사료화': 191.8, '퇴비화': 40.1, '기타': 3.3, 'lat': 37.5172, 'lon': 127.0473},
    '송파구': {'발생량': 187.3, '사료화': 181.3, '퇴비화': 5.6, '기타': 0.4, 'lat': 37.5145, 'lon': 127.1058},
    '강동구': {'발생량': 105.6, '사료화': 101.4, '퇴비화': 3.7, '기타': 0.5, 'lat': 37.5301, 'lon': 127.1238},
}

GYEONGGI_FOOD_WASTE_DATA = {
    '수원시': {'발생량': 320.5, 'lat': 37.2636, 'lon': 127.0286},
    '성남시': {'발생량': 285.3, 'lat': 37.4200, 'lon': 127.1267},
    '고양시': {'발생량': 298.7, 'lat': 37.6584, 'lon': 126.8320},
    '용인시': {'발생량': 310.2, 'lat': 37.2411, 'lon': 127.1776},
    '부천시': {'발생량': 245.6, 'lat': 37.5034, 'lon': 126.7660},
    '안산시': {'발생량': 198.4, 'lat': 37.3219, 'lon': 126.8309},
    '안양시': {'발생량': 165.8, 'lat': 37.3943, 'lon': 126.9568},
    '남양주시': {'발생량': 195.3, 'lat': 37.6360, 'lon': 127.2165},
    '화성시': {'발생량': 248.9, 'lat': 37.1996, 'lon': 126.8312},
    '평택시': {'발생량': 152.7, 'lat': 36.9921, 'lon': 127.1128},
    '의정부시': {'발생량': 125.4, 'lat': 37.7381, 'lon': 127.0337},
    '시흥시': {'발생량': 145.2, 'lat': 37.3800, 'lon': 126.8028},
    '파주시': {'발생량': 132.8, 'lat': 37.7599, 'lon': 126.7800},
    '김포시': {'발생량': 128.6, 'lat': 37.6152, 'lon': 126.7156},
    '광명시': {'발생량': 95.3, 'lat': 37.4786, 'lon': 126.8644},
    '광주시': {'발생량': 112.5, 'lat': 37.4294, 'lon': 127.2551},
    '군포시': {'발생량': 85.6, 'lat': 37.3617, 'lon': 126.9352},
    '하남시': {'발생량': 78.9, 'lat': 37.5395, 'lon': 127.2148},
    '오산시': {'발생량': 68.4, 'lat': 37.1498, 'lon': 127.0772},
    '이천시': {'발생량': 65.2, 'lat': 37.2719, 'lon': 127.4351},
}

SEOUL_FACILITIES = [
    {'시설명': '노원자원회수시설', '구': '노원구', '용량(톤/일)': 800, '처리량(톤/년)': 158687, '발전용량(MW)': 25, '운영방식': '연속식'},
    {'시설명': '은평환경플랜트', '구': '은평구', '용량(톤/일)': 48, '처리량(톤/년)': 13215, '발전용량(MW)': 3, '운영방식': '연속식'},
    {'시설명': '마포자원회수시설', '구': '마포구', '용량(톤/일)': 750, '처리량(톤/년)': 175354, '발전용량(MW)': 35, '운영방식': '연속식'},
    {'시설명': '양천자원회수시설', '구': '양천구', '용량(톤/일)': 400, '처리량(톤/년)': 104409, '발전용량(MW)': 17, '운영방식': '연속식'},
    {'시설명': '강남자원회수시설', '구': '강남구', '용량(톤/일)': 900, '처리량(톤/년)': 235025, '발전용량(MW)': 45, '운영방식': '연속식'},
]

GYEONGGI_FACILITIES = [
    {'시설명': '수원환경시설사업소', '시군': '수원시', '용량(톤/일)': 300, '처리량(톤/년)': 89250, '운영방식': '연속식'},
    {'시설명': '성남환경에너지시설', '시군': '성남시', '용량(톤/일)': 350, '처리량(톤/년)': 98500, '운영방식': '연속식'},
    {'시설명': '고양자원회수시설', '시군': '고양시', '용량(톤/일)': 400, '처리량(톤/년)': 112000, '운영방식': '연속식'},
    {'시설명': '용인시자원회수센터', '시군': '용인시', '용량(톤/일)': 200, '처리량(톤/년)': 56800, '운영방식': '연속식'},
    {'시설명': '안산자원회수시설', '시군': '안산시', '용량(톤/일)': 300, '처리량(톤/년)': 85600, '운영방식': '연속식'},
    {'시설명': '화성환경에너지센터', '시군': '화성시', '용량(톤/일)': 250, '처리량(톤/년)': 72500, '운영방식': '연속식'},
    {'시설명': '평택환경에너지센터', '시군': '평택시', '용량(톤/일)': 200, '처리량(톤/년)': 58000, '운영방식': '연속식'},
    {'시설명': '의정부자원회수시설', '시군': '의정부시', '용량(톤/일)': 150, '처리량(톤/년)': 43500, '운영방식': '연속식'},
    {'시설명': '남양주자원회수시설', '시군': '남양주시', '용량(톤/일)': 200, '처리량(톤/년)': 58000, '운영방식': '연속식'},
    {'시설명': '부천자원회수시설', '시군': '부천시', '용량(톤/일)': 250, '처리량(톤/년)': 72500, '운영방식': '연속식'},
]

# ============================================================
# 헤더
# ============================================================
st.markdown('<div class="main-header">⚡ 바이오가스 사업성 종합 분석 대시보드 v3.0</div>', unsafe_allow_html=True)
st.markdown("##### Biogas Feasibility Analysis with Regional Map, Facility Status & Data Export")

# ============================================================
# 사이드바
# ============================================================
with st.sidebar:
    st.markdown("## 📊 사업 파라미터 설정")
    daily_capacity = st.slider("일일 처리량 (톤/일)", 50, 1000, 300, 10)
    food_waste_ratio = st.slider("음식물쓰레기 비율 (%)", 0, 100, 50, 5)
    livestock_ratio = 100 - food_waste_ratio
    
    st.markdown(f"""
    <div class="metric-card">
    <b>📦 투입량</b><br>
    • 음식물: {daily_capacity * food_waste_ratio / 100:.0f} 톤/일<br>
    • 축분: {daily_capacity * livestock_ratio / 100:.0f} 톤/일<br>
    <hr style="margin:8px 0; border-color:#1976D2;">
    <b>⚡ 바이오가스 발생량</b><br>
    • 음식물: {daily_capacity * food_waste_ratio / 100 * 130:.0f} Nm³/일 <small>(130 Nm³/톤)</small><br>
    • 축분: {daily_capacity * livestock_ratio / 100 * 20:.0f} Nm³/일 <small>(20 Nm³/톤)</small><br>
    • <b>합계: {daily_capacity * food_waste_ratio / 100 * 130 + daily_capacity * livestock_ratio / 100 * 20:,.0f} Nm³/일</b><br>
    <hr style="margin:8px 0; border-color:#1976D2;">
    <small>※ 음식물이 축분 대비 <b>6.5배</b> 가스 발생<br>
    (130÷20 = 6.5배)</small>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    tipping_fee_food = st.number_input("음식물 티핑피 (원/톤)", 50000, 200000, 140000, 10000)
    tipping_fee_livestock = st.number_input("축분 티핑피 (원/톤)", 10000, 100000, 30000, 5000)
    
    st.markdown("---")
    operating_days = st.slider("연간 가동일수", 200, 365, 330, 5)
    utilization_rate = st.slider("가동률 (%)", 50, 100, 80, 5)
    methane_content = st.slider("메탄 함량 (%)", 50, 70, 60, 1)
    power_gen_efficiency = st.slider("발전 효율 (%)", 20, 45, 30, 1)
    
    st.markdown("---")
    smp_price = st.number_input("SMP 가격 (원/kWh)", 50, 200, 100, 5)
    rec_price = st.number_input("REC 가격 (원/kWh)", 30, 150, 70, 5)
    rng_price = st.number_input("바이오가스 RNG (원/Nm³)", 500, 2000, 900, 50)
    saf_price_usd = st.number_input("SAF 가격 (USD/톤)", 1500, 5000, 2700, 100)
    exchange_rate = st.number_input("환율 (원/USD)", 1200, 1500, 1400, 10)
    carbon_credit_price = st.number_input("탄소배출권 가격 (원/tCO2)", 5000, 20000, 10000, 500)

# ============================================================
# 계산
# ============================================================
food_waste_daily = daily_capacity * food_waste_ratio / 100
livestock_daily = daily_capacity * livestock_ratio / 100
annual_capacity = daily_capacity * operating_days

tipping_revenue_annual = (food_waste_daily * tipping_fee_food + livestock_daily * tipping_fee_livestock) * operating_days

biogas_daily = (food_waste_daily * BIOGAS_YIELD_FOOD_WASTE + livestock_daily * BIOGAS_YIELD_LIVESTOCK) * (utilization_rate / 100)
biogas_annual = biogas_daily * operating_days

methane_daily = biogas_daily * (methane_content / 100)
methane_annual = methane_daily * operating_days
methane_mass_annual = methane_annual * METHANE_DENSITY_KG_NM3

power_daily_kwh = biogas_daily * BIOGAS_ENERGY_KWH_NM3 * (power_gen_efficiency / 100)
power_annual_kwh = power_daily_kwh * operating_days
power_annual_gwh = power_annual_kwh / 1000000
power_revenue_annual = power_annual_kwh * (smp_price + rec_price)

rng_purification_rate = 0.90
rng_annual = methane_daily * rng_purification_rate * operating_days
rng_revenue_annual = rng_annual * rng_price

gtl_efficiency = 0.55
saf_cut_ratio = 0.25
saf_mass_kg = methane_mass_annual * METHANE_ENERGY_MJ_KG * gtl_efficiency * saf_cut_ratio / SAF_ENERGY_MJ_KG
saf_mass_ton = saf_mass_kg / 1000
saf_barrels = saf_mass_kg / SAF_MASS_PER_BARREL_KG
saf_revenue_krw = saf_mass_ton * saf_price_usd * exchange_rate

carbon_reduction_annual = annual_capacity * CO2_REDUCTION_PER_TON_WASTE
carbon_credit_revenue = carbon_reduction_annual * carbon_credit_price

# ============================================================
# 탭 구성
# ============================================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 종합 현황", "🗺️ 수도권 지도", "🏭 처리업체 현황",
    "💰 재무 분석", "📐 환산 테이블", "📥 데이터 다운로드"
])

# ============================================================
# 탭1: 종합 현황
# ============================================================
with tab1:
    st.markdown("## 📊 사업 종합 현황")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("일일 처리량", f"{daily_capacity:,.0f} 톤", f"연간 {annual_capacity:,.0f} 톤")
    with col2:
        st.metric("일일 바이오가스", f"{biogas_daily:,.0f} Nm³", f"연간 {biogas_annual/1000000:.2f} 백만Nm³")
    with col3:
        st.metric("일일 전력생산", f"{power_daily_kwh:,.0f} kWh", f"연간 {power_annual_gwh:.2f} GWh")
    with col4:
        st.metric("연간 SAF 생산", f"{saf_mass_ton:,.1f} 톤", f"{saf_barrels:,.0f} 배럴")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        revenue_df = pd.DataFrame({
            '수익원': ['티핑피', '전력(SMP+REC)', 'RNG', 'SAF', '탄소배출권'],
            '연간 수익(억원)': [
                tipping_revenue_annual / 1e8, power_revenue_annual / 1e8,
                rng_revenue_annual / 1e8, saf_revenue_krw / 1e8, carbon_credit_revenue / 1e8
            ]
        })
        fig1 = px.bar(revenue_df, x='수익원', y='연간 수익(억원)', color='수익원',
                     title='수익원별 연간 수익 비교', color_discrete_sequence=px.colors.qualitative.Set2)
        fig1.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # 3D Scatter: 에너지 수익화 방식 종합 매력도 비교
        # X축: 기술성숙도/상용화수준 (1-10, 높을수록 성숙)
        # Y축: 단위수익성 (원/Nm³ 바이오가스 기준)
        # Z축: 리스크 수준 (1-10, 낮을수록 안전)
        
        # 단위수익 계산 (바이오가스 1 Nm³ 기준)
        # 전력: 6 kWh × 30% 효율 × (SMP+REC) = 1.8 × 170 = 306원/Nm³
        unit_revenue_power = 6 * (power_gen_efficiency/100) * (smp_price + rec_price)
        # RNG: 60% 메탄 × 90% 정제율 × RNG가격 = 0.54 × 900 = 486원/Nm³
        unit_revenue_rng = (methane_content/100) * 0.90 * rng_price
        # SAF: 복잡한 변환... 대략 추정 (GTL 55% × SAF 25% × 에너지 환산)
        # 메탄 0.6 Nm³ × 0.717 kg × 50 MJ/kg × 55% GTL × 25% SAF cut / 43 MJ/kg SAF × SAF가격
        unit_revenue_saf = (methane_content/100) * METHANE_DENSITY_KG_NM3 * METHANE_ENERGY_MJ_KG * 0.55 * 0.25 / SAF_ENERGY_MJ_KG * (saf_price_usd * exchange_rate / 1000)
        
        energy_comparison_df = pd.DataFrame({
            '수익화방식': ['전력(SMP+REC)', 'RNG', 'SAF'],
            '기술성숙도': [8, 7, 2],  # 전력 가장 성숙, SAF는 초기단계
            '단위수익(원/Nm³)': [unit_revenue_power, unit_revenue_rng, unit_revenue_saf],
            '리스크수준': [3, 4, 8],  # 전력은 SMP변동, RNG 안정적, SAF는 환율+유가 변동
            '시장성장성': [3, 5, 9],  # 전력 포화, RNG 성장, SAF 고성장
            '정책지원도': [6, 8, 9],  # REC, RNG인센티브, SAF의무화
            '연간수익(억원)': [power_revenue_annual/1e8, rng_revenue_annual/1e8, saf_revenue_krw/1e8]
        })
        
        fig_3d = go.Figure(data=[go.Scatter3d(
            x=energy_comparison_df['기술성숙도'],
            y=energy_comparison_df['단위수익(원/Nm³)'],
            z=energy_comparison_df['리스크수준'],
            mode='markers+text',
            marker=dict(
                size=[25, 25, 25],
                color=['#2196F3', '#4CAF50', '#FF9800'],
                opacity=0.8,
                line=dict(color='white', width=2)
            ),
            text=energy_comparison_df['수익화방식'],
            textposition='top center',
            textfont=dict(size=12, color='white'),
            hovertemplate=(
                '<b>%{text}</b><br>' +
                '기술성숙도: %{x}/10<br>' +
                '단위수익: %{y:.0f}원/Nm³<br>' +
                '리스크: %{z}/10<br>' +
                '<extra></extra>'
            )
        )])
        
        fig_3d.update_layout(
            title='에너지 수익화 방식 종합 매력도 비교',
            scene=dict(
                xaxis=dict(title='기술성숙도 (←높을수록 상용화)', range=[0, 10], backgroundcolor='rgba(0,0,0,0)'),
                yaxis=dict(title='단위수익 (원/Nm³)', backgroundcolor='rgba(0,0,0,0)'),
                zaxis=dict(title='리스크수준 (→낮을수록 안전)', range=[0, 10], backgroundcolor='rgba(0,0,0,0)'),
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.2))
            ),
            height=450,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        st.plotly_chart(fig_3d, use_container_width=True)
        
        # 범례/설명
        st.markdown("""
        <small>
        📊 <b>축 설명</b><br>
        • <b>X축 (기술성숙도)</b>: 상용화 수준 (10=완전 상용화)<br>
        • <b>Y축 (단위수익)</b>: 바이오가스 1Nm³당 수익 (원)<br>
        • <b>Z축 (리스크)</b>: 가격변동성, 환율 등 (10=고위험)<br>
        💡 <b>이상적 위치</b>: X↑ Y↑ Z↓ (우측 상단 아래)
        </small>
        """, unsafe_allow_html=True)

# ============================================================
# 탭2: 수도권 지도
# ============================================================
with tab2:
    st.markdown("## 🗺️ 수도권 음식물쓰레기 발생량 현황")
    
    seoul_df = pd.DataFrame([
        {'지역': k, '발생량(톤/일)': v['발생량'], 'lat': v['lat'], 'lon': v['lon'], '구분': '서울'}
        for k, v in SEOUL_FOOD_WASTE_DATA.items()
    ])
    
    gyeonggi_df = pd.DataFrame([
        {'지역': k, '발생량(톤/일)': v['발생량'], 'lat': v['lat'], 'lon': v['lon'], '구분': '경기'}
        for k, v in GYEONGGI_FOOD_WASTE_DATA.items()
    ])
    
    all_df = pd.concat([seoul_df, gyeonggi_df], ignore_index=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("서울시 총 발생량", f"{seoul_df['발생량(톤/일)'].sum():,.1f} 톤/일")
    with col2:
        st.metric("경기도 주요시군", f"{gyeonggi_df['발생량(톤/일)'].sum():,.1f} 톤/일")
    with col3:
        st.metric("수도권 합계", f"{all_df['발생량(톤/일)'].sum():,.1f} 톤/일")
    with col4:
        st.metric("연간 환산", f"{all_df['발생량(톤/일)'].sum() * 365 / 10000:.1f} 만톤/년")
    
    region_choice = st.radio("지역 선택:", ["전체 수도권", "서울시", "경기도"], horizontal=True)
    
    if region_choice == "서울시":
        map_df, center_lat, center_lon, zoom = seoul_df, 37.5665, 126.9780, 10.5
    elif region_choice == "경기도":
        map_df, center_lat, center_lon, zoom = gyeonggi_df, 37.4138, 127.0183, 8.5
    else:
        map_df, center_lat, center_lon, zoom = all_df, 37.5000, 127.0000, 9
    
    fig_map = px.scatter_mapbox(
        map_df, lat='lat', lon='lon', size='발생량(톤/일)', color='구분',
        hover_name='지역', hover_data={'발생량(톤/일)': ':.1f', 'lat': False, 'lon': False},
        title=f'{region_choice} 음식물쓰레기 발생량',
        color_discrete_map={'서울': '#E53935', '경기': '#1E88E5'},
        size_max=40, zoom=zoom, center={'lat': center_lat, 'lon': center_lon}
    )
    fig_map.update_layout(mapbox_style='carto-positron', height=600, margin={'r': 0, 't': 50, 'l': 0, 'b': 0})
    st.plotly_chart(fig_map, use_container_width=True)
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        top10_seoul = seoul_df.nlargest(10, '발생량(톤/일)')
        fig_bar1 = px.bar(top10_seoul, x='지역', y='발생량(톤/일)',
                        color='발생량(톤/일)', color_continuous_scale='Reds',
                        title='서울시 음식물쓰레기 발생량 Top 10')
        fig_bar1.update_layout(height=400)
        st.plotly_chart(fig_bar1, use_container_width=True)
    
    with col2:
        top10_gg = gyeonggi_df.nlargest(10, '발생량(톤/일)')
        fig_bar2 = px.bar(top10_gg, x='지역', y='발생량(톤/일)',
                        color='발생량(톤/일)', color_continuous_scale='Blues',
                        title='경기도 음식물쓰레기 발생량 Top 10')
        fig_bar2.update_layout(height=400)
        st.plotly_chart(fig_bar2, use_container_width=True)

# ============================================================
# 탭3: 처리업체 현황
# ============================================================
with tab3:
    st.markdown("## 🏭 수도권 폐기물 처리업체 현황")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏙️ 서울시 공공소각시설")
        seoul_fac_df = pd.DataFrame(SEOUL_FACILITIES)
        st.metric("총 시설수", f"{len(SEOUL_FACILITIES)}개소")
        st.metric("총 처리용량", f"{seoul_fac_df['용량(톤/일)'].sum():,} 톤/일")
        st.dataframe(seoul_fac_df, use_container_width=True)
    
    with col2:
        st.markdown("### 🏞️ 경기도 공공소각시설")
        gg_fac_df = pd.DataFrame(GYEONGGI_FACILITIES)
        st.metric("총 시설수", f"{len(GYEONGGI_FACILITIES)}개소")
        st.metric("총 처리용량", f"{gg_fac_df['용량(톤/일)'].sum():,} 톤/일")
        st.dataframe(gg_fac_df, use_container_width=True)
    
    st.markdown("---")
    
    all_fac = []
    for f in SEOUL_FACILITIES:
        all_fac.append({'시설명': f['시설명'], '지역': f['구'], '용량(톤/일)': f['용량(톤/일)'], '구분': '서울'})
    for f in GYEONGGI_FACILITIES:
        all_fac.append({'시설명': f['시설명'], '지역': f['시군'], '용량(톤/일)': f['용량(톤/일)'], '구분': '경기'})
    
    all_fac_df = pd.DataFrame(all_fac).sort_values('용량(톤/일)', ascending=True)
    
    fig_fac = px.bar(all_fac_df, y='시설명', x='용량(톤/일)', color='구분',
                    orientation='h', title='수도권 공공소각시설 처리용량',
                    color_discrete_map={'서울': '#E53935', '경기': '#1E88E5'})
    fig_fac.update_layout(height=600)
    st.plotly_chart(fig_fac, use_container_width=True)

# ============================================================
# 탭4: 재무 분석
# ============================================================
with tab4:
    st.markdown("## 💰 재무 분석 (IRR/DCF & 원리금 상환)")
    
    # 기본 파라미터
    st.markdown("### 📊 기본 투자 파라미터")
    col1, col2, col3 = st.columns(3)
    with col1:
        capex = st.number_input("CAPEX (억원)", 100, 2000, 500, 50)
        opex_ratio = st.number_input("OPEX (억원)", 10, 200, 50, 5)
    with col2:
        labor_cost = st.number_input("연간 인건비 (억원)", 1, 50, 10, 1)
        depreciation_years = st.slider("감가상각 기간 (년)", 10, 30, 20, 1)
    with col3:
        project_years = st.slider("사업기간 (년)", 10, 30, 20, 1)
        construction_period = st.slider("건설기간 (년)", 1, 5, 2, 1)
    
    # 에너지 수익화 혼합 비중 설정
    st.markdown("### ⚡ 에너지 수익화 혼합 비중")
    st.caption("바이오가스를 전력, RNG, SAF로 분배하여 판매할 비중을 설정하세요. (합계 100%)")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        power_ratio = st.slider("🔌 전력(SMP+REC) 비중 (%)", 0, 100, 40, 5, key="power_mix")
    with col2:
        rng_ratio = st.slider("🔥 RNG 비중 (%)", 0, 100, 40, 5, key="rng_mix")
    with col3:
        saf_ratio = st.slider("✈️ SAF 비중 (%)", 0, 100, 20, 5, key="saf_mix")
    
    total_mix = power_ratio + rng_ratio + saf_ratio
    
    # 비중 합계 검증 및 정규화
    if total_mix != 100:
        st.warning(f"⚠️ 현재 합계: {total_mix}% (100%가 되어야 합니다)")
        # 자동 정규화
        if total_mix > 0:
            norm_power = power_ratio / total_mix * 100
            norm_rng = rng_ratio / total_mix * 100
            norm_saf = saf_ratio / total_mix * 100
        else:
            norm_power, norm_rng, norm_saf = 33.3, 33.3, 33.4
        st.caption(f"정규화 적용: 전력 {norm_power:.1f}%, RNG {norm_rng:.1f}%, SAF {norm_saf:.1f}%")
    else:
        norm_power, norm_rng, norm_saf = power_ratio, rng_ratio, saf_ratio
        st.success(f"✅ 비중 합계: {total_mix}%")
    
    # 혼합 수익 계산
    mixed_power_revenue = power_revenue_annual * (norm_power / 100)
    mixed_rng_revenue = rng_revenue_annual * (norm_rng / 100)
    mixed_saf_revenue = saf_revenue_krw * (norm_saf / 100)
    mixed_energy_revenue = mixed_power_revenue + mixed_rng_revenue + mixed_saf_revenue
    
    # 혼합 비중 시각화
    col1, col2 = st.columns([1, 2])
    with col1:
        mix_df = pd.DataFrame({
            '수익화 방식': ['전력(SMP+REC)', 'RNG', 'SAF'],
            '비중(%)': [norm_power, norm_rng, norm_saf],
            '연간수익(억원)': [mixed_power_revenue/1e8, mixed_rng_revenue/1e8, mixed_saf_revenue/1e8]
        })
        st.dataframe(mix_df, use_container_width=True, hide_index=True)
        
        st.markdown(f"""
        <div class="revenue-card">
        <h4>💰 혼합 에너지 수익</h4>
        <p style="font-size:1.5rem; text-align:center; margin:0;">
        <b>{mixed_energy_revenue/1e8:.2f} 억원/년</b></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        fig_mix = go.Figure()
        fig_mix.add_trace(go.Bar(
            name='전력(SMP+REC)', x=['에너지 수익'], y=[mixed_power_revenue/1e8],
            marker_color='#2196F3', text=f'{norm_power:.0f}%', textposition='inside'
        ))
        fig_mix.add_trace(go.Bar(
            name='RNG', x=['에너지 수익'], y=[mixed_rng_revenue/1e8],
            marker_color='#4CAF50', text=f'{norm_rng:.0f}%', textposition='inside'
        ))
        fig_mix.add_trace(go.Bar(
            name='SAF', x=['에너지 수익'], y=[mixed_saf_revenue/1e8],
            marker_color='#FF9800', text=f'{norm_saf:.0f}%', textposition='inside'
        ))
        fig_mix.update_layout(barmode='stack', height=300, yaxis_title='수익 (억원/년)',
                             legend=dict(orientation='h', yanchor='bottom', y=1.02))
        st.plotly_chart(fig_mix, use_container_width=True)
    
    # 총 수익 계산 (혼합 에너지 수익 적용)
    total_revenue = tipping_revenue_annual + mixed_energy_revenue + carbon_credit_revenue
    ebitda = total_revenue - total_revenue * (opex_ratio) - labor_cost * 1e8
    monthly_ebitda = ebitda / 12
    
    st.markdown("---")
    
    # Equity / Debt 구조
    st.markdown("### 🏦 자금조달 구조 (Equity / Debt)")
    
    col1, col2 = st.columns(2)
    with col1:
        equity_ratio = st.slider("Equity 비율 (%)", 10, 100, 30, 5)
        debt_ratio = 100 - equity_ratio
        
        equity_amount = capex * equity_ratio / 100
        debt_amount = capex * debt_ratio / 100
        
        st.markdown(f"""
        <div class="metric-card">
        <h4>💼 자금조달 구조</h4>
        <table style="width:100%">
            <tr><td>총 CAPEX</td><td style="text-align:right"><b>{capex:,.0f} 억원</b></td></tr>
            <tr><td>Equity ({equity_ratio}%)</td><td style="text-align:right">{equity_amount:,.1f} 억원</td></tr>
            <tr><td>Debt ({debt_ratio}%)</td><td style="text-align:right">{debt_amount:,.1f} 억원</td></tr>
        </table>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 🔧 대출 조건")
        interest_type = st.radio("금리 유형:", ["고정금리", "변동금리"], horizontal=True)
        
        if interest_type == "고정금리":
            annual_interest_rate = st.slider("연 이자율 (%)", 3.0, 12.0, 5.5, 0.1)
        else:
            base_rate = st.number_input("기준금리 (%)", 2.0, 6.0, 3.5, 0.1)
            spread = st.number_input("가산금리 (%)", 1.0, 5.0, 2.0, 0.1)
            annual_interest_rate = base_rate + spread
            st.caption(f"적용금리: {base_rate}% + {spread}% = **{annual_interest_rate}%**")
        
        loan_term_years = st.slider("대출 기간 (년)", 5, 20, 15, 1)
        grace_period_years = st.slider("거치 기간 (년)", 0, 5, 2, 1)
        repayment_method = st.radio("상환 방식:", ["원리금균등", "원금균등"], horizontal=True)
    
    st.markdown("---")
    
    # 원리금 상환 계산
    st.markdown("### 📅 원리금 상환 분석")
    
    debt_krw = debt_amount * 1e8  # 원 단위
    monthly_rate = annual_interest_rate / 100 / 12
    total_months = loan_term_years * 12
    grace_months = grace_period_years * 12
    repayment_months = total_months - grace_months
    
    # 상환 스케줄 계산
    schedule = []
    remaining_principal = debt_krw
    
    for month in range(1, total_months + 1):
        if month <= grace_months:
            # 거치기간: 이자만 납부
            interest_payment = remaining_principal * monthly_rate
            principal_payment = 0
            monthly_payment = interest_payment
        else:
            # 상환기간
            repay_month = month - grace_months
            if repayment_method == "원리금균등":
                # PMT 공식
                if monthly_rate > 0:
                    monthly_payment = debt_krw * monthly_rate * (1 + monthly_rate) ** repayment_months / ((1 + monthly_rate) ** repayment_months - 1)
                else:
                    monthly_payment = debt_krw / repayment_months
                interest_payment = remaining_principal * monthly_rate
                principal_payment = monthly_payment - interest_payment
            else:  # 원금균등
                principal_payment = debt_krw / repayment_months
                interest_payment = remaining_principal * monthly_rate
                monthly_payment = principal_payment + interest_payment
        
        remaining_principal -= principal_payment
        if remaining_principal < 0:
            remaining_principal = 0
        
        schedule.append({
            '월': month,
            '년차': (month - 1) // 12 + 1,
            '월상환액': monthly_payment,
            '원금상환': principal_payment,
            '이자납부': interest_payment,
            '잔여원금': remaining_principal
        })
    
    schedule_df = pd.DataFrame(schedule)
    
    # 연간 요약
    annual_summary = schedule_df.groupby('년차').agg({
        '월상환액': 'sum',
        '원금상환': 'sum',
        '이자납부': 'sum'
    }).reset_index()
    annual_summary.columns = ['년차', '연간상환액', '원금상환', '이자납부']
    
    # 주요 지표 계산
    first_year_payment = annual_summary[annual_summary['년차'] == 1]['연간상환액'].values[0] if len(annual_summary) > 0 else 0
    max_annual_payment = annual_summary['연간상환액'].max()
    total_interest = schedule_df['이자납부'].sum()
    
    # DSCR 계산 (Debt Service Coverage Ratio)
    dscr = ebitda / max_annual_payment if max_annual_payment > 0 else float('inf')
    monthly_dscr = monthly_ebitda / (max_annual_payment / 12) if max_annual_payment > 0 else float('inf')
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="revenue-card">
        <h4>💵 상환 요약</h4>
        <table style="width:100%">
            <tr><td>대출원금</td><td style="text-align:right">{debt_amount:,.1f} 억원</td></tr>
            <tr><td>총 이자비용</td><td style="text-align:right">{total_interest/1e8:,.1f} 억원</td></tr>
            <tr><td>총 상환액</td><td style="text-align:right">{(debt_krw + total_interest)/1e8:,.1f} 억원</td></tr>
            <tr><td>최대 연상환액</td><td style="text-align:right">{max_annual_payment/1e8:,.1f} 억원</td></tr>
        </table>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
        <h4>📊 현금흐름 분석</h4>
        <table style="width:100%">
            <tr><td>연간 EBITDA</td><td style="text-align:right">{ebitda/1e8:,.1f} 억원</td></tr>
            <tr><td>월간 EBITDA</td><td style="text-align:right">{monthly_ebitda/1e8:,.2f} 억원</td></tr>
            <tr><td>최대 월상환액</td><td style="text-align:right">{max_annual_payment/12/1e8:,.2f} 억원</td></tr>
            <tr><td>월 잉여현금</td><td style="text-align:right">{(monthly_ebitda - max_annual_payment/12)/1e8:,.2f} 억원</td></tr>
        </table>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # DSCR 판단
        if dscr >= 1.5:
            dscr_status = "🟢 매우 안전"
            dscr_color = "#4CAF50"
        elif dscr >= 1.2:
            dscr_status = "🟡 안전"
            dscr_color = "#FF9800"
        elif dscr >= 1.0:
            dscr_status = "🟠 주의"
            dscr_color = "#FF5722"
        else:
            dscr_status = "🔴 위험"
            dscr_color = "#F44336"
        
        st.markdown(f"""
        <div class="highlight-box" style="border-color: {dscr_color};">
        <h4>🛡️ DSCR (원리금상환비율)</h4>
        <p style="font-size:2rem; text-align:center; margin:0;"><b>{dscr:.2f}x</b></p>
        <p style="text-align:center; color:{dscr_color};"><b>{dscr_status}</b></p>
        <small>※ DSCR = EBITDA ÷ 연간원리금<br>
        1.2x 이상: 안전 / 1.5x 이상: 매우 안전</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 상환 스케줄 차트
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 연도별 상환 스케줄")
        fig_repay = go.Figure()
        fig_repay.add_trace(go.Bar(name='원금상환', x=annual_summary['년차'], y=annual_summary['원금상환']/1e8, marker_color='#2196F3'))
        fig_repay.add_trace(go.Bar(name='이자납부', x=annual_summary['년차'], y=annual_summary['이자납부']/1e8, marker_color='#FF9800'))
        fig_repay.add_trace(go.Scatter(name='EBITDA', x=annual_summary['년차'], y=[ebitda/1e8]*len(annual_summary), 
                                       mode='lines', line=dict(color='#4CAF50', width=3, dash='dash')))
        fig_repay.update_layout(barmode='stack', height=400, yaxis_title='금액 (억원)', xaxis_title='년차',
                               legend=dict(orientation='h', yanchor='bottom', y=1.02))
        st.plotly_chart(fig_repay, use_container_width=True)
    
    with col2:
        st.markdown("#### 📉 잔여원금 추이")
        monthly_balance = schedule_df[schedule_df['월'] % 12 == 0].copy()
        monthly_balance['년차'] = monthly_balance['월'] // 12
        fig_balance = px.area(monthly_balance, x='년차', y='잔여원금', 
                             title='', labels={'잔여원금': '잔여원금 (원)', '년차': '년차'})
        fig_balance.update_traces(fill='tozeroy', line_color='#E53935')
        fig_balance.update_layout(height=400)
        fig_balance.update_yaxes(tickformat=',.0f')
        st.plotly_chart(fig_balance, use_container_width=True)
    
    st.markdown("---")
    
    # 상세 스케줄 테이블
    with st.expander("📋 월별 상환 스케줄 상세"):
        display_schedule = schedule_df.copy()
        display_schedule['월상환액'] = display_schedule['월상환액'].apply(lambda x: f"{x/1e4:,.0f} 만원")
        display_schedule['원금상환'] = display_schedule['원금상환'].apply(lambda x: f"{x/1e4:,.0f} 만원")
        display_schedule['이자납부'] = display_schedule['이자납부'].apply(lambda x: f"{x/1e4:,.0f} 만원")
        display_schedule['잔여원금'] = display_schedule['잔여원금'].apply(lambda x: f"{x/1e8:,.2f} 억원")
        st.dataframe(display_schedule, use_container_width=True, height=400)
    
    st.markdown("---")
    
    # 기존 IRR/NPV 계산
    st.markdown("### 📊 수익성 지표")
    
    def calculate_irr(capex_val, annual_cf, years):
        for irr in np.arange(0.01, 0.50, 0.01):
            npv = -capex_val
            for y in range(1, years + 1):
                npv += annual_cf / ((1 + irr) ** y)
            if npv <= 0:
                return irr - 0.01
        return 0.50
    
    # Equity IRR 계산 (대출 원리금 상환 후)
    equity_krw = equity_amount * 1e8
    annual_debt_service = max_annual_payment
    equity_cashflow = ebitda - annual_debt_service
    
    project_irr = calculate_irr(capex * 1e8, ebitda, project_years)
    equity_irr = calculate_irr(equity_krw, equity_cashflow, project_years) if equity_cashflow > 0 else 0
    
    payback_years = (capex * 1e8) / ebitda if ebitda > 0 else float('inf')
    equity_payback = equity_krw / equity_cashflow if equity_cashflow > 0 else float('inf')
    
    npv = -capex * 1e8 + sum([ebitda / ((1 + 0.08) ** y) for y in range(1, project_years + 1)])
    equity_npv = -equity_krw + sum([equity_cashflow / ((1 + 0.10) ** y) for y in range(1, project_years + 1)])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="highlight-box">
        <h4>🏢 Project 기준</h4>
        <table style="width:100%">
            <tr><td>총 매출</td><td style="text-align:right"><b>{total_revenue/1e8:.1f} 억원/년</b></td></tr>
            <tr><td>EBITDA</td><td style="text-align:right"><b>{ebitda/1e8:.1f} 억원/년</b></td></tr>
            <tr><td>Project IRR</td><td style="text-align:right"><b>{project_irr*100:.1f}%</b></td></tr>
            <tr><td>NPV (8%)</td><td style="text-align:right"><b>{npv/1e8:.1f} 억원</b></td></tr>
            <tr><td>투자회수기간</td><td style="text-align:right"><b>{payback_years:.1f} 년</b></td></tr>
        </table>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="revenue-card">
        <h4>💰 Equity 투자자 기준</h4>
        <table style="width:100%">
            <tr><td>Equity 투자금</td><td style="text-align:right"><b>{equity_amount:.1f} 억원</b></td></tr>
            <tr><td>연간 배당가능액</td><td style="text-align:right"><b>{equity_cashflow/1e8:.1f} 억원</b></td></tr>
            <tr><td>Equity IRR</td><td style="text-align:right"><b>{equity_irr*100:.1f}%</b></td></tr>
            <tr><td>NPV (10%)</td><td style="text-align:right"><b>{equity_npv/1e8:.1f} 억원</b></td></tr>
            <tr><td>Equity 회수기간</td><td style="text-align:right"><b>{equity_payback:.1f} 년</b></td></tr>
        </table>
        </div>
        """, unsafe_allow_html=True)
    
    # 레버리지 효과
    leverage_effect = equity_irr - project_irr if equity_irr > 0 else 0
    if leverage_effect > 0:
        st.success(f"✅ 레버리지 효과: Equity IRR이 Project IRR 대비 **+{leverage_effect*100:.1f}%p** 증가")
    elif equity_cashflow <= 0:
        st.error("❌ 원리금 상환 후 배당가능 현금흐름이 없습니다. 자금구조 재검토가 필요합니다.")

# ============================================================
# 탭5: 환산 테이블
# ============================================================
with tab5:
    st.markdown("## 📐 에너지 단위 환산 테이블")
    
    st.markdown("### 바이오가스·메탄·SAF")
    conversion_table = pd.DataFrame({
        '구분': ['바이오가스 에너지', '메탄 에너지(부피)', '메탄 에너지(질량)', '메탄 밀도', 'SAF 밀도', 'SAF 발열량', '탄소 감축계수'],
        '환산식': ['1 Nm³ ≈ 6 kWh (21.6 MJ)', '1 Nm³ CH₄ ≈ 10 kWh (35.8 MJ)', '1 kg CH₄ ≈ 50 MJ',
                 '1 Nm³ CH₄ ≈ 0.717 kg', '0.8 kg/L (127 kg/bbl)', '1 kg ≈ 43 MJ', '폐기물 1톤 → 0.18 tCO₂'],
        '비고': ['CH4 60% 기준 LHV', 'LHV 기준', 'LHV', '0℃, 1 atm', '표준 배럴 159L', '제트연료 LHV', '환경부 기준']
    })
    st.dataframe(conversion_table, use_container_width=True)

# ============================================================
# 탭6: 데이터 다운로드
# ============================================================
with tab6:
    st.markdown("## 📥 데이터 다운로드")
    
    st.markdown("### 1️⃣ 서울시 음식물쓰레기 발생량")
    seoul_download_df = pd.DataFrame([
        {'자치구': k, '발생량(톤/일)': v['발생량'], '사료화': v.get('사료화', 0), 
         '퇴비화': v.get('퇴비화', 0), '기타': v.get('기타', 0)}
        for k, v in SEOUL_FOOD_WASTE_DATA.items()
    ])
    st.dataframe(seoul_download_df, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        csv_seoul = seoul_download_df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button("📥 CSV 다운로드", csv_seoul, "seoul_food_waste.csv", "text/csv")
    with col2:
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            seoul_download_df.to_excel(writer, index=False)
        st.download_button("📥 Excel 다운로드", buffer.getvalue(), "seoul_food_waste.xlsx")
    
    st.markdown("---")
    
    st.markdown("### 2️⃣ 경기도 음식물쓰레기 발생량")
    gg_download_df = pd.DataFrame([
        {'시군': k, '발생량(톤/일)': v['발생량']}
        for k, v in GYEONGGI_FOOD_WASTE_DATA.items()
    ])
    st.dataframe(gg_download_df, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        csv_gg = gg_download_df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button("📥 CSV 다운로드", csv_gg, "gyeonggi_food_waste.csv", "text/csv", key="gg_csv")
    with col2:
        buffer2 = BytesIO()
        with pd.ExcelWriter(buffer2, engine='xlsxwriter') as writer:
            gg_download_df.to_excel(writer, index=False)
        st.download_button("📥 Excel 다운로드", buffer2.getvalue(), "gyeonggi_food_waste.xlsx", key="gg_xlsx")
    
    st.markdown("---")
    
    st.markdown("### 3️⃣ 시뮬레이션 결과")
    sim_result = pd.DataFrame({
        '항목': ['일일 처리량', '연간 처리량', '연간 바이오가스', '연간 전력생산', '연간 SAF 생산',
               '티핑피 수익', '전력 수익', 'RNG 수익', 'SAF 수익', '탄소배출권 수익'],
        '값': [f'{daily_capacity:,.0f} 톤/일', f'{annual_capacity:,.0f} 톤/년',
              f'{biogas_annual/1e6:.2f} 백만Nm³', f'{power_annual_gwh:.2f} GWh', f'{saf_mass_ton:.1f} 톤',
              f'{tipping_revenue_annual/1e8:.2f} 억원', f'{power_revenue_annual/1e8:.2f} 억원',
              f'{rng_revenue_annual/1e8:.2f} 억원', f'{saf_revenue_krw/1e8:.2f} 억원',
              f'{carbon_credit_revenue/1e8:.2f} 억원']
    })
    st.dataframe(sim_result, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        csv_sim = sim_result.to_csv(index=False, encoding='utf-8-sig')
        st.download_button("📥 CSV 다운로드", csv_sim, "simulation_result.csv", "text/csv", key="sim_csv")
    with col2:
        buffer3 = BytesIO()
        with pd.ExcelWriter(buffer3, engine='xlsxwriter') as writer:
            sim_result.to_excel(writer, index=False)
        st.download_button("📥 Excel 다운로드", buffer3.getvalue(), "simulation_result.xlsx", key="sim_xlsx")

# ============================================================
# 푸터
# ============================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>⚡ 바이오가스 사업성 종합 분석 대시보드 v3.0</p>
    <p>데이터 기준: 2023년 | 출처: 환경부 폐기물통계, 바이오가스 생산이용 활성화 전략</p>
</div>
""", unsafe_allow_html=True)
