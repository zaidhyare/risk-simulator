import streamlit as st
import matplotlib.pyplot as plt
import random

st.title("محاكاة استراتيجية إدارة المخاطر المخصصة")

# الإعدادات
winrate = st.slider("نسبة الفوز (Winrate)", 0.0, 1.0, 0.5, 0.01)
rr = st.number_input("الـ Risk-to-Reward Ratio", value=2.5)
trades = st.number_input("عدد الصفقات", min_value=10, max_value=500, value=100)
initial_capital = st.number_input("رأس المال الابتدائي ($)", value=100.0)

if st.button("ابدأ المحاكاة"):

    capital = initial_capital
    capital_history = [capital]
    risk_percent = 1.0
    winning_streak = 0

    for _ in range(int(trades)):
        is_win = random.random() < winrate
        risk_amount = capital * (risk_percent / 100)

        if is_win:
            capital += risk_amount * rr
            result = "win"
        else:
            capital -= risk_amount
            result = "loss"

        capital_history.append(capital)

        # تحديث المخاطرة حسب الاستراتيجية
        if result == "loss":
            risk_percent = 0.5
            winning_streak = 0
        elif result == "win":
            if risk_percent == 0.5:
                risk_percent = 1.0
            elif risk_percent == 1.0:
                risk_percent = 1.5
            elif risk_percent == 1.5:
                winning_streak += 1
                if winning_streak >= 3:
                    risk_percent = 0.5
                    winning_streak = 0

    # عرض الرسم البياني
    st.subheader("تطور رأس المال")
    fig, ax = plt.subplots()
    ax.plot(capital_history)
    ax.set_xlabel("عدد الصفقات")
    ax.set_ylabel("رأس المال ($)")
    ax.grid(True)
    st.pyplot(fig)

    st.success(f"📈 رأس المال النهائي بعد {trades} صفقة: ${capital:.2f}")
