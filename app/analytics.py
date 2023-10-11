# analytics.py
import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split as ttt
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pymongo

# Connect to MongoDB
def anal(collection):

    df = pd.DataFrame(list(collection.find()))
    st.title("Analytics")

    df = df.set_index("_id")

    # COLUMN SPLITTING
    num = [x for x in df if df[x].dtype == 'int64' and df[x].nunique() < 11]
    cat = [x for x in df if df[x].dtype == 'object' and len(str(df[x].iloc[0])) < 30]
    prf = ['gpa', 'stud_hb', 'stud_hr', 'attend']
    ovhap = ['hap_rate', 'hap_fact']
    hap = ['acad_impc', 'acad_press', 'acad_guilt', 'ch_guilt', 'gr_guilt', 'bal_contri', 'proc', 'wl_bal', 'extra_curr_hap', 'attd_impc']

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

    # Happiness Factors
    st.header("Happiness Factors")
    f, a = plt.subplots(1, 1)
    df[ovhap].groupby('hap_fact').mean().plot(kind='pie', subplots=True, ax=a)
    st.pyplot(f)

    # Year of study dist
    st.header("Year of Study Distribution")
    st.bar_chart(df['yo_stud'].value_counts())

    # Select either Happiness or Performance
    st.header("Select Happiness or Performance")
    opt = st.selectbox("Select which metric to expand upon: ", ['Happiness', 'Performance'])

    if opt == "Performance":
        st.write("Performance attributes: ", prf)
        genre = st.radio(
            "Choose the type of plot",
            ["KDE & Hist", "Groupby", "Scatter", "Violin & Boxplot"],
            format_func=lambda x: "Density/Distribution" if x == "KDE & Hist" else ("Groupby various categorical attributes" if x == "Groupby" else "Outlier visualisation")
        )
        if genre == "KDE & Hist":
            fig, ax = plt.subplots()
            sns.kdeplot(df[prf].groupby('attend').mean(), ax=ax)
            st.pyplot(fig)
            #fig.savefig("kdeplot.png")

        elif genre == "Groupby":
            fig, ax = plt.subplots()
            df[prf].groupby('attend').mean().plot(kind='barh', subplots=True)
            st.pyplot(fig)
            #fig.savefig("groupby.png")

        elif genre == "Scatter":
            fig, ax = plt.subplots()
            sns.pairplot(df[prf], hue='attend')
            st.pyplot(fig)
            #fig.savefig("pairplot.png")

        elif genre == "Violin & Boxplot":
            fig, ax = plt.subplots()
            sns.violinplot(df[prf].groupby('attend').mean())
            st.pyplot(fig)
            #fig.savefig("violinboxplot.png")
    elif opt == "Happiness":
        st.write("Happiness attributes: ", hap)
        genre = st.radio(
            "Choose the type of plot",
            ["KDE & Hist", "Groupby", "Scatter", "Violin & Boxplot"],
            format_func=lambda x: "Density/Distribution" if x == "KDE & Hist" else ("Groupby various categorical attributes" if x == "Groupby" else "Outlier visualisation")
        )
        if genre == "KDE & Hist":
            fig, ax = plt.subplots()
            sns.kdeplot(df[hap].groupby('attd_impc').mean(), ax=ax)
            st.pyplot(fig)

        elif genre == "Groupby":
            fig, ax = plt.subplots()
            df[hap].groupby('attd_impc').mean().plot(kind='barh', subplots=True)
            st.pyplot(fig)

        elif genre == "Scatter":
            sns.pairplot(df[hap], hue='attd_impc')
            st.pyplot()
            

        elif genre == "Violin & Boxplot":
            fig, ax = plt.subplots()
            sns.violinplot(df[hap].groupby('attd_impc').mean())
            st.pyplot(fig)

    # Correlation Analysis
    st.header("Correlation Analysis")
    optio = st.selectbox("Select the correlation matrix among: ", ['Performance', 'Happiness', 'All'])
    if optio == 'Performance':
        fig, ax = plt.subplots()
        sns.heatmap(df[prf].drop('attend', axis=1).corr())
        st.pyplot(fig)

    elif optio == 'Happiness':
        fig, ax = plt.subplots()
        sns.heatmap(df[hap].drop('attd_impc', axis=1).corr())
        st.pyplot(fig)

    elif optio == 'All':
        fig, ax = plt.subplots()
        sns.heatmap(df[num].corr())
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
    fig, ax = plt.subplots()
    sns.scatterplot(x=xte.reshape(1, -1)[0], y=yte.reshape(1, -1)[0], color='r')
    st.pyplot(fig)

    fig, ax = plt.subplots()
    sns.scatterplot(x=xte.reshape(1, -1)[0], y=lr.predict(xte).reshape(1, -1)[0], color='b')



