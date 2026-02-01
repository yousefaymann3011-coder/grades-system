import streamlit as st
import pandas as pd
import plotly.express as px
import os
# اسم ملف تخزين البيانات
DB_FILE = "students_data.csv"
# دالة لتحميل البيانات
def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["الاسم", "نبات", "حيوان", "كيمياء", "ماث", "فيزياء", "إنجليزي"])
# إعداد الصفحة بستايل جوجل
st.set_page_config(page_title="نظام الدرجات", layout="centered")
# CSS لإعطاء طابع Google Docs
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { background-color: #1a73e8; color: white; border-radius: 4px; }
    </style>
    """, unsafe_base_content=True)
menu = ["إدخال الدرجات", "لوحة تحكم المسؤول (🔒)"]
choice = st.sidebar.selectbox("القائمة", menu)
if choice == "إدخال الدرجات":
    st.title("📝 نموذج تسجيل الدرجات")
    st.info("برجاء إدخال درجاتك بدقة. الاسم اختياري.")
    with st.form("entry_form"):
        name = st.text_input("الأسم (اختياري)")
        c1, c2 = st.columns(2)
        with c1:
            botany = st.number_input("نبات", 0, 100)
            zoology = st.number_input("حيوان", 0, 100)
            chem = st.number_input("كيمياء", 0, 100)
        with c2:
            math = st.number_input("ماث", 0, 100)
            phys = st.number_input("فيزياء", 0, 100)
            eng = st.number_input("إنجليزي", 0, 100)
        submit = st.form_submit_button("إرسال البيانات")
        if submit:
            df = load_data()
            new_row = [name if name else "مجهول", botany, zoology, chem, math, phys, eng]
            df.loc[len(df)] = new_row
            df.to_csv(DB_FILE, index=False)
            st.success("تم الحفظ بنجاح! شكراً لك.")
else:
    st.title("📊 تحليل الدرجات")
    password = st.text_input("أدخل كلمة السر للمشاهدة", type="password")
    if password == "1234": # تقدر تغير كلمة السر من هنا
        df = load_data()
        if not df.empty:
            st.write("### إحصائيات عامة")
            subject = st.selectbox("اختر المادة للتحليل", ["نبات", "حيوان", "كيمياء", "ماث", "فيزياء", "إنجليزي"])
            fig = px.histogram(df, x=subject, title=f"توزيع درجات {subject}", color_discrete_sequence=['#1a73e8'])
            st.plotly_chart(fig)
            st.write("### جدول البيانات الكامل")
            st.dataframe(df)
        else:
            st.warning("لا توجد بيانات مسجلة بعد.")
    elif password:
        st.error("كلمة السر خطأ!")