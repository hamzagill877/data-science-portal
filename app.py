import streamlit as st
import pandas as pd

st.set_page_config(page_title="IUB BSDS Portal", page_icon="🎓", layout="wide")

@st.cache_data
def load_students():
    return pd.read_csv("students.csv", dtype=str).fillna("")
@st.cache_data
def load_results():
    try: return pd.read_csv("results.csv", dtype=str).fillna("")
    except: return pd.DataFrame()

if 'login' not in st.session_state:
    st.session_state.login=False; st.session_state.roll=""

students=load_students(); results_df=load_results()

if not st.session_state.login:
    st.title("🎓 IUB BSDS - Complete Portal")
    st.markdown("**Har Student - Sara Record, Result, Timetable**")
    t1,t2=st.tabs(["🔐 Login","✨ Registration"])
    with t1:
        roll=st.text_input("Roll No / Email"); pwd=st.text_input("Password",type="password")
        if st.button("Login",type="primary",use_container_width=True):
            m=students[(students['Roll_No'].str.lower()==roll.lower())|(students['Email'].str.lower()==roll.lower())]
            if not m.empty and m.iloc[0]['Password']==pwd:
                st.session_state.login=True; st.session_state.roll=m.iloc[0]['Roll_No']; st.rerun()
            else: st.error("Ghalat Roll/Email ya Password")
        st.info("Demo: BSDS-2ND-001 / password123")
    with t2:
        with st.form("reg"):
            r=st.text_input("Roll No*"); n=st.text_input("Name*"); f=st.text_input("Father Name"); e=st.text_input("Email*"); ph=st.text_input("Phone"); sem=st.selectbox("Semester",["1st","2nd","3rd","4th","5th","6th","7th","8th"]); c=st.text_input("CGPA","3.0"); p=st.text_input("Password*",type="password")
            if st.form_submit_button("Account Banao",use_container_width=True):
                if r and n and e and p:
                    pd.DataFrame([{'Roll_No':r,'Name':n,'Father_Name':f,'Email':e,'Phone':ph,'Semester':sem,'CGPA':c,'Password':p,'Attendance':'90%','Department':'BS Data Science','Session':'2023-27','CNIC':'','Address':''}]).to_csv("students.csv",mode='a',header=False,index=False)
                    st.success("Account ban gaya! Login karo"); st.cache_data.clear()
    st.stop()

students=load_students(); results_df=load_results()
me=students[students['Roll_No']==st.session_state.roll].iloc[0]
my_res=results_df[results_df['Roll_No']==st.session_state.roll]

with st.sidebar:
    st.title(f"👋 {me['Name']}"); st.metric("CGPA",me['CGPA']); st.metric("Semester",me['Semester'])
    if st.button("🚪 Logout",use_container_width=True): st.session_state.login=False; st.rerun()

st.title(f"Welcome {me['Name']} 🎉")
t1,t2,t3,t4=st.tabs(["📊 Mera Record","📜 Sara Result","📅 Timetable","👤 Full Info"])
with t1:
    st.subheader(f"{me['Semester']} Semester Result")
    if not my_res.empty: st.dataframe(my_res,use_container_width=True,hide_index=True)
    else: st.dataframe(pd.DataFrame({"Subject":["Python","Stats-II","Linear Alg","DS","Skills","Islamiat"],"Marks":[85,78,88,82,75,80],"Grade":["A","B+","A","A-","B","A-"]}),use_container_width=True)
with t2:
    st.subheader("Sara Pichla Result")
    for s in ["1st","2nd"]:
        with st.expander(f"{s} Semester",expanded=True):
            d=my_res[my_res['Semester']==s]
            if not d.empty: st.table(d)
            else:
                if s=="1st": st.table(pd.DataFrame({"Subject":["Intro DS","Calculus","PF","English","Pak Studies"],"Marks":[80,75,85,78,70],"Grade":["A-","B+","A","B+","B"]}))
                else: st.table(pd.DataFrame({"Subject":["Python","Stats-II","Linear Alg","DS","Skills","Islamiat"],"Marks":[85,78,88,82,75,80],"Grade":["A","B+","A","A-","B","A-"]}))
with t3:
    st.subheader("Timetable - All Semesters")
    sel=st.selectbox("Semester", ["1st","2nd","3rd","4th","5th","6th","7th","8th"], index=1)
    tt={"Mon":["Python","Stats-II","DS","Lab"],"Tue":["Linear Alg","Python","Islamiat","Sports"],"Wed":["Stats-II","DS","Python Lab","Skills"],"Thu":["DS","Linear Alg","Stats Lab","Python"],"Fri":["Skills","Islamiat","-","-"]}
    df=pd.DataFrame(tt); df.index=["09:00-10:30","10:30-12:00","12:00-01:30","02:00-03:30"]; st.table(df)
with t4:
    st.subheader("Full Profile")
    st.write(f"**Name:** {me['Name']} | **Father:** {me.get('Father_Name','')} | **Roll:** {me['Roll_No']}")
    st.write(f"**Email:** {me['Email']} | **Phone:** {me.get('Phone','')} | **CGPA:** {me['CGPA']} | **Session:** {me.get('Session','')}")
    st.write(f"**Dept:** {me.get('Department','')} | **Address:** {me.get('Address','')}")
