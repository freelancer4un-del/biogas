"""
바이오가스 사업성 종합 분석 대시보드
Biogas Feasibility Comprehensive Analysis Dashboard
Version 2.0 - with SAF, Carbon Credits, IRR/DCF Analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
        background: linear-gradient(135deg, #BBDEFB 100%,  #BBDEFB 100%);
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
    .cost-card {
        background: linear-gradient(135deg, #FFCDD2 100%, #FFCDD2 100%);
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 5px solid #D32F2F;
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
    .conversion-table {
        background-color: #F5F5F5;
        padding: 1rem;
        border-radius: 8px;
        font-size: 0.9rem;
        color: #333333;
    }
    .saf-box {
        background: linear-gradient(135deg, #B3E5FC 100%, #B3E5FC 100%);
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 5px solid #0288D1;
        margin: 0.5rem 0;
    }
    .carbon-box {
        background: linear-gradient(135deg, #E1BEE7 100%, #E1BEE7 100%);
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 5px solid #7B1FA2;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 상수 정의 (에너지 환산 테이블 기반)
# ============================================================
# 기본 에너지 단위
KWH_TO_MJ = 3.6
MJ_TO_KWH = 0.27778

# 바이오가스/메탄
BIOGAS_ENERGY_KWH_NM3 = 6  # CH4 60% 기준 LHV
BIOGAS_ENERGY_MJ_NM3 = 21.6
METHANE_ENERGY_KWH_NM3 = 10  # 순수 메탄
METHANE_ENERGY_MJ_NM3 = 35.8
METHANE_ENERGY_MJ_KG = 50  # LHV
METHANE_DENSITY_KG_NM3 = 0.717

# 수소
H2_ENERGY_MJ_KG = 120  # LHV
H2_ENERGY_MJ_NM3 = 10.8
H2_ENERGY_KWH_NM3 = 3.0
H2_DENSITY_KG_NM3 = 0.0899
CH4_TO_H2_THEORETICAL = 0.36  # kg H2 per Nm³ CH4

# SAF
SAF_DENSITY_KG_L = 0.8
BARREL_VOLUME_L = 159
SAF_MASS_PER_BARREL_KG = 127.2
SAF_ENERGY_MJ_KG = 43
SAF_ENERGY_MJ_BBL = 5470

# 탄소배출권
CO2_REDUCTION_PER_TON_WASTE = 0.18  # tCO2/톤 폐기물

# 바이오가스 발생량 (Nm³/톤)
BIOGAS_YIELD_FOOD_WASTE = 130  # 음식물쓰레기
BIOGAS_YIELD_LIVESTOCK = 20   # 축분

# ============================================================
# 헤더
# ============================================================
st.markdown('<div class="main-header">⚡ 바이오가스 사업성 종합 분석 대시보드</div>', unsafe_allow_html=True)
st.markdown("##### Biogas Feasibility Analysis with SAF, Carbon Credits & Financial Modeling")

# ============================================================
# 사이드바 - 입력 파라미터
# ============================================================
with st.sidebar:
    st.markdown("## 📊 사업 파라미터 설정")
    
    st.markdown("### 🗑️ 폐기물 처리량")
    daily_capacity = st.slider("일일 처리량 (톤/일)", 50, 1000, 300, 10)
    
    st.markdown("### 📊 음식물 vs 축분 비율")
    food_waste_ratio = st.slider("음식물쓰레기 비율 (%)", 0, 100, 50, 5)
    livestock_ratio = 100 - food_waste_ratio
    
    st.markdown(f"""
    <div class="metric-card">
    <b>음식물쓰레기:</b> {daily_capacity * food_waste_ratio / 100:.0f} 톤/일<br>
    <b>축분:</b> {daily_capacity * livestock_ratio / 100:.0f} 톤/일
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 💰 티핑피 (처리 수수료)")
    tipping_fee_food = st.number_input("음식물 티핑피 (원/톤)", 50000, 200000, 140000, 10000)
    tipping_fee_livestock = st.number_input("축분 티핑피 (원/톤)", 10000, 100000, 30000, 5000)
    
    st.markdown("---")
    st.markdown("### ⚙️ 운영 파라미터")
    operating_days = st.slider("연간 가동일수", 200, 365, 330, 5)
    utilization_rate = st.slider("가동률 (%)", 50, 100, 80, 5)
    methane_content = st.slider("메탄 함량 (%)", 50, 70, 60, 1)
    power_gen_efficiency = st.slider("발전 효율 (%)", 20, 45, 30, 1)
    
    st.markdown("---")
    st.markdown("### 💵 판매 가격")
    smp_price = st.number_input("SMP 가격 (원/kWh)", 50, 200, 100, 5)
    rec_price = st.number_input("REC 가격 (원/kWh)", 30, 150, 70, 5)
    rng_price = st.number_input("바이오가스 RNG (원/Nm³)", 500, 2000, 900, 50)
    saf_price_usd = st.number_input("SAF 가격 (USD/톤)", 1500, 5000, 2700, 100)
    exchange_rate = st.number_input("환율 (원/USD)", 1200, 1500, 1400, 10)
    carbon_credit_price = st.number_input("탄소배출권 가격 (원/tCO2)", 5000, 20000, 10000, 500)

# ============================================================
# 계산 로직
# ============================================================

# 1. 폐기물 처리량 계산
food_waste_daily = daily_capacity * food_waste_ratio / 100
livestock_daily = daily_capacity * livestock_ratio / 100
annual_capacity = daily_capacity * operating_days
food_waste_annual = food_waste_daily * operating_days
livestock_annual = livestock_daily * operating_days

# 2. 티핑피 수익 계산
tipping_revenue_food_daily = food_waste_daily * tipping_fee_food
tipping_revenue_livestock_daily = livestock_daily * tipping_fee_livestock
tipping_revenue_daily = tipping_revenue_food_daily + tipping_revenue_livestock_daily
tipping_revenue_annual = tipping_revenue_daily * operating_days

# 3. 바이오가스 발생량 계산
biogas_food_daily = food_waste_daily * BIOGAS_YIELD_FOOD_WASTE * (utilization_rate / 100)
biogas_livestock_daily = livestock_daily * BIOGAS_YIELD_LIVESTOCK * (utilization_rate / 100)
biogas_daily = biogas_food_daily + biogas_livestock_daily
biogas_annual = biogas_daily * operating_days

# 4. 메탄 생산량
methane_daily = biogas_daily * (methane_content / 100)
methane_annual = methane_daily * operating_days
methane_mass_annual = methane_annual * METHANE_DENSITY_KG_NM3  # kg

# 5. 에너지 생산량 (전력)
energy_daily_mj = biogas_daily * BIOGAS_ENERGY_MJ_NM3
power_daily_kwh = biogas_daily * BIOGAS_ENERGY_KWH_NM3 * (power_gen_efficiency / 100)
power_annual_kwh = power_daily_kwh * operating_days
power_annual_mwh = power_annual_kwh / 1000
power_annual_gwh = power_annual_kwh / 1000000

# 6. 전력 판매 수익 (SMP + REC)
power_revenue_daily = power_daily_kwh * (smp_price + rec_price)
power_revenue_annual = power_annual_kwh * (smp_price + rec_price)

# 7. RNG 판매 수익 (정제효율 90% 가정)
rng_purification_rate = 0.90
rng_daily = methane_daily * rng_purification_rate
rng_annual = rng_daily * operating_days
rng_revenue_annual = rng_annual * rng_price

# 8. SAF 생산량 및 수익
# GTL 효율 55%, SAF cut 비율 25%
gtl_efficiency = 0.55
saf_cut_ratio = 0.25
methane_energy_annual_mj = methane_mass_annual * METHANE_ENERGY_MJ_KG
ft_liquid_energy_mj = methane_energy_annual_mj * gtl_efficiency
saf_energy_mj = ft_liquid_energy_mj * saf_cut_ratio
saf_mass_kg = saf_energy_mj / SAF_ENERGY_MJ_KG
saf_mass_ton = saf_mass_kg / 1000
saf_barrels = saf_mass_kg / SAF_MASS_PER_BARREL_KG
saf_revenue_usd = saf_mass_ton * saf_price_usd
saf_revenue_krw = saf_revenue_usd * exchange_rate

# 9. 탄소배출권 수익
carbon_reduction_annual = annual_capacity * CO2_REDUCTION_PER_TON_WASTE
carbon_credit_revenue = carbon_reduction_annual * carbon_credit_price

# ============================================================
# 탭 구성
# ============================================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 종합 현황",
    "⚡ 전력 판매",
    "🔥 RNG 판매", 
    "✈️ SAF 생산",
    "🌱 탄소배출권",
    "💰 재무 분석",
    "📐 환산 테이블"
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
    
    # 수익원별 비교
    st.markdown("### 💰 수익원별 연간 수익 비교")
    
    col1, col2 = st.columns(2)
    
    with col1:
        revenue_comparison = pd.DataFrame({
            '수익원': ['티핑피 수익', '전력 판매 (SMP+REC)', 'RNG 판매', 'SAF 판매', '탄소배출권'],
            '연간 수익(억원)': [
                tipping_revenue_annual / 100000000,
                power_revenue_annual / 100000000,
                rng_revenue_annual / 100000000,
                saf_revenue_krw / 100000000,
                carbon_credit_revenue / 100000000
            ]
        })
        
        fig1 = px.bar(revenue_comparison, x='수익원', y='연간 수익(억원)',
                     title='수익원별 연간 수익 비교',
                     color='수익원',
                     color_discrete_sequence=px.colors.qualitative.Set2)
        fig1.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # 에너지 수익화 방식별 비교 (전력 vs RNG vs SAF)
        energy_options = pd.DataFrame({
            '수익화 방식': ['전력 (SMP+REC)', 'RNG 판매', 'SAF 판매'],
            '연간 수익(억원)': [
                power_revenue_annual / 100000000,
                rng_revenue_annual / 100000000,
                saf_revenue_krw / 100000000
            ]
        })
        
        fig2 = px.pie(energy_options, values='연간 수익(억원)', names='수익화 방식',
                     title='에너지 수익화 방식 비교',
                     color_discrete_sequence=['#4CAF50', '#2196F3', '#FF9800'])
        fig2.update_traces(textposition='inside', textinfo='percent+label+value')
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("---")
    
    # 핵심 지표 요약
    st.markdown("### 📋 핵심 지표 요약")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="revenue-card">
        <h4>💵 티핑피 수익</h4>
        <table style="width:100%">
            <tr><td>음식물 (일)</td><td style="text-align:right">{tipping_revenue_food_daily/10000:,.0f} 만원</td></tr>
            <tr><td>축분 (일)</td><td style="text-align:right">{tipping_revenue_livestock_daily/10000:,.0f} 만원</td></tr>
            <tr><td><b>합계 (일)</b></td><td style="text-align:right"><b>{tipping_revenue_daily/10000:,.0f} 만원</b></td></tr>
            <tr><td><b>연간 합계</b></td><td style="text-align:right"><b>{tipping_revenue_annual/100000000:.1f} 억원</b></td></tr>
        </table>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
        <h4>⚡ 바이오가스 생산</h4>
        <table style="width:100%">
            <tr><td>음식물 (일)</td><td style="text-align:right">{biogas_food_daily:,.0f} Nm³</td></tr>
            <tr><td>축분 (일)</td><td style="text-align:right">{biogas_livestock_daily:,.0f} Nm³</td></tr>
            <tr><td><b>합계 (일)</b></td><td style="text-align:right"><b>{biogas_daily:,.0f} Nm³</b></td></tr>
            <tr><td><b>연간 합계</b></td><td style="text-align:right"><b>{biogas_annual/1000000:.2f} 백만Nm³</b></td></tr>
        </table>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="carbon-box">
        <h4>🌱 탄소 감축</h4>
        <table style="width:100%">
            <tr><td>감축계수</td><td style="text-align:right">{CO2_REDUCTION_PER_TON_WASTE} tCO₂/톤</td></tr>
            <tr><td>연간 처리량</td><td style="text-align:right">{annual_capacity:,.0f} 톤</td></tr>
            <tr><td><b>연간 감축량</b></td><td style="text-align:right"><b>{carbon_reduction_annual:,.0f} tCO₂</b></td></tr>
            <tr><td><b>배출권 수익</b></td><td style="text-align:right"><b>{carbon_credit_revenue/100000000:.2f} 억원</b></td></tr>
        </table>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# 탭2: 전력 판매
# ============================================================
with tab2:
    st.markdown("## ⚡ 전력 판매 (SMP + REC) 분석")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("일일 발전량", f"{power_daily_kwh:,.0f} kWh")
    with col2:
        st.metric("연간 발전량", f"{power_annual_gwh:.2f} GWh")
    with col3:
        st.metric("SMP 수익", f"{power_annual_kwh * smp_price / 100000000:.2f} 억원/년")
    with col4:
        st.metric("REC 수익", f"{power_annual_kwh * rec_price / 100000000:.2f} 억원/년")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 발전량 계산 과정")
        st.markdown(f"""
        <div class="metric-card">
        <h4>Step 1: 바이오가스 에너지</h4>
        <p>• 바이오가스: {biogas_daily:,.0f} Nm³/일</p>
        <p>• 에너지 밀도: {BIOGAS_ENERGY_KWH_NM3} kWh/Nm³ (CH₄ 60% 기준)</p>
        <p>• 총 에너지: {biogas_daily * BIOGAS_ENERGY_KWH_NM3:,.0f} kWh/일</p>
        </div>
        
        <div class="metric-card">
        <h4>Step 2: 발전량</h4>
        <p>• 발전 효율: {power_gen_efficiency}%</p>
        <p>• 일일 발전량: {power_daily_kwh:,.0f} kWh</p>
        <p>• 연간 발전량: {power_annual_kwh:,.0f} kWh = {power_annual_gwh:.2f} GWh</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 💰 수익 계산")
        st.markdown(f"""
        <div class="revenue-card">
        <h4>SMP (계통한계가격)</h4>
        <p>• 단가: {smp_price} 원/kWh</p>
        <p>• 일일 수익: {power_daily_kwh * smp_price:,.0f} 원</p>
        <p>• <b>연간 수익: {power_annual_kwh * smp_price / 100000000:.2f} 억원</b></p>
        </div>
        
        <div class="revenue-card">
        <h4>REC (신재생에너지 공급인증서)</h4>
        <p>• 단가: {rec_price} 원/kWh</p>
        <p>• 일일 수익: {power_daily_kwh * rec_price:,.0f} 원</p>
        <p>• <b>연간 수익: {power_annual_kwh * rec_price / 100000000:.2f} 억원</b></p>
        </div>
        
        <div class="highlight-box">
        <h4>📊 전력 판매 총 수익</h4>
        <p style="font-size:1.3rem"><b>연간: {power_revenue_annual / 100000000:.2f} 억원</b></p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # SMP/REC 가격 민감도 분석
    st.markdown("### 📊 SMP/REC 가격 민감도 분석")
    
    smp_range = np.arange(70, 151, 10)
    rec_range = np.arange(40, 121, 10)
    
    sensitivity_data = []
    for smp in smp_range:
        for rec in rec_range:
            revenue = power_annual_kwh * (smp + rec) / 100000000
            sensitivity_data.append({'SMP': smp, 'REC': rec, '연간수익(억원)': revenue})
    
    sensitivity_df = pd.DataFrame(sensitivity_data)
    pivot_df = sensitivity_df.pivot(index='REC', columns='SMP', values='연간수익(억원)')
    
    fig3 = px.imshow(pivot_df, 
                    labels=dict(x="SMP (원/kWh)", y="REC (원/kWh)", color="연간수익(억원)"),
                    title="SMP/REC 가격별 연간 수익 (억원)",
                    color_continuous_scale='Greens')
    fig3.update_layout(height=400)
    st.plotly_chart(fig3, use_container_width=True)

# ============================================================
# 탭3: RNG 판매
# ============================================================
with tab3:
    st.markdown("## 🔥 바이오가스 RNG 판매 분석")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("일일 RNG 생산", f"{rng_daily:,.0f} Nm³")
    with col2:
        st.metric("연간 RNG 생산", f"{rng_annual/1000000:.2f} 백만Nm³")
    with col3:
        st.metric("RNG 판매단가", f"{rng_price:,} 원/Nm³")
    with col4:
        st.metric("연간 RNG 수익", f"{rng_revenue_annual/100000000:.1f} 억원")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 RNG 생산 과정")
        st.markdown(f"""
        <div class="metric-card">
        <h4>Step 1: 바이오가스 → 메탄</h4>
        <p>• 바이오가스: {biogas_daily:,.0f} Nm³/일</p>
        <p>• 메탄 함량: {methane_content}%</p>
        <p>• 메탄량: {methane_daily:,.0f} Nm³/일</p>
        </div>
        
        <div class="metric-card">
        <h4>Step 2: 정제 (Upgrading)</h4>
        <p>• 정제 효율: {rng_purification_rate*100:.0f}%</p>
        <p>• 일일 RNG: {rng_daily:,.0f} Nm³</p>
        <p>• 연간 RNG: {rng_annual:,.0f} Nm³ = {rng_annual/1000000:.2f} 백만Nm³</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 💰 RNG 판매 수익")
        st.markdown(f"""
        <div class="revenue-card">
        <h4>판매 옵션</h4>
        <table style="width:100%">
            <tr><td>도시가스 공급</td><td style="text-align:right">~900 원/Nm³</td></tr>
            <tr><td>차량용 CNG</td><td style="text-align:right">~1,500 원/Nm³</td></tr>
        </table>
        </div>
        
        <div class="highlight-box">
        <h4>📊 RNG 판매 수익 (현재 설정: {rng_price:,}원/Nm³)</h4>
        <p>• 일일 수익: {rng_daily * rng_price:,.0f} 원 = {rng_daily * rng_price / 10000:,.0f} 만원</p>
        <p style="font-size:1.3rem"><b>연간 수익: {rng_revenue_annual / 100000000:.2f} 억원</b></p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 전력 vs RNG 비교
    st.markdown("### ⚖️ 전력 판매 vs RNG 판매 비교")
    
    col1, col2 = st.columns(2)
    
    with col1:
        comparison_df = pd.DataFrame({
            '항목': ['연간 수익(억원)', '기술 복잡도', '초기 투자', '시장 안정성'],
            '전력 판매': [power_revenue_annual/100000000, '낮음', '중간', '높음 (RPS)'],
            'RNG 판매': [rng_revenue_annual/100000000, '높음', '높음', '중간']
        })
        st.dataframe(comparison_df, use_container_width=True)
    
    with col2:
        diff = rng_revenue_annual - power_revenue_annual
        if diff > 0:
            st.success(f"✅ RNG 판매가 {diff/100000000:.2f} 억원 더 유리합니다!")
        else:
            st.info(f"ℹ️ 전력 판매가 {-diff/100000000:.2f} 억원 더 유리합니다.")

# ============================================================
# 탭4: SAF 생산
# ============================================================
with tab4:
    st.markdown("## ✈️ SAF (지속가능 항공유) 생산 분석")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("연간 SAF 생산", f"{saf_mass_ton:,.1f} 톤")
    with col2:
        st.metric("SAF 배럴", f"{saf_barrels:,.0f} bbl")
    with col3:
        st.metric("SAF 가격", f"${saf_price_usd:,}/톤")
    with col4:
        st.metric("연간 SAF 수익", f"{saf_revenue_krw/100000000:.1f} 억원")
    
    st.markdown("---")
    
    # SAF 시장 현황
    st.markdown("### 🌍 SAF 시장 현황")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="saf-box">
        <h4>🇰🇷 국내 항공유 시장</h4>
        <ul>
            <li><b>연간 소비량:</b> 약 500만 톤</li>
            <li><b>2027 SAF 의무비율:</b> 1%</li>
            <li><b>2027 SAF 수요:</b> ~5만 톤</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="saf-box">
        <h4>💰 SAF 시장 규모 (2027)</h4>
        <ul>
            <li><b>수요:</b> 50,000 톤</li>
            <li><b>가격:</b> $2,700/톤</li>
            <li><b>시장 규모:</b> $135M</li>
            <li><b>원화 환산:</b> 약 1,890억원</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="highlight-box">
        <h4>📊 본 사업 SAF 시장 점유율</h4>
        <ul>
            <li><b>연간 생산량:</b> {saf_mass_ton:,.1f} 톤</li>
            <li><b>시장 점유율:</b> {saf_mass_ton/50000*100:.2f}%</li>
            <li><b>연간 수익:</b> {saf_revenue_krw/100000000:.1f} 억원</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # SAF 생산 과정
    st.markdown("### 🔄 Biogas → GTL → SAF 전환 과정")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
        <h4>① 바이오가스 에너지</h4>
        <p>• 연간 메탄: {methane_annual:,.0f} Nm³</p>
        <p>• 메탄 질량: {methane_mass_annual:,.0f} kg = {methane_mass_annual/1000:.1f} 톤</p>
        <p>• 메탄 에너지: {methane_energy_annual_mj/1000000:.1f} TJ (= {methane_mass_annual} kg × 50 MJ/kg)</p>
        </div>
        
        <div class="metric-card">
        <h4>② GTL 전환</h4>
        <p>• GTL 효율 (η_GTL): {gtl_efficiency*100:.0f}%</p>
        <p>• FT 액체 에너지: {ft_liquid_energy_mj/1000000:.1f} TJ</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
        <h4>③ SAF Cut</h4>
        <p>• SAF 비율 (Y_SAF): {saf_cut_ratio*100:.0f}%</p>
        <p>• SAF 에너지: {saf_energy_mj/1000000:.2f} TJ</p>
        </div>
        
        <div class="revenue-card">
        <h4>④ SAF 생산량 & 수익</h4>
        <p>• SAF 질량: {saf_mass_kg:,.0f} kg = {saf_mass_ton:.1f} 톤</p>
        <p>• SAF 배럴: {saf_barrels:,.0f} bbl</p>
        <p>• <b>연간 수익: ${saf_revenue_usd:,.0f} = {saf_revenue_krw/100000000:.1f} 억원</b></p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # SAF 가격 민감도
    st.markdown("### 📊 SAF 가격 및 생산량 민감도 분석")
    
    saf_prices = [2000, 2500, 2700, 3000, 3500]
    production_rates = [0.8, 0.9, 1.0, 1.1, 1.2]
    
    sensitivity_saf = []
    for price in saf_prices:
        for rate in production_rates:
            revenue = saf_mass_ton * rate * price * exchange_rate / 100000000
            sensitivity_saf.append({
                'SAF가격($/톤)': price,
                '생산량 배수': rate,
                '연간수익(억원)': revenue
            })
    
    sens_df = pd.DataFrame(sensitivity_saf)
    
    fig4 = px.line(sens_df, x='SAF가격($/톤)', y='연간수익(억원)', 
                   color='생산량 배수', markers=True,
                   title='SAF 가격 및 생산량별 연간 수익')
    fig4.update_layout(height=400)
    st.plotly_chart(fig4, use_container_width=True)

# ============================================================
# 탭5: 탄소배출권
# ============================================================
with tab5:
    st.markdown("## 🌱 탄소배출권 수익 분석")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("연간 폐기물 처리량", f"{annual_capacity:,.0f} 톤")
    with col2:
        st.metric("CO₂ 감축량", f"{carbon_reduction_annual:,.0f} tCO₂")
    with col3:
        st.metric("배출권 단가", f"{carbon_credit_price:,} 원/tCO₂")
    with col4:
        st.metric("연간 배출권 수익", f"{carbon_credit_revenue/100000000:.2f} 억원")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 산출 근거")
        st.markdown(f"""
        <div class="carbon-box">
        <h4>환경부 기준 (2024.01.02)</h4>
        <p><b>「바이오가스 생산이용 활성화 전략」</b></p>
        <ul>
            <li>유기성 폐자원 557만톤 처리 시</li>
            <li>온실가스 100만톤(CO₂ eq) 감축</li>
            <li><b>감축계수: 1,000,000 ÷ 5,570,000 ≈ 0.18 tCO₂/톤</b></li>
        </ul>
        </div>
        
        <div class="metric-card">
        <h4>K-ETS (배출권거래제)</h4>
        <ul>
            <li><b>1 KOC = 1 tCO₂-eq</b></li>
            <li>거래가격: 9,000 ~ 12,000원/KOC</li>
            <li>현재 설정: {carbon_credit_price:,}원/tCO₂</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 💰 수익 계산")
        st.markdown(f"""
        <div class="revenue-card">
        <h4>연간 탄소 감축량</h4>
        <p>• 폐기물 처리량: {annual_capacity:,.0f} 톤/년</p>
        <p>• 감축계수: {CO2_REDUCTION_PER_TON_WASTE} tCO₂/톤</p>
        <p>• <b>연간 감축량: {carbon_reduction_annual:,.0f} tCO₂</b></p>
        </div>
        
        <div class="highlight-box">
        <h4>📊 탄소배출권 수익</h4>
        <p>• 감축량 × 단가 = {carbon_reduction_annual:,.0f} × {carbon_credit_price:,}원</p>
        <p style="font-size:1.3rem"><b>= {carbon_credit_revenue:,.0f} 원</b></p>
        <p style="font-size:1.3rem"><b>= {carbon_credit_revenue/100000000:.2f} 억원/년</b></p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 배출권 가격 시나리오
    st.markdown("### 📈 배출권 가격 시나리오별 수익")
    
    carbon_prices = [5000, 7000, 10000, 12000, 15000, 20000]
    carbon_revenues = [carbon_reduction_annual * p / 100000000 for p in carbon_prices]
    
    carbon_scenario = pd.DataFrame({
        '배출권 가격 (원/tCO₂)': carbon_prices,
        '연간 수익 (억원)': carbon_revenues
    })
    
    fig5 = px.bar(carbon_scenario, x='배출권 가격 (원/tCO₂)', y='연간 수익 (억원)',
                 title='배출권 가격별 연간 수익',
                 color='연간 수익 (억원)',
                 color_continuous_scale='Purples')
    fig5.add_hline(y=carbon_credit_revenue/100000000, line_dash="dash", 
                   annotation_text=f"현재 설정: {carbon_credit_revenue/100000000:.2f}억원")
    fig5.update_layout(height=400)
    st.plotly_chart(fig5, use_container_width=True)

# ============================================================
# 탭6: 재무 분석
# ============================================================
with tab6:
    st.markdown("## 💰 재무 분석 (IRR/DCF)")
    
    st.markdown("### 📥 비용 파라미터 설정")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        capex = st.number_input("CAPEX (억원)", 100, 2000, 500, 50)
        opex_ratio = st.slider("OPEX (매출 대비 %)", 10, 50, 25, 1)
    
    with col2:
        labor_cost = st.number_input("연간 인건비 (억원)", 1, 50, 10, 1)
        depreciation_years = st.slider("감가상각 기간 (년)", 10, 30, 20, 1)
    
    with col3:
        financing_rate = st.slider("금융비용 (이자율 %)", 2.0, 10.0, 5.0, 0.5)
        project_years = st.slider("사업기간 (년)", 10, 30, 20, 1)
    
    st.markdown("---")
    
    # 수익 선택
    st.markdown("### ⚡ 에너지 수익화 방식 선택")
    
    energy_option = st.radio(
        "수익화 방식을 선택하세요:",
        ["전력 판매 (SMP + REC)", "RNG 판매", "SAF 판매"],
        horizontal=True
    )
    
    if energy_option == "전력 판매 (SMP + REC)":
        energy_revenue = power_revenue_annual
    elif energy_option == "RNG 판매":
        energy_revenue = rng_revenue_annual
    else:
        energy_revenue = saf_revenue_krw
    
    # 총 수익 계산
    total_revenue = tipping_revenue_annual + energy_revenue + carbon_credit_revenue
    
    # 비용 계산
    opex_annual = total_revenue * (opex_ratio / 100)
    depreciation = capex * 100000000 / depreciation_years
    financing_cost = capex * 100000000 * (financing_rate / 100)
    total_cost = opex_annual + labor_cost * 100000000 + depreciation + financing_cost
    
    # EBITDA, 영업이익
    ebitda = total_revenue - opex_annual - labor_cost * 100000000
    operating_profit = ebitda - depreciation
    net_profit = operating_profit - financing_cost
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 손익 분석")
        
        pnl_data = pd.DataFrame({
            '항목': ['티핑피 수익', '에너지 수익', '탄소배출권', '총 매출', 
                    'OPEX', '인건비', '감가상각', '금융비용', '총 비용', 
                    'EBITDA', '영업이익', '순이익'],
            '금액(억원)': [
                tipping_revenue_annual/100000000,
                energy_revenue/100000000,
                carbon_credit_revenue/100000000,
                total_revenue/100000000,
                opex_annual/100000000,
                labor_cost,
                depreciation/100000000,
                financing_cost/100000000,
                total_cost/100000000,
                ebitda/100000000,
                operating_profit/100000000,
                net_profit/100000000
            ]
        })
        st.dataframe(pnl_data, use_container_width=True)
    
    with col2:
        st.markdown("### 📈 수익성 지표")
        
        # IRR 계산 (간소화)
        annual_cashflow = ebitda
        payback_years = (capex * 100000000) / annual_cashflow if annual_cashflow > 0 else float('inf')
        
        # 간단 IRR 추정 (NPV=0 되는 할인율)
        def calculate_irr(capex, annual_cf, years):
            for irr in np.arange(0.01, 0.50, 0.01):
                npv = -capex
                for y in range(1, years + 1):
                    npv += annual_cf / ((1 + irr) ** y)
                if npv <= 0:
                    return irr - 0.01
            return 0.50
        
        irr = calculate_irr(capex * 100000000, annual_cashflow, project_years)
        
        # NPV 계산 (할인율 8% 가정)
        discount_rate = 0.08
        npv = -capex * 100000000
        for y in range(1, project_years + 1):
            npv += annual_cashflow / ((1 + discount_rate) ** y)
        
        roi = (net_profit / (capex * 100000000)) * 100
        
        st.markdown(f"""
        <div class="highlight-box">
        <h4>💡 핵심 수익성 지표</h4>
        <table style="width:100%">
            <tr><td><b>총 매출</b></td><td style="text-align:right"><b>{total_revenue/100000000:.1f} 억원/년</b></td></tr>
            <tr><td><b>EBITDA</b></td><td style="text-align:right"><b>{ebitda/100000000:.1f} 억원/년</b></td></tr>
            <tr><td><b>순이익</b></td><td style="text-align:right"><b>{net_profit/100000000:.1f} 억원/년</b></td></tr>
            <tr><td><b>ROI</b></td><td style="text-align:right"><b>{roi:.1f}%</b></td></tr>
            <tr><td><b>IRR</b></td><td style="text-align:right"><b>{irr*100:.1f}%</b></td></tr>
            <tr><td><b>NPV (8%)</b></td><td style="text-align:right"><b>{npv/100000000:.1f} 억원</b></td></tr>
            <tr><td><b>투자회수기간</b></td><td style="text-align:right"><b>{payback_years:.1f} 년</b></td></tr>
        </table>
        </div>
        """, unsafe_allow_html=True)
        
        if irr > 0.15:
            st.success(f"✅ IRR {irr*100:.1f}% - 우수한 투자 수익률!")
        elif irr > 0.10:
            st.info(f"ℹ️ IRR {irr*100:.1f}% - 양호한 투자 수익률")
        else:
            st.warning(f"⚠️ IRR {irr*100:.1f}% - 투자 검토 필요")
    
    st.markdown("---")
    
    # 시나리오 분석
    st.markdown("### 🔄 가동률 시나리오별 IRR 분석")
    
    utilization_scenarios = [60, 70, 80, 90, 100]
    scenario_results = []
    
    for util in utilization_scenarios:
        # 가동률에 따른 수익 재계산
        bg_daily_s = (food_waste_daily * BIOGAS_YIELD_FOOD_WASTE + livestock_daily * BIOGAS_YIELD_LIVESTOCK) * (util/100)
        bg_annual_s = bg_daily_s * operating_days
        
        # 전력 수익
        pwr_s = bg_annual_s * BIOGAS_ENERGY_KWH_NM3 * (power_gen_efficiency/100) * (smp_price + rec_price)
        # RNG 수익
        rng_s = bg_annual_s * (methane_content/100) * rng_purification_rate * rng_price
        # SAF 수익 (간소화)
        ch4_mass_s = bg_annual_s * (methane_content/100) * METHANE_DENSITY_KG_NM3
        saf_mass_s = ch4_mass_s * METHANE_ENERGY_MJ_KG * gtl_efficiency * saf_cut_ratio / SAF_ENERGY_MJ_KG
        saf_s = saf_mass_s / 1000 * saf_price_usd * exchange_rate
        
        # 티핑피, 탄소배출권
        tip_s = tipping_revenue_annual * (util/utilization_rate)
        carbon_s = annual_capacity * (util/utilization_rate) * CO2_REDUCTION_PER_TON_WASTE * carbon_credit_price
        
        for option, rev in [('전력', pwr_s), ('RNG', rng_s), ('SAF', saf_s)]:
            total_s = tip_s + rev + carbon_s
            ebitda_s = total_s - total_s*(opex_ratio/100) - labor_cost*100000000
            irr_s = calculate_irr(capex*100000000, ebitda_s, project_years)
            scenario_results.append({
                '가동률(%)': util,
                '수익화방식': option,
                'IRR(%)': irr_s * 100
            })
    
    scenario_df = pd.DataFrame(scenario_results)
    
    fig6 = px.line(scenario_df, x='가동률(%)', y='IRR(%)', 
                   color='수익화방식', markers=True,
                   title='가동률 및 수익화 방식별 IRR')
    fig6.add_hline(y=10, line_dash="dash", line_color="red", annotation_text="IRR 10%")
    fig6.add_hline(y=15, line_dash="dash", line_color="green", annotation_text="IRR 15%")
    fig6.update_layout(height=450)
    st.plotly_chart(fig6, use_container_width=True)

# ============================================================
# 탭7: 에너지 환산 테이블
# ============================================================
with tab7:
    st.markdown("## 📐 에너지 단위 환산 테이블")
    
    st.markdown("### 1️⃣ 기본 에너지 단위")
    basic_energy = pd.DataFrame({
        '구분': ['kWh → MJ', 'MJ → kWh'],
        '환산식': ['1 kWh = 3.6 MJ', '1 MJ = 0.27778 kWh'],
        '값': ['3.6', '0.27778'],
        '비고': ['전력·열 에너지 변환', '역변환']
    })
    st.dataframe(basic_energy, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("### 2️⃣ 바이오가스·메탄 (천연가스)")
    st.caption("※ 바이오가스는 CH₄ 60% 가정")
    
    biogas_table = pd.DataFrame({
        '구분': ['바이오가스 에너지', '〃', '메탄 에너지(부피)', '〃', '메탄 에너지(질량)', '메탄 밀도'],
        '환산식': [
            '1 Nm³ Biogas ≈ 6 kWh', 
            '1 Nm³ Biogas ≈ 21.6 MJ',
            '1 Nm³ CH₄ ≈ 10 kWh',
            '1 Nm³ CH₄ ≈ 35.8 MJ',
            '1 kg CH₄ ≈ 50 MJ',
            '1 Nm³ CH₄ ≈ 0.717 kg'
        ],
        '값': ['6 kWh/Nm³', '21.6 MJ/Nm³', '10 kWh/Nm³', '35.8 MJ/Nm³', '50 MJ/kg', '0.717 kg/Nm³'],
        '비고': ['CH₄ 60% 기준 LHV', '6×3.6', 'LHV 기준 근사값', '물성치 기반', 'LHV', '0℃, 1 atm 기준']
    })
    st.dataframe(biogas_table, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("### 3️⃣ 수소 (H₂)")
    h2_table = pd.DataFrame({
        '구분': ['수소 에너지(질량)', '수소 에너지(부피)', '〃', '수소 밀도', 'CH₄ → H₂ 이론 전환'],
        '환산식': [
            '1 kg H₂ ≈ 120 MJ',
            '1 Nm³ H₂ ≈ 10.8 MJ',
            '1 Nm³ H₂ ≈ 3.0 kWh',
            '1 Nm³ H₂ ≈ 0.0899 kg',
            '1 Nm³ CH₄ → ≈ 0.36 kg H₂'
        ],
        '값': ['120 MJ/kg', '10.8 MJ/Nm³', '3 kWh/Nm³', '0.0899 kg/Nm³', '0.36 kg/Nm³'],
        '비고': ['LHV', '0℃, 1 atm 기준', '10.8 ÷ 3.6', '0℃, 1 atm 기준', '화학반응식 기준 이론값(효율 미반영)']
    })
    st.dataframe(h2_table, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("### 4️⃣ SAF (지속가능 항공유) / 제트연료")
    saf_table = pd.DataFrame({
        '구분': ['SAF 밀도', '배럴 부피', '배럴당 질량', 'SAF 발열량', '배럴당 에너지'],
        '환산식': [
            'ρ ≈ 0.8 kg/L',
            '1 bbl = 159 L',
            '1 bbl SAF ≈ 159 × 0.8 = 127.2 kg',
            '1 kg SAF ≈ 43 MJ',
            '1 bbl SAF ≈ 127.2×43 ≈ 5,470 MJ'
        ],
        '값': ['0.8 kg/L', '159 L', '≈ 127 kg/bbl (≈0.127 t/bbl)', '43 MJ/kg', '≈ 5,470 MJ/bbl (≈ 1,520 kWh/bbl)'],
        '비고': ['일반 제트연료 수준', '표준 배럴', '', '제트연료 LHV 수준', '']
    })
    st.dataframe(saf_table, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("### 5️⃣ 탄소배출권")
    carbon_table = pd.DataFrame({
        '구분': ['감축계수', '배출권 단위'],
        '환산식': ['폐기물 1톤 처리 시 ≈ 0.18 tCO₂-eq', '1 KOC = 1 tCO₂-eq'],
        '값': ['0.18 tCO₂/톤', '1 tCO₂'],
        '비고': ['1,000,000 ÷ 5,570,000 기준', 'K-ETS 단위 정의']
    })
    st.dataframe(carbon_table, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("### 6️⃣ Biogas → Gas-to-Liquid → SAF (개념식)")
    st.caption("※ 공정마다 효율이 달라지므로 효율·수율 변수로 표현")
    
    gtl_table = pd.DataFrame({
        '단계': ['① Biogas 에너지', '② GTL 전체 효율', '③ SAF cut 비율', '④ SAF 질량', '⑤ SAF 톤', '⑥ SAF 배럴 수'],
        '기호': ['E_bg (MJ)', 'η_GTL', 'Y_SAF', 'm_SAF(kg)', 'ton_SAF', 'bbl_SAF'],
        '개념식': [
            'E_bg = V_bg × 21.6',
            'E_liq = E_bg × η_GTL',
            'E_SAF = E_liq × Y_SAF',
            'm_SAF = E_SAF / 43',
            'ton_SAF = m_SAF / 1,000',
            'bbl_SAF = m_SAF / 127.2'
        ],
        '설명': [
            'V_bg: 바이오가스량(Nm³)',
            '가스 에너지 → FT 액체 에너지 (예: 0.55~0.65)',
            'FT 액체 중 SAF 비율 (예: 0.2~0.3)',
            '43 MJ/kg 사용',
            'kg → 톤 환산',
            '1 bbl ≈ 127.2 kg'
        ]
    })
    st.dataframe(gtl_table, use_container_width=True)
    
    st.markdown("---")
    
    # 환산 계산기
    st.markdown("### 🧮 환산 계산기")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**바이오가스 → 에너지**")
        input_biogas = st.number_input("바이오가스 (Nm³)", 0, 1000000, 10000)
        st.write(f"→ {input_biogas * 6:,.0f} kWh")
        st.write(f"→ {input_biogas * 21.6:,.0f} MJ")
    
    with col2:
        st.markdown("**메탄 → 수소**")
        input_methane = st.number_input("메탄 (Nm³)", 0, 1000000, 10000)
        h2_output = input_methane * 0.36 * 0.75  # 효율 75% 가정
        st.write(f"→ {h2_output:,.1f} kg H₂ (η=75%)")
        st.write(f"→ {h2_output * 120:,.0f} MJ")
    
    with col3:
        st.markdown("**폐기물 → 탄소배출권**")
        input_waste = st.number_input("폐기물 (톤)", 0, 1000000, 10000)
        st.write(f"→ {input_waste * 0.18:,.0f} tCO₂ 감축")
        st.write(f"→ {input_waste * 0.18 * 10000:,.0f} 원 (단가 1만원)")

# ============================================================
# 푸터
# ============================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>⚡ 바이오가스 사업성 종합 분석 대시보드 v2.0</p>
    <p>데이터 기준: 2024년 12월 | 환경부 바이오가스 생산이용 활성화 전략 참고</p>
    <p>⚠️ 본 자료는 참고용 시뮬레이션이며, 실제 사업 검토 시 전문가 컨설팅이 필요합니다.</p>
</div>
""", unsafe_allow_html=True)
