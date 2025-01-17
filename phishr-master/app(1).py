import streamlit as st
import machine_learning as ml
import feature_extraction as fe
from bs4 import BeautifulSoup
import requests as re
import matplotlib.pyplot as plt

# col1, col2 = st.columns([1, 3])

st.title('Phishing Website Detection using Machine Learning')
st.write('This ML-based app is developed for educational purposes. Objective of the app is detecting phishing websites only using content data. Not URL!'
         ' You can see the details of approach, data set, and feature set if you click on _"See The Details"_. ')


with st.expander("PROJECT DETAILS"):
    st.subheader('Approach')
    st.write('We used _supervised learning_ to classify phishing and legitimate websites. '
             'We benefit from content-based approach and focus on html of the websites. '
             'Also, We used scikit-learn for the ML models.'
             )
    st.write('For this educational project, '
             'We created my own data set and defined features, some from the literature and some based on manual analysis. '
             'We used requests library to collect data, BeautifulSoup module to parse and extract features. ')
    st.write('The source code and data sets are available in the below Github link:')
    st.write('https://github.com/SasiCherukuri123/Phishing-Detection')

    st.subheader('Data set')
    # ----- FOR THE PIE CHART ----- #
    labels = 'phishing', 'legitimate'
    phishing_rate = int(ml.phishing_df.shape[0] / (ml.phishing_df.shape[0] + ml.legitimate_df.shape[0]) * 100)
    legitimate_rate = 100 - phishing_rate
    sizes = [phishing_rate, legitimate_rate]
    explode = (0.1, 0)
    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, shadow=True, startangle=90, autopct='%1.1f%%')
    ax.axis('equal')
    st.pyplot(fig)
    # ----- !!!!! ----- #

    st.write('Features + URL + Label ==> Dataframe')
    st.markdown('label is 1 for phishing, 0 for legitimate')
    number = st.slider("Select row number to display", 0, 100)
    st.dataframe(ml.legitimate_df.head(number))


    @st.cache
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    csv = convert_df(ml.df)

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='phishing.csv',
        mime='text/csv',
    )

    st.subheader('Features')
    st.write('We used only content-based features. I didn\'t use url-based faetures like length of url etc.'
             'Most of the features extracted using find_all() method of BeautifulSoup module after parsing html.')

    st.subheader('Results')
    st.write('We used 10 different ML classifiers of scikit-learn and tested them implementing k-fold cross validation.'
             'Firstly obtained their confusion matrices, then calculated their accuracy, precision and recall scores.')
    
    st.write('GCMLP --> Gradient + Catboost + Multi-layer Perceptron')
    st.write('CC --> CatBoost Classifier')
    st.write('RF --> Random Forest')
    st.write('GBC --> Gradient Boosting Classifier')
    st.write('MLP --> Multi-layer Perceptron')
    st.write('DTSVMRF --> Decision Tree + SVM + Random Forest')
    st.write('SVM --> Support Vector Machine')
    st.write('DT --> Decision Tree')
    st.write('KN --> K-Neighbours')
    st.write('LR --> Logistic Regression')


choice = st.selectbox("Please select your machine learning model",
                 [
                     'Gradient + Catboost + Multi-layer Perceptron', 'CatBoost Classifier', 'Random Forest', 'Gradient Boosting Classifier', 'Multi-layer Perceptron', 'Decision Tree + SVM + Random Forest', 
                     'Support Vector Machine', ' Decision Tree', 'K-Neighbours', ' Logistic Regression'
                 ]
                )

model = ml.nb_model

if choice == 'Gradient + Catboost + Multi-layer Perceptron':
    model = ml.nb_model
    st.write('GCMLP model is selected!')
elif choice == 'CatBoost Classifier':
    model = ml.svm_model
    st.write('CC model is selected!')
elif choice == 'Random Forest':
    model = ml.dt_model
    st.write('RF model is selected!')
elif choice == 'Random Forest':
    model = ml.rf_model
    st.write('RF model is selected!')
elif choice == 'Gradient Boosting Classifier':
    model = ml.ab_model
    st.write('GBC model is selected!')
elif choice == ' Multi-layer Perceptron':
    model = ml.nn_model
    st.write('MLP model is selected!')
elif choice == ' Decision Tree + SVM + Random Forest':
    model = ml.nn_model
    st.write('DTSVMRF model is selected!')
elif choice == ' Support Vector Machine':
    model = ml.nn_model
    st.write('SVM model is selected!')
elif choice == 'Decision Tree':
    model = ml.nn_model
    st.write('DT model is selected!')
elif choice == 'K-Neighbours':
    model = ml.nn_model
    st.write('KN model is selected!')
elif choice == 'Logistic Regression':
    model = ml.nn_model
    st.write('LR model is selected!')
else:
    model = ml.kn_model
    st.write('GCMLP model is selected!')


url = st.text_input('Enter the URL')
# check the url is valid or not
if st.button('Check!'):
    try:
        response = re.get(url, verify=False, timeout=4)
        if response.status_code != 200:
            print(". HTTP connection was not successful for the URL: ", url)
        else:
            soup = BeautifulSoup(response.content, "html.parser")
            vector = [fe.create_vector(soup)]  # it should be 2d array, so I added []
            result = model.predict(vector)
            if result[0] == 0:
                st.success("This web page seems a legitimate!")
                st.balloons()
            else:
                st.warning("Attention! This web page is a potential PHISHING!")
                st.snow()

    except re.exceptions.RequestException as e:
        print("--> ", e)





