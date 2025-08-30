import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def plot_count(data):
    sns.countplot(x='ACLARADO', data=data)
    plt.title('ACLARADO')
    plt.title("count of clarified cases")
    plt.xlabel("ACLARADO")
    plt.ylabel("count")
    plt.show()

def plot_victim_SEXO(df):
    sex_counts = df['SEXO'].value_counts()
    sns.barplot(x=sex_counts.index, y=sex_counts.values, palette="Set2")
    plt.title("count of cases by gender")
    plt.xlabel("gender: 0 male, 1 female")
    plt.ylabel("number of victims")
    plt.show()

def plot_count_by_SEXO(data):
    sns.countplot(x='SEXO', hue='ACLARADO', data=data)
    plt.title('count of clarified cases by gender')
    plt.xlabel("gender")
    plt.ylabel("reports")
    plt.show()

def plot_count_by_EDADCALC(data:pd.DataFrame):
    data_plot = data[['EDADCALC', 'ACLARADO']].copy()
    data_plot['EDADCALC'] = pd.to_numeric(data_plot['EDADCALC'], errors='coerce')
    data_plot['ACLARADO'] = pd.to_numeric(data_plot['ACLARADO'], errors='coerce')
    data_plot = data_plot.dropna()
    data_plot = data_plot.sort_values(by='EDADCALC')
    bins = list(range(0, int(data_plot['EDADCALC'].max()) + 5, 1))
    sns.histplot(data=data_plot, x='EDADCALC', bins=bins, hue='ACLARADO', multiple='stack')
    plt.title('count of clarified cases by age')
    plt.xlabel("age")
    plt.ylabel("reports")
    plt.show()

def plot_cases_per_hour(data):
    data['HORA'] = pd.to_numeric(data['HORA'], errors='coerce')
    Perhour = data['HORA'].value_counts().sort_index()
    sns.lineplot(x=Perhour.index, y=Perhour.values, marker="o")
    plt.title("cases per hour")
    plt.xlabel("hour")
    plt.ylabel("reports")
    plt.grid(alpha=0.3)
    plt.show()

def plot_count_by_HORA(data):
    sns.countplot(x='HORA', hue='ACLARADO', data=data)
    plt.title('count of clarified cases by hour')
    plt.xlabel("hour")
    plt.ylabel("reports")
    plt.show()

def plot_antecedentes_aclarado(data):
    cross_tab = pd.crosstab(data['ANTECEDENTES'], data['ACLARADO'])
    cross_tab.plot(kind='bar', stacked=True, colormap='coolwarm')
    plt.title("antecedentes y aclarado")
    plt.xlabel("antecedentes")
    plt.ylabel("reports")
    plt.legend(title="aclarado (yes 1, no 0)")
    plt.show()