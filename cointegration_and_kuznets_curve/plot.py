import matplotlib.pyplot as plt
import seaborn as sns

def plot_variable(df,name):
    plt.plot(df[name])
    plt.show()

def plot_k_curve(df, turning_point):
    sns.set_theme(style='whitegrid')
    plt.figure(figsize=(10, 6))
    sns.regplot(
        x='realgdp', y='totalghg', data=df,
        order=2,
        ci=None,
        scatter_kws={'s': 20,'color': "#4A7200", 'alpha': 0.9},
        line_kws={'color': "#5fa834", 'linewidth': 3}
    )

    #turning_point = 10.019

    plt.axvline(turning_point, color='red', linestyle='--', label='Turning Point')
    plt.title('Environmental Kuznets Curve (EKC) in Uruguay (1984-2014)')
    plt.xlabel('Log of Real GDP per Capita')
    plt.ylabel('GHG Emissions per Capita')
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_irf(model_result,significance):
    irf = model_result.irf(10)
    irf.plot(orth=True, signif=significance)
    plt.show()