import matplotlib.pyplot as plt

def plot_simulation_results(history: dict):
    periods = range(len(history['commons']))
    
    plt.figure(figsize=(10, 6))
    plt.plot(periods, history['commons'], label='Informational Commons ($I_t$)', color='crimson', linewidth=2)
    plt.plot(periods, history['avg_disclosure'], label='Average Disclosure ($d$)', color='royalblue', linewidth=2)
    plt.plot(periods, history['avg_acquisition'], label='Acquisition Rate', color='forestgreen', linestyle='--', linewidth=1.5)
    
    plt.title('Systemic Market Degradation: The Decoupled Compounding Commons', fontsize=12, fontweight='bold')
    plt.xlabel('Time Periods', fontsize=10)
    plt.ylabel('Normalized Metric Level', fontsize=10)
    plt.legend(frameon=True, facecolor='white', edgecolor='none')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.show()
