# Final Project Proposal

**GitHub Repo URL:** https://github.com/CMU-IDS-2022/final-project-ketchup-wants-h1b

**Topic:** A Customized Platform to Understand the H-1B Visa Application Status and A Machine Learning-Based Prediction Model

### Motivation
The H-1B visa allows employers in the United States to temporarily employ foreign workers in occupations that require the theoretical and practical application of a body of highly specialized knowledge and a bachelor's degree or higher in the specific specialty or its equivalent.

We, as international students, will need to obtain an H-1B visa to work in the United States.  However, there are only a limited number of visas available each year. It is beneficial for international students to have a one-stop platform to understand the visa application status quo of their interested employers.

### Problem Definition
The purpose of our project is to provide a one-stop platform for international students to obtain information about H-1B visa sponsors during the process of job searching. Our platform will be composed of two sections:
- Informational visualizations of H-1B visa applications that allow users to query H-1B applications based on company, job titles, wages, city of work, etc
- A machine learning-based model that estimates the probability of visa approval on the basis of data collected

We are interested in exploring the following questions:
- Is it possible to predict the number of approved visas for each company based on their historical data?
- How do different factors, including job titles, wages, cities of work relate to the probability of getting a visa?
- Are we able to predict the probability of H-1B visa approvals based on historical data?

### Expected Deliverables
Our final product would be a one-stop platform. We would present the customized results through a series of visualizations that allow the users to filter the data based on factors of interest. As an example of the use case, one may be interested in knowing top 10 companies that offer visa sponsorship to software engineer roles. Additionally, we will develop a machine learning-based model to predict the probability of visa approval based on the personal information of the user.

### Datasets
1. [H1B employers data hub, United States Citizenship and Immigration Services](https://www.uscis.gov/tools/reports-and-studies/h-1b-employer-data-hub/h-1b-employer-data-hub-files)
2. [LCA data for H1B, H1B1, E3, US Department of Labor](https://www.dol.gov/agencies/eta/foreign-labor/performance)

### Sketches and Data Analysis

#### Data Processing
- Do you have to do substantial data cleanup? What quantities do you plan to derive from your data? How will data processing be implemented?  Show some screenshots of your data to demonstrate you have explored it.
##### H1B employer data
We selected the data from 2019 to 2021 and combine three datasets into one. We only keep columns like Employer, State, City, ZIP. Also, we sum Initial Approval and Continuing Approval into Approval, Initial Denial and Continuing Deinal into Denial.

##### LCA data
We selected data from 2019 to 2021 and combined three datasets together. First of all, we filter the data by visa type and only keep H1B visa applications. Second, we remove the columns which cannot provide us useful information for visualization or building a prediction model. ([Inital data columns](https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/PERM_Record_Layout_FY2020.pdf)) We only keep 13 columns for our model training process:
- CASE_NUMBER                     
- CASE_STATUS                     
- RECEIVED_DATE                   
- DECISION_DATE                   
- EMPLOYER_NAME                   
- EMPLOYER_NUM_EMPLOYEES        
- WORKSITE_CITY                   
- WORKSITE_STATE                  
- WAGE_OFFER_FROM                 
- JOB_TITLE                       
- COUNTRY_OF_CITIZENSHIP          
- FOREIGN_WORKER_EDUCATION        
- FOREIGN_WORKER_INFO_MAJOR   
Finally, we remove all rows which include na. Our final data has 123,863 rows. 

#### System Design
How will you display your data? What types of interactions will you support? Provide some sketches that you have for the system design.

### References
1. Swain, D., Chakraborty, K., Dombe, A., Ashture, A., & Valakunde, N. (2018, December). [Prediction of H1B Visa Using Machine Learning Algorithms.](https://ieeexplore.ieee.org/abstract/document/8933628?casa_token=kw9Mm8Q-unoAAAAA:U80awNcdpk4JT3KkKXAomHdGDWywIcO4MUl-BGwBuJqJd5NhPpzb1DKgNTsfCzlQuONylqyIlg) In 2018 International Conference on Advanced Computation and Telecommunication (ICACAT) (pp. 1-7). IEEE.
