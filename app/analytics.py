# analytics.py
import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split as ttt
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor as dt
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# Connect to MongoDB
def anal(collection):

    df = pd.DataFrame(list(collection.find()))
    st.title("Analytics")
    df = df.set_index("_id")

    #COLUMN SPLITTING
    num = [x for x in df if str(df[x].dtype) == 'int64' if df[x].nunique() < 11]
    cat = [x for x in df if str(df[x].dtype) == 'object' if len(df[x][0]) <30]
    prf = ['gpa', 'stud_hb', 'stud_hr', 'attend']
    ovhap = ['hap_rate', 'hap_fact']
    hap = ['acad_impc', 'acad_press', 'acad_guilt', 'ch_guilt', 'gr_guilt', 'bal_contri', 'proc', 'wl_bal', 'extra_curr_hap', 'attd_impc']
   
    st.header("The data:")
    st.dataframe(df.head(5))

    # Summary statistics
    st.header("Summary Statistics")
    st.write(df.describe())

    # Distribution of Age
    st.header("Age Distribution")
    st.bar_chart(df['age'].value_counts())

    # Gender Distribution
    st.header("Gender Distribution")
    st.bar_chart(df['gen'].value_counts())

    # Academic Program Distribution
    st.header("Academic Program Distribution")
    st.bar_chart(df['acad_prg'].value_counts())

    #Happiness Factors
    st.header("Happiness Factors")
    f, a = plt.subplots(1, 1)
    df[ovhap].groupby('hap_fact').mean().plot(kind='pie', subplots=True, ax=a)
    st.pyplot(f)

    # Year of study dist
    st.header("Year of Study Distribution")
    st.bar_chart(df['yo_stud'].value_counts())

    # Select either Happiness or Performance 
    st.header("Select Happiness or Performance")
    opt = st.selectbox("Select which metric to expand upon: ",['Happiness','Performance'])

    if opt == "Performance":
        st.write("Performance attributes: ",prf)
        genre = st.radio(
            "Choose the type of plot",
            ["KDE", "Groupby", "Scatter", "Violin & Boxplot"],
            captions = ["Density/Distribution", "Groupby various categorical attributes","Pairwise scatter", "Outlier visualisation"])
        if genre == "KDE":
            fig, ax = plt.subplots()
            sns.kdeplot(df[prf].groupby('attend').mean(), ax=ax)
            st.subheader("KDE plot Student Performance metric")
            st.pyplot(fig)

        elif genre == "Groupby":
            fig, ax = plt.subplots()
            df[prf].groupby('attend').mean().plot(kind='barh', subplots=False, ax=ax)
            st.subheader("Distribution of Student Performance metric, grouped by Attendence")
            st.pyplot(fig)
            
        elif genre == "Scatter":
            fig = sns.pairplot(df[prf], kind='hist',hue='attend',)
            st.subheader("Pairwise scatter plot of happiness metrics")
            st.pyplot(fig)

        elif genre == "Violin & Boxplot":
            fig, ax = plt.subplots(1,2)
            sns.violinplot(df[prf].groupby('attend').mean(),ax=ax[0])
            sns.boxenplot(df[prf].groupby('attend').mean(),ax=ax[1])
            st.subheader("Violin and Boxenplots")
            st.pyplot(fig)

    elif opt == "Happiness":
        st.write("Happiness attributes: ",hap)
        genre = st.radio(
            "Choose the type of plot",
            ["KDE & Hist", "Groupby", "Scatter", "Violin & Boxplot"],
            captions = ["Density/Distribution", "Groupby various categorical attributes","Pairwise scatter", "Outlier visualisation"])
        if genre == "KDE & Hist":
            fig, ax = plt.subplots()
            lo = df[hap].drop('attd_impc',axis=1)
            lo = (lo - lo.mean())/lo.std()
            sns.kdeplot(lo, ax=ax)
            st.subheader("KDE for happiness metrics")
            st.pyplot(fig)

        elif genre == "Groupby":
            fig, ax = plt.subplots()
            
            df[hap].groupby('attd_impc').mean().plot(kind='barh', subplots=False,ax=ax)
            st.subheader("Barplot grouped by attendence impact")
            st.pyplot(fig)

        elif genre == "Scatter":
            fig = sns.pairplot(df[hap], kind='hist',hue='attd_impc',)
            st.subheader("Pairwise scatter plot of happiness metrics")
            st.pyplot(fig)

        elif genre == "Violin & Boxplot":
            fig, ax = plt.subplots(1,2)
            plt.xticks(rotation=90)
            sns.violinplot(df[hap],ax=ax[0])
            ax[0].tick_params(axis='x', labelrotation = 90)

            plt.xticks(rotation=90)
            sns.boxenplot(df[hap],ax=ax[1])
            st.subheader("Outlier Detection via box and violin plots")
            st.pyplot(fig)

     # Correlation Analysis
    st.header("Correlation Analysis")
    optio = st.selectbox("Select the correlation matrix among: ", ['Performance', 'Happiness', 'All'])
    if optio == 'Performance':
        fig, ax = plt.subplots()
        sns.heatmap(df[prf].drop('attend', axis=1).corr(),ax=ax)
        st.subheader("Correlation matrix of performance metrics")
        st.pyplot(fig)

    elif optio == 'Happiness':
        fig, ax = plt.subplots()
        sns.heatmap(df[hap].drop('attd_impc', axis=1).corr(),ax=ax)
        st.subheader("Correlation matrix of happiness metrics")

        st.pyplot(fig)

    elif optio == 'All':
        fig, ax = plt.subplots()
        sns.heatmap(df[num].corr(),ax=ax)
        st.subheader("Correlation matrix of all metrics")

        st.pyplot(fig)



    # Regression Analysis
    st.header("Regression analysis to check for dependency of happiness to performance")
    st.write("Here we will aggregate all the performance and happiness metrics to continuous float. This will help us model a dependency relationship among them using Linear Regression")

    x = pd.concat([df[hap].drop('attd_impc', axis=1), df[ovhap].drop('hap_fact', axis=1)], axis=1).mean(axis=1)
    y = (2 * df[prf].gpa + 2 * df[prf].stud_hb + df[prf].stud_hr) / 5

    # Convert NumPy arrays to Pandas Series
    x = pd.Series(x)
    y = pd.Series(y)

    # Combine the Series into a DataFrame
    data = pd.concat([x, y], axis=1)
    st.dataframe(data)

    slid = st.slider("Enter test size", min_value=0.0, max_value=1.0, value=0.2, step=0.05)

    xtr, xte, ytr, yte = ttt(x.values.reshape(-1, 1), y.values.reshape(-1, 1), test_size=slid)

    lr = LinearRegression()

    lr.fit(xtr, ytr)
    st.write(f'The R-square score is {lr.score(xte, yte)}')

    st.write(f"The mean rating of performance is {float(lr.intercept_)} and if happiness increases by one unit, performance increases by {float(lr.coef_)} units.")

    # Scatter plot of the regression line
    st.subheader("Visualising Linear Regression")
    fig, ax = plt.subplots()
    sns.scatterplot(x=xte.reshape(1, -1)[0], y=yte.reshape(1, -1)[0], color='r',ax=ax)
    sns.scatterplot(x=xte.reshape(1, -1)[0], y=lr.predict(xte).reshape(1, -1)[0], color='b',ax=ax)
    st.pyplot(fig)

    #Lasso Regression
    st.subheader("Decision tree")

    x = pd.concat([df[hap].drop('attd_impc', axis=1), df[ovhap].drop('hap_fact', axis=1)], axis=1)
    st.subheader("Features")
    st.dataframe(x)

    xtr, xte, ytr, yte = ttt(x.values, y.values.reshape(-1, 1), test_size=slid)
    
    reg = dt()

    reg.fit(xtr, ytr)

    st.write(f'The R-square score for decision tree is {reg.score(xte, yte)}')

    st.subheader("Feature importance")
    val ={k:i for k,i in zip(x.columns,reg.feature_importances_)}
    val = pd.Series(val).sort_values(ascending=False)
    st.write(val)

    st.subheader("Visualising fit")
    fig, ax = plt.subplots()
    sns.scatterplot(x=yte.reshape(1, -1)[0], y=reg.predict(xte).reshape(1, -1)[0], color='b',ax=ax)
    st.pyplot(fig)
    
    st.write("THERE IS CORRELATION!!")
    
    
    
    
