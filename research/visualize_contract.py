import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from contract_architect import architect_personalized_contract
from micro_encoder import process_microstructure_data
from behavioral_encode import process_behavioral_profiles

def generate_architect_plot():
    print("Generating data for visualization.")
    market_df = process_microstructure_data("../data/optiver/book_train.parquet/stock_id=0")
    user_df = process_behavioral_profiles("../data/american_consumer_survey/ss15pusb/ss15pusb.csv")
    
    # Simulating contracts for 500000 random users
    results = []
    sample_market = market_df.iloc[0]
    
    for _, user in user_df.head(500000).iterrows():
        contract = architect_personalized_contract(user, sample_market)
        results.append(contract)
    
    plot_df = pd.DataFrame(results)

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Graph 1: Distribution of Personalization
    sns.histplot(data=plot_df, x='User_Bias', bins=15, ax=axes[0], kde=True, color='teal')
    axes[0].set_title("Distribution of Behavioral Bias in Population")
    axes[0].set_xlabel("Bias Score")

    # ==========================================
    # Graph 2: Microstructure vs Hedge (UPDATED)
    # ==========================================
    market_sim = []
    vols = np.linspace(0.001, 0.01, 50) # Simulated market stress
    
    # Extract all user biases to apply logic to all 500,000 users simultaneously
    biases = plot_df['User_Bias'].values
    
    # Apply your engine's logic to the whole population array
    multipliers = np.where(biases > 0.4, 1.5, 
                  np.where(biases < -0.4, 0.8, 1.0))
    
    for v in vols:
        # Calculate the hedges for EVERY user at this volatility level
        all_hedges = (v * multipliers) * 100
        market_sim.append({
            'Volatility': v,
            'Average_Hedge': np.mean(all_hedges),
            'Max_Hedge': np.max(all_hedges), # The most aggressive engine adjustment
            'Min_Hedge': np.min(all_hedges)  # The most defensive engine adjustment
        })
    
    sim_df = pd.DataFrame(market_sim)
    
    # Plot the Average as the solid red line
    sns.lineplot(data=sim_df, x='Volatility', y='Average_Hedge', ax=axes[1], color='red', label='Population Average')
    
    # Shade the area between the Min and Max to show the entire population's spread
    axes[1].fill_between(sim_df['Volatility'], sim_df['Min_Hedge'], sim_df['Max_Hedge'], color='red', alpha=0.2, label='Population Range')

    axes[1].set_title(f"Contract Sensitivity to Market Micro-Vol)")
    axes[1].set_xlabel("Realized Volatility")
    axes[1].set_ylabel("Hedge Ratio (%)")
    axes[1].legend(loc='upper left')
    
    plt.tight_layout()
    plt.savefig("../outcomes/architect_research_exhibit3.png")
    print("Research Exhibit saved!")

    # Create the Plot
    plt.figure(figsize=(12, 6))
    sns.set_style("whitegrid")
    
    # Graph 3: Scatter plot: Age vs Hedge Ratio, colored by Bias Type
    plot = sns.scatterplot(
        data=plot_df, 
        x='User_Age', 
        y='Final_Hedge_Ratio', 
        hue='Adjustment_Type',
        palette='viridis',
        s=100
    )
    
    plt.title("The Architect:Personalized Hedge Ratios based on Life-History Bias", fontsize=15)
    plt.xlabel("User Age (Years)", fontsize=12)
    plt.ylabel("Hedge Ratio (Protection Level %)", fontsize=12)
    plt.legend(title="Behavioral Correction", bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    plt.savefig("../outcomes/architect_results3.png")
    print("Visualization saved to ../outcomes/architect_results3.png")

    # Create ranges for the Matrix
    bias_range = np.linspace(-1, 1, 20)  # Frugal to Overconfident
    vol_range = np.linspace(0.001, 0.01, 20) # Low to High Market Vol
    
    matrix_data = []
    for b in bias_range:
        row = []
        for v in vol_range:
            # Replicating Architect Logic: Base Risk * Bias Multiplier
            multiplier = 1.5 if b > 0.4 else (0.8 if b < -0.4 else 1.0)
            hedge = (v * multiplier) * 100
            row.append(hedge)
        matrix_data.append(row)

    # Plotting the Heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        matrix_data, 
        xticklabels=np.round(vol_range, 4), 
        yticklabels=np.round(bias_range, 2),
        cmap="YlOrRd",
        annot=False
    )
    plt.title("The Architect Matching Matrix: Hedge Ratio (%)")
    plt.xlabel("Market Micro-Volatility")
    plt.ylabel("User Behavioral Bias")
    
    plt.savefig("../outcomes/matching_matrix3.png")
    print("Matching Matrix Heatmap saved to ../outcomes/matching_matrix3.png")


if __name__ == "__main__":
    generate_architect_plot()