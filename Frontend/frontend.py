import io
import streamlit as st
import pandas as pd
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
import pickle
import numpy as np 
from specs_states import states,specs
st.set_page_config(layout="wide")

X = pd.read_csv("Columns.csv", nrows=0)


def prediction():
    def format_data(gender,spec,state,tot_hcpcs,avg_age,tot_serv,tot_bene,avg_risk_score,charges_subm,charges_payed):

        formated = {
            "spec": spec,
            "state": state,
            "gender": gender,
            "tot_hcpcs": tot_hcpcs,
            "avg_age": avg_age,
            "tot_serv": tot_serv,
            "tot_bene": tot_bene,
            "avg_risk_score": avg_risk_score,
            "charges_subm": charges_subm,
            "charges_payed": charges_payed
        }

        return formated

    def clear():

        st.session_state['gender']='Male'
        st.session_state['spec']='Addiction Medicine'
        st.session_state['state']='AE'
        st.session_state['tot_hcpcs']=0
        st.session_state['male_bene']=0
        st.session_state['avg_age']=0
        st.session_state['tot_serv']=0
        st.session_state['tot_bene']=0
        st.session_state['avg_risk_score']=0
        st.session_state['charges_subm']=0
        st.session_state['charges_payed']=0
        

    def clear_hist():
        st.session_state.history =pd.DataFrame(data=one_line)

    def highlight(df,column): 
        fraud = pd.Series(data=False, index=df.index)
        fraud[column] = df.loc[column] == 'Potential Fraud'
        return ['background-color: #ED2939' if fraud.any() else '' for v in fraud]
    
    def check_form(tot_hcpcs,avg_age,tot_bene,tot_serv,avg_risk_score,charges_subm,charges_payed):
        val = 1
         
        int_cols={'Total HCPCS':tot_hcpcs,
        'Bene_Avg_Age':avg_age,
        'Total Patients ':tot_bene,
        'Total Services':tot_serv,
        "Avg_risk_score": avg_risk_score,
        "Charges_subm": charges_subm,
        "Charges_payed": charges_payed
        }
    
        for f in int_cols.keys():
            if not isinstance(int_cols[f], (int, float)):
                st.warning("Error! '" + f + "' has to be of type numeric (int or float)")
                val = 0
            else:
                if int_cols[f] < 0: 
                    st.warning("Error! '" + f + "' cannot be negative")
                    val = 0
        return val 
    
    def predict_Fraud(X, gender, spec, state, tot_hcpcs, avg_age, tot_serv, tot_bene, avg_risk_score, charges_subm, charges_payed):
        with open('Model.pkl', 'rb') as file:
            model = pickle.load(file)

        gender_index = np.where(X.columns == gender)[0]
        speciality_index = np.where(X.columns == spec)[0]
        state_index = np.where(X.columns == state)[0]

        x = np.zeros(len(X.columns))
        x[0] = tot_hcpcs
        x[1] = avg_age
        x[2] = tot_serv
        x[3] = tot_bene
        x[4] = avg_risk_score
        x[5] = charges_subm
        x[6] = charges_payed

        if gender_index.size > 0:  
            x[gender_index[0]] = 1  
        if speciality_index.size > 0:  
            x[speciality_index[0]] = 1 
        if state_index.size > 0:  
            x[state_index[0]] = 1  

        pred = model.predict([x])[0]
        label = 'Potential Fraud' if pred == 1 else 'Legitimate'

        return label
    

    one_line={"status":[],'spec':[],'state':[],'gender':[],'tot_hcpcs':[],'male_bene':[],'avg_age':[],'tot_serv':[],'tot_bene':[],'avg_risk_score':[],'charges_subm':[],'charges_payed':[]}

    history=pd.DataFrame(data=one_line)

    if 'history' not in st.session_state:
        st.session_state['history'] = history

    st.markdown("<h1 style='text-align: center;'>MedGuard fraud detection</h1>", unsafe_allow_html=True)
    st.markdown("""---""")

    with st.container():
        
        st.subheader('Enter the practitioner annual details :')
        col1, col2 = st.columns([1,1],gap='small')

        with col1:
            gender = st.radio("Gender or Org :",('Male', 'Female','Organization'),horizontal=True,key='gender')
            spec=st.selectbox('Specialty :',options=sorted(specs),key='spec')
            state=st.selectbox('State :',options=sorted(states),key='state')
            tot_hcpcs = st.number_input("Total HCPCS :",key='tot_hcpcs',min_value=0.00)
            avg_age = st.number_input("Average Age :",key='avg_age',min_value=0.00)
            
            

        with col2:
            tot_serv = st.number_input("Total Services :",key='tot_serv',min_value=0.00)
            tot_bene = st.number_input("Total Patients :",key='tot_bene',min_value=0.00)
            avg_risk_score = st.number_input("Average Risk Score :",key='avg_risk_score',min_value=0.00)
            charges_subm = st.number_input("Charges Submitted :",key='charges_subm',min_value=0.00)
            charges_payed = st.number_input("Charges Paid :",key='charges_payed',min_value=0.00)
        
        col5,col6,col7,col8,col9 = st.columns(5,gap='small')

        with col5:
            pass
        with col6:
        
            submitted = st.button("Submit")
        with col7:
            
            st.button("Clear",on_click=clear)
        with col8:
            
            hist = st.button("History")
        with col9:
            pass

        if(submitted):
            if(check_form(tot_hcpcs,avg_age,tot_bene,tot_serv,avg_risk_score,charges_subm,charges_payed)):
                with st.spinner('Processing ...'):
                    data_pract= format_data(gender,spec,state,tot_hcpcs,avg_age,tot_serv,tot_bene,avg_risk_score,charges_subm,charges_payed)
                    label=predict_Fraud(X,gender,spec,state,tot_hcpcs,avg_age,tot_serv,tot_bene,avg_risk_score,charges_subm,charges_payed)
                    
                    if(label=='Potential Fraud'):
                        fraud =  st.error(label)
                    
                    elif (label=='Legitimate') :
                        legit =  st.success(label)
                    
                    one_line['status']=label
                    for key in data_pract.keys():
                        one_line[key]=data_pract[key]
                    
                    st.session_state.history=pd.concat([st.session_state.history, pd.DataFrame.from_dict(one_line,orient='index').T],ignore_index=True)
                    

        if(hist):
            df_tmp = st.session_state.history.style.apply(highlight, column='status',axis=1)
            st.write(df_tmp)
            if(st.session_state.history.shape[0]!=0):
                col66,col77,col99,col90 = st.columns(4,gap='small')
                with col66:
                    pass
                with col77:
                    buffer = io.BytesIO()
                    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                        df_tmp.to_excel(writer,index=False)
                        
                    st.download_button(label="Download",data=buffer,file_name='History.xlsx',mime="application/vnd.ms-excel")
                
                with col99:
                    
                    st.button(label='Clear History',on_click=clear_hist)
                        
                
    st.write()
    st.markdown("""---""")
    st.write()




def home():
    # Image in local 


    # use following for aws cloud 
    # st.image("medicare-fraud.jpg",width=100, use_container_width=True)

    st.markdown("<h1 style='text-align: center;'>MedGuard Fraud Detection System</h1>", unsafe_allow_html=True)
    st.markdown("""---""")
    st.header("Project Goal")
    st.write(
        """
        The primary goal is to develop a strong classification model that can anticipate and identify fraudulent behaviors 
        in Medicare claims data.
        """
    )
    st.write(
        """
        The dataset used describes the services and procedures that health care professionals provide to Medicare beneficiaries. 
        The records in the dataset contain various provider-level attributes, such as National Provider Identifier (NPI), 
        first and last name, gender, address, etc. In addition, the records contain information that describes a provider's 
        Medicare activity in a given year. Examples include: the procedure performed, the average fee submitted to Medicare, 
        the average amount paid by Medicare, and the location of service.
        """
    )

    st.write(
        """
        This dataset is aggregated at the NPI level, the identifier of a provider, and contains information for the years 
        2016 through 2019 with over one million records and 73 variables for each year, which makes this database an 
        excellent candidate for data analysis and machine learning.
        """
    )

    st.write(
        """
        The Medicare provider fraud labels are identified using LEIE data, LEIE is maintained by the OIG in accordance 
        with sections 1128 and 1156 of the Social Security Act and is updated monthly. The OIG has the authority to 
        exclude providers from federally funded health care programs for various reasons. Excluded individuals cannot 
        receive payment from federal health programs for any services, and must apply for reinstatement once their 
        exclusion period has expired. The current LEIE data format contains 18 attributes that describe the provider 
        and the reason for the exclusion.
        """
    )

    # Datasets section
    st.header("Datasets Used")
    st.write(
        """
        We used the following official datasets given by the Centers for Medicare and Medicaid Services (CMS):
        1. **Medicare Part B** (Physician and Other Practitioners - by Provider). https://data.cms.gov/provider-summary-by-type-of-service/medicare-physician-other-practitioners/medicare-physician-other-practitioners-by-provider
        2. **LEIE Data** (List of Excluded Individuals and Entities). https://www.oig.hhs.gov/exclusions/exclusions_list.asp
        """
    )

    # Technologies section
    st.header("Technologies Employed")
    st.write(
        """
        The technologies employed were:
        - **PySpark**
        - **AWS S3**
        - **MySQL**
        - **Python** (Pandas, Sklearn, Matplotlib)
        - **Tableau**
        - **AWS EC2**
        - **Streamlit**
        """
    )

def dashboard():
    st.title("MedGuard Fraud Detection System Dashboard")
    
    tableau_embed_code = """
    <div class='tableauPlaceholder' id='viz1738731464990' style='position: relative'>
        <noscript>
            <a href='#'>
                <img alt=' ' src='https://public.tableau.com/static/images/Pr/Project_final_17386603042680/Dashboard1/1_rss.png' style='border: none' />
            </a>
        </noscript>
        <object class='tableauViz' style='display:none;'>
            <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' />
            <param name='embed_code_version' value='3' />
            <param name='site_root' value='' />
            <param name='name' value='Project_final_17386603042680/Dashboard1' />
            <param name='tabs' value='no' />  <!-- Changed to 'no' -->
            <param name='toolbar' value='no' />  <!-- Changed to 'no' -->
            <param name='static_image' value='https://public.tableau.com/static/images/Pr/Project_final_17386603042680/Dashboard1/1.png' />
            <param name='animate_transition' value='yes' />
            <param name='display_static_image' value='yes' />
            <param name='display_spinner' value='yes' />
            <param name='display_overlay' value='yes' />
            <param name='display_count' value='yes' />
            <param name='language' value='en-US' />
            <param name='filter' value='publish=yes' />
        </object>
    </div>
    <script type='text/javascript'>
        var divElement = document.getElementById('viz1738731464990');
        var vizElement = divElement.getElementsByTagName('object')[0];
        if (divElement.offsetWidth > 800) {
            vizElement.style.width = '100%';
            vizElement.style.height = (divElement.offsetWidth * 0.75) + 'px';
        } else if (divElement.offsetWidth > 500) {
            vizElement.style.width = '100%';
            vizElement.style.height = (divElement.offsetWidth * 0.75) + 'px';
        } else {
            vizElement.style.width = '100%';
            vizElement.style.minHeight = '1800px';
            vizElement.style.maxHeight = (divElement.offsetWidth * 1.77) + 'px';
        }
        var scriptElement = document.createElement('script');
        scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
        vizElement.parentNode.insertBefore(scriptElement, vizElement);
    </script>
    """
    st.components.v1.html(tableau_embed_code, height=900, scrolling=False)


def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select a page:", ["Home", "Prediction", "Dashboard"])

    if page == "Home":
        home()
    elif page == "Prediction":
        prediction()
    elif page == "Dashboard":
        dashboard()
 
if __name__ == "__main__":
    main()                      
                        
                
        
                








        