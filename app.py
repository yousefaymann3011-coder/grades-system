import streamlit as st
import pandas as pd
import plotly.express as px
import os

# اسم الملف
DB_FILE = "data.csv"

# دالة محسنة لتحميل البيانات بدون أخطاء
def load_data():
    if os.path.exists(DB_FILE):
        try:
            return pd.read_csv(DB_FILE)
        except:
            return pd.DataFrame(columns=["الاسم", "نبات", "حيوان", "كيمياء", "ماث", "فيزياء", "إنجليزي"])
    return pd.DataFrame(columns=["الاسم", "نبات", "حيوان", "كيمياء", "ماث", "فيزياء", "إنجليزي"])

st.set_page_config(page_title="نظام الدرجات الذكي", layout="centered")

# القائمة الجانبية
menu = ["تسجيل درجاتي", "لوحة تحكم المعلم"]
choice = st.sidebar.selectbox("اختر الصفحة", menu)

if choice == "تسجيل درجاتي":
    st.title("📝 أدخل درجاتك هنا")
    with st.form("my_form", clear_on_submit=True):
        name = st.text_input("الاسم (اختياري)")
        c1, c2 = st.columns(2)
        with c1:
            botany = st.number_input("نبات", 0, 100, value=0)
            zoology = st.number_input("حيوان", 0, 100, value=0)
            chem = st.number_input("كيمياء", 0, 100, value=0)
        with c2:
            math = st.number_input("ماث", 0, 100, value=0)
            phys = st.number_input("فيزياء", 0, 100, value=0)
            eng = st.number_input("إنجليزي", 0, 100, value=0)
        
        submit = st.form_submit_button("حفظ الدرجات")
        
        if submit:
            df = load_data()
            new_data = {
                "الاسم": name if name else "مجهول",
                "نبات": botany, "حيوان": zoology, "كيمياء": chem,
                "ماث": math, "فيزياء": phys, "إنجليزي": eng
            }
            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.success("✅ تم الحفظ بنجاح!")

else:
    st.title("📊 تحليل نتائج الطلاب")
    pw = st.text_input("كلمة السر", type="password")
    if pw == "1234":
        df = load_data()
        if not df.empty:
            sub = st.selectbox("اختر المادة للتحليل", ["نبات", "حيوان", "كيمياء", "ماث", "فيزياء", "إنجليزي"])
            fig = px.histogram(df, x=sub, title=f"توزيع درجات {sub}", color_discrete_sequence=['#1a73e8'])
            st.plotly_chart(fig)
            st.write("### جدول البيانات:")
            st.dataframe(df)
        else:
            st.info("لا توجد بيانات مسجلة بعد.")
    elif pw:
        st.error("كلمة السر غير صحيحة")
