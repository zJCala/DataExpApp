import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
@st.cache_data
def load_data():
    data = pd.read_csv('nba_games.csv')
    data['game_date'] = pd.to_datetime(data['game_date'])  # Convert game_date to datetime
    return data

# Load data
nba_data = load_data()

# Sidebar for Navigation
st.sidebar.title("NBA Games Exploration")
selected_section = st.sidebar.radio("Navigate to:", options=["Introduction", "Visualizations", "Conclusion"])

# Filter Options
season_filter = st.sidebar.selectbox("Select Season:", options=nba_data['season'].unique())
win_filter = st.sidebar.radio("Win/Loss Filter:", options=["All", "Wins", "Losses"])

# Filter data based on selections
filtered_data = nba_data[nba_data['season'] == season_filter]
if win_filter == "Wins":
    filtered_data = filtered_data[filtered_data['team_win'] == 1]
elif win_filter == "Losses":
    filtered_data = filtered_data[filtered_data['team_win'] == 0]

# Introduction Section
if selected_section == "Introduction":
    st.title("NBA Games Data Exploration Report")
    st.header("Introduction")
    st.write("""
    This report provides an in-depth exploration of the Los Angeles Lakers' game data for the selected season, 
    sourced from official NBA statistics. The objective of this analysis is to uncover key trends, 
    performance metrics, and insights that can inform strategic decisions and enhance understanding of the team's performance.
    
    The dataset encompasses various performance metrics including:
    - Points scored per game
    - Field goal (FG), free throw (FT), and three-point (3PT) shooting percentages
    - Assists and rebounds statistics
    - Win-loss outcomes

    Through visualizations and statistical analysis, we aim to highlight significant patterns in the Lakers' performance over the season.
    """)

    # Display key metrics
    st.header("Key Performance Metrics")
    st.metric("Total Games Played", len(filtered_data))
    st.metric("Total Wins", filtered_data['team_win'].sum())
    st.metric("Average Points Scored", round(filtered_data['team_points'].mean(), 2))
    st.metric("Average Field Goal Percentage", f"{round(filtered_data['team_fg_percentage'].mean() * 100, 2)}%")

# Visualizations Section
elif selected_section == "Visualizations":
    st.header("Visualizations")
    
    # Points Scored Over Time
    st.subheader("Points Scored Over Time")
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=filtered_data, x='game_date', y='team_points', marker='o', color='purple')
    plt.title('Points Scored by the Lakers Over the Selected Season')
    plt.xlabel('Game Date')
    plt.ylabel('Points Scored')
    plt.xticks(rotation=45)
    plt.grid()
    st.pyplot(plt)

    st.write("""
    This line chart illustrates the points scored by the Lakers throughout the selected season. 
    Notably, peaks in scoring can be observed during specific games, which may correlate with opponents, 
    player performances, or strategic adjustments made by the coaching staff.
    """)

    # Field Goal Percentage Distribution
    st.subheader("Field Goal Percentage Distribution")
    plt.figure(figsize=(10, 5))
    sns.histplot(filtered_data['team_fg_percentage'], bins=10, kde=True, color='orange')
    plt.title('Distribution of Field Goal Percentage')
    plt.xlabel('Field Goal Percentage')
    plt.ylabel('Frequency')
    plt.grid()
    st.pyplot(plt)

    st.write("""
    The histogram above shows the distribution of the Lakers' field goal percentages during the selected season. 
    The Kernel Density Estimate (KDE) overlay provides insight into the shooting efficiency across games.
    """)

    # Wins and Losses
    st.subheader("Wins and Losses in the Selected Season")
    win_count = filtered_data['team_win'].value_counts()
    plt.figure(figsize=(6, 4))
    sns.barplot(x=win_count.index, y=win_count.values, palette='pastel')
    plt.title('Wins and Losses in the Selected Season')
    plt.xlabel('Result (0 = Loss, 1 = Win)')
    plt.ylabel('Number of Games')
    plt.xticks(ticks=[0, 1], labels=['Loss', 'Win'])
    plt.grid()
    st.pyplot(plt)

    st.write("""
    The bar chart displays the Lakers' win-loss record for the selected season. 
    The results indicate a balanced performance; however, the number of losses suggests potential 
    areas for strategic improvement.
    """)

    # Average Points per Game
    st.subheader("Average Points per Game by Season")
    avg_points = nba_data.groupby('season')['team_points'].mean()
    plt.figure(figsize=(8, 5))
    avg_points.plot(kind='bar', color='skyblue')
    plt.title('Average Points per Game by Season')
    plt.xlabel('Season')
    plt.ylabel('Average Points')
    plt.grid()
    st.pyplot(plt)

    st.write("""
    This bar chart represents the average points scored by the Lakers per game during the selected season. 
    The average can serve as a benchmark for evaluating the team's scoring capabilities relative to other teams 
    in the league.
    """)

# Conclusion Section
elif selected_section == "Conclusion":
    st.header("Conclusion")
    st.write("""
    The exploration of the Lakers' game data for the selected season reveals several critical insights:
    1. **Scoring Variability**: The fluctuation in points scored highlights the inconsistency in offensive performance.
    2. **Shooting Efficiency**: The distribution of field goal percentages suggests that the Lakers maintained an average shooting efficiency.
    3. **Win-Loss Dynamics**: The win-loss data indicates that while the Lakers experienced a number of wins, 
       there is room for improvement in converting close games into wins.
    4. **Future Directions**: Further analysis is warranted, focusing on individual player contributions, 
       defensive metrics, and situational analysis to develop a more comprehensive understanding of the team's dynamics.
    """)
