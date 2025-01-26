
import xgboost as xgb
from xgboost import XGBClassifier
import pickle
import streamlit as st

# loading the trained model
pickle_in = open('classifier.pkl', 'rb')
classifier = pickle.load(pickle_in)



@st.cache_data

# defining the function which will make the prediction using the data which the user inputs
def prediction(loan_amnt, int_rate, term, dti, annual_inc, delinq_2yrs,open_acc, grade,home_ownership,collections_12_mths_ex_med,revol_bal, total_acc,last_pymnt_amnt):

    # Pre-processing user input
    if term == "36 Months":
        term = 1
    else:
        term = 0

    if grade == "A":
      grade = 1
    elif grade == "B":
      grade = 2
    elif grade == "C":
      grade = 3
    elif grade == "D":
      grade = 4
    elif grade == "E":
      grade = 5
    else:
      grade = 6


    if home_ownership == "RENT":
      home_ownership = 1
    elif home_ownership == "MORTGAGE":
      home_ownership = 2
    else:
      home_ownership = 3



    # Making predictions
    prediction = classifier.predict(
        [[loan_amnt, int_rate, term, dti, annual_inc, delinq_2yrs,open_acc, grade,home_ownership,collections_12_mths_ex_med,revol_bal, total_acc,last_pymnt_amnt]])

    if prediction == 0:
        pred = 'Approved'
    else:
        pred = 'Not Approved'
    return pred


# this is the main function in which we define our webpage
def main():
    # front end elements of the web page
    html_temp = """
    <div style ="background-color:yellow;padding:13px">
    <h1 style ="color:black;text-align:center;">Streamlit Loan Prediction ML App</h1>
    </div>
    """

    # display the front end aspect
    st.markdown(html_temp, unsafe_allow_html = True)

    # following lines create boxes in which user can enter data required to make prediction
    loan_amnt = st.number_input("Total loan amount")
    int_rate = st.number_input("Interest rate")
    term = st.selectbox('Term',("36 Months","60 Months"))
    dti = st.number_input("dti")
    annual_inc = st.number_input("Annual Income")
    delinq_2yrs = st.number_input("delinq_2yrs")
    open_acc = st.number_input("open_acc")
    grade = st.selectbox('Grade',("A","B","C","D","E","F"))
    home_ownership = st.selectbox('Home Ownership',("RENT","MORTGAGE","OWN"))
    collections_12_mths_ex_med = st.number_input("collections_12_mths_ex_med")
    revol_bal = st.number_input("revol_bal")
    total_acc = st.number_input("total_acc")
    last_pymnt_amnt = st.number_input("last_pymnt_amnt")
    # Married = st.selectbox('Marital Status',("Unmarried","Married"))
    # ApplicantIncome = st.number_input("Applicants monthly income")
    # LoanAmount = st.number_input("Total loan amount")
    # Credit_History = st.selectbox('Credit_History',("Unclear Debts","No Unclear Debts"))
    result =""

    # when 'Predict' is clicked, make the prediction and store it
    if st.button("Predict"):
        result = prediction(loan_amnt, int_rate, term, dti, annual_inc, delinq_2yrs,open_acc, grade,home_ownership,collections_12_mths_ex_med,revol_bal, total_acc,last_pymnt_amnt)
        st.success('Your loan is {}'.format(result))
        print(loan_amnt)

if __name__=='__main__':
    main()
