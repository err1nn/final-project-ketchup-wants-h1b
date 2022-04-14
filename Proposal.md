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
We will provide visualizations and the prediction application using the following two datasets. In all, the data cleaning and processing are not substantial since the raw dataset has already been clean, and all we need to do is extract the useful information from them and convert them into the right format for visualizations.

**1. H-1B Employer Data**

We collected the annaul data from 2019 to 2021 and combined three datasets into one. We only kept columns including Employer, State, City, ZIP Code. We summed Initial Approval and Continuing Approval into Total Approval, Initial Denial and Continuing Deinal into Total Denial, to provide the complete data throughout the three years.

We plan to use this data to generate a choropleth map that shows the aggregate summary of total approved and denied H-1B applications from the spatial view.

**2. LCA Data (H-1B Applicants Data)**

We collected annual data from 2019 to 2021 and combined three datasets into one.

For data pre-processing, we first filtered the data by visa type and only kept H-1B visa applications. Second, we removed the columns that we are not using in the prediction model. There are 13 columns in our final dataset. Finally, we removed all rows which include missing values (NA) to have the complete data for model training and it is feasible because there is only a little amount of data that contain NA. Our final data has 123,863 rows.

| Variable      |
| ------------- |
| CASE_NUMBER   |
| CASE_STATUS   |
| RECEIVED_DATE |
| DECISION_DATE |
| EMPLOYER_NAME |
| EMPLOYER_NUM_EMPLOYEES|
| WORKSITE_CITY |
| WORKSITE_STATE|
| WAGE_OFFER_FROM|
| JOB_TITLE     |
| COUNTRY_OF_CITIZENSHIP|
| FOREIGN_WORKER_EDUCATION|
| FOREIGN_WORKER_INFO_MAJOR|

In addition to insightful visualizations, we will also build a ML-based prediction model using this dataset. We will partition the data into two groups, 80% for training and 20% for testing.

#### System Design
How will you display your data? What types of interactions will you support? Provide some sketches that you have for the system design.

### References
1. Swain, D., Chakraborty, K., Dombe, A., Ashture, A., & Valakunde, N. (2018, December). [Prediction of H1B Visa Using Machine Learning Algorithms.](https://ieeexplore.ieee.org/abstract/document/8933628?casa_token=kw9Mm8Q-unoAAAAA:U80awNcdpk4JT3KkKXAomHdGDWywIcO4MUl-BGwBuJqJd5NhPpzb1DKgNTsfCzlQuONylqyIlg) In 2018 International Conference on Advanced Computation and Telecommunication (ICACAT) (pp. 1-7). IEEE.
