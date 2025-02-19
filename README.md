[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://mohamed-lahna-medicare-fraud-detection-streamlitmain-dep-5q9z51.streamlitapp.com/)

# MedGuard: Fraud Detection System
MedGuard is a comprehensive framework designed to identify and mitigate the fraudulent activities in the healthcare sector. 
Utilizing machine learning algorithms and data analytics, MedGuard aims to preserve the integrity of healthcare transactions, ensuring that resources are allocated efficiently and ethically.

* Check the notebooks for more details about data processing and model training/evaluation.

## Requirements
* Python 3.9+
* Tableau
* PySpark

## Usage 
#### Launching the app
* Make sure that the requirements are installed : 
```python
pip install -r requirements.txt
``` 
* Launch the app from terminal :
```
streamlit run frontend.py
``` 


__It is essential that the CSV file adheres to a specific order of columns/variables:__
   
    1. Rndrng_Prvdr_Type
    2. State
    3. Total HCPCS_Cds
    4. Provider_Gender_Or_Organization
    5. Average Age
    6. Total Services
    7. Total Beneficiaries
    8. Average Risk Score
    9. Charges Submitted
    10. Charges Paid 
    11. Fraud

#### Creating the virtual environment
* Run the following command to create python virtual environment:
```python
python -m venv myenv
``` 
* Activate the environment :
```python
python -m venv myenv/Scripts/activate
``` 
## Data used
### Overview
 The primary data source for this project is the official website of the Centers for Medicare & Medicaid Services (CMS), a federal agency under the Department of Health and Human Services (HHS). CMS oversees major healthcare programs, including Medicare and Medicaid.

This dataset is aggregated at the NPI level,first_name and last_name of the identifier of a provider/organization, and contains information for the years 2019, 2020, 2021 and 2022 with around 4.75 million records and 82 variables for each year, which makes this database an excellent candidate for data analysis and machine learning.

The Medicare provider fraud labels are identified using LEIE data, LEIE is maintained by the OIG in accordance with sections 1128 and 1156 of the Social Security Act and is updated monthly. The OIG has the authority to exclude providers from federally funded health care programs for various reasons. Excluded individuals cannot receive payment from federal health programs for any services, and must apply for reinstatement once their exclusion period has expired. The current LEIE data format contains 18 attributes that describe the provider and the reason for the exclusion.
### Data sampling
After data processing and labeling , the final dataset includes information on 47,54,509 practitioners, of which 20,058 are fraudulent, which represents a little over 0.42% of the total workforce.

The fraud rate (0.42%) does not reflect reality (10% worldwide), therefore it is necessary to select a sample of the negative class (population) to increase the fraud rate up to 10%.
The sample was selected using random sampling, and statistical tests were used to ensure that it was not biased.

Check the notebooks for more details.