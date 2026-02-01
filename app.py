
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ملف البيانات
DB_FILE = "data.csv"

def load_data():
    if os.path.exists(DB_FILE):
        try:
            return pd.read_csv(DB_FILE)
        except:
            return pd.DataFrame(columns=["الاسم", "نبات", "حيوان", "كيمياء", "ماث", "فيزياء", "إنجليزي"])
    return pd.DataFrame(columns=["الاسم", "نبات", "حيوان", "كيمياء", "ماث", "فيزياء", "إنجليزي"])

st.set_page_config(page_title="نظام التحليل المتطور", layout="wide")

# تصميم شيك
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: white; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_base_content=True)

menu = ["📝 تسجيل الدرجات", "📊 لوحة تحكم المسؤول"]
choice = st.sidebar.selectbox("الانتقال إلى", menu)

if choice == "📝 تسجيل الدرجات":
    st.title("📝 نموذج تسجيل درجات الطلاب")
    st.write("يرجى إدخال البيانات التالية بدقة:")
    with st.form("student_form", clear_on_submit=True):
        name = st.text_input("الاسم الكامل (اختياري)")
        c1, c2 = st.columns(2)
        with c1:
            botany = st.number_input("درجة النبات", 0, 100, 0)
            zoology = st.number_input("درجة الحيوان", 0, 100, 0)
            chem = st.number_input("درجة الكيمياء", 0, 100, 0)
        with c2:
            math = st.number_input("درجة الماث", 0, 100, 0)
            phys = st.number_input("درجة الفيزياء", 0, 100, 0)
            eng = st.number_input("درجة الإنجليزي", 0, 100, 0)
        
        if st.form_submit_button("إرسال البيانات"):
            df = load_data()
            new_row = {"الاسم": name if name else "مجهول", "نبات": botany, "حيوان": zoology, "كيمياء": chem, "ماث": math, "فيزياء": phys, "إنجليزي": eng}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.success("✅ تم حفظ بياناتك بنجاح!")

else:
    st.title("📊 لوحة التحليل الإحصائي للمسؤول")
    pw = st.text_input("أدخل كلمة السر للوصول", type="password")
    
    if pw == "3070": # الرقم السري الجديد
        df = load_data()
        if not df.empty:
            # الصف الأول: إحصائيات سريعة
            st.write("### 📈 نظرة عامة")
            col1, col2, col3 = st.columns(3)
            col1.metric("إجمالي الطلاب المسجلين", len(df))
            
            # تحليل مادة معينة
            subject = st.selectbox("اختر المادة لتحليلها بشكل دقيق:", ["نبات", "حيوان", "كيمياء", "ماث", "فيزياء", "إنجليزي"])
            
            # رسم بياني احترافي
            fig = px.bar(df, x="الاسم", y=subject, color=subject, 
                         title=f"توزيع درجات الطلاب في مادة {subject}",
                         color_continuous_scale=px.colors.sequential.Viridis,
                         text_auto=True)
            st.plotly_chart(fig, use_container_width=True)

            # قسم حصر الدرجات الضعيفة (تحت الـ 60)
            st.markdown("---")
            st.write(f"### ⚠️ حصر الطلاب (تحت الـ 60) في مادة {subject}")
            
            # تصنيف الدرجات
            low_60_55 = df[(df[subject] < 60) & (df[subject] >= 55)]
            low_55_50 = df[(df[subject] < 55) & (df[subject] >= 50)]
            low_under_50 = df[df[subject] < 50]

            c1, c2, c3 = st.columns(3)
            c1.error(f"درجة (55-59): {len(low_60_55)} طالب")
            c2.error(f"درجة (50-54): {len(low_55_50)} طالب")
            c3.error(f"أقل من 50: {len(low_under_50)} طالب")

            st.write("#### تفاصيل الطلاب ذوي الدرجات المنخفضة:")
            st.table(df[df[subject] < 60][["الاسم", subject]])

            st.markdown("---")
            st.write("### 📋 جدول البيانات الكامل")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("لا توجد بيانات مسجلة حالياً.")
    elif pw:
        st.error("❌ كلمة السر غير صحيحة!")
