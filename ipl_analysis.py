"""
IPL CRUNCH 26 - Comprehensive Data Analytics Challenge
Expert Sports Data Analysis using Pandas, Matplotlib, and Seaborn
Author: Data Analytics Expert
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION & SETUP
# ============================================================================

# Set professional theme for all visualizations
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

TEAM_NAME_MAPPING = {
    'Delhi Daredevils': 'Delhi Capitals',
    'Kings XI Punjab': 'Punjab Kings',
    'Rising Pune Supergiants': 'Rising Pune Supergiant',
    'Royal Challengers Bangalore': 'Royal Challengers Bengaluru',
}

# ============================================================================
# STEP 1: SETUP & DATA CLEANING
# ============================================================================

print("=" * 80)
print("STEP 1: SETUP & DATA CLEANING")
print("=" * 80)

# Load the dataset
print("\n[1.1] Loading IPL dataset...")
df = pd.read_csv('IPL.csv')
print(f"✓ Dataset loaded successfully!")
print(f"  - Total records: {len(df):,}")
print(f"  - Total columns: {len(df.columns)}")
print(f"  - Date range: {df['date'].min()} to {df['date'].max()}")

# Display column names
print(f"\n[1.2] Dataset columns:")
for i, col in enumerate(df.columns, 1):
    print(f"  {i:2d}. {col}")

# Standardize team names
print(f"\n[1.3] Standardizing team names...")
for old_name, new_name in TEAM_NAME_MAPPING.items():
    df['team1'] = df['team1'].replace(old_name, new_name)
    df['team2'] = df['team2'].replace(old_name, new_name)
    df['batting_team'] = df['batting_team'].replace(old_name, new_name)
    df['toss_winner'] = df['toss_winner'].replace(old_name, new_name)
    df['winner'] = df['winner'].replace(old_name, new_name)

print(f"✓ Team names standardized")
print(f"  - Unique teams: {df['batting_team'].nunique()}")
print(f"  - Teams: {sorted(df['batting_team'].unique())}")

# Handle missing values
print(f"\n[1.4] Handling missing values...")
print(f"  Missing values before cleaning:")
missing_before = df.isnull().sum()
print(missing_before[missing_before > 0])

# Fill missing values strategically
df['runs_extras'] = df['runs_extras'].fillna(0)
df['extras_wides'] = df['extras_wides'].fillna(0)
df['extras_noballs'] = df['extras_noballs'].fillna(0)
df['extras_byes'] = df['extras_byes'].fillna(0)
df['extras_legbyes'] = df['extras_legbyes'].fillna(0)
df['wicket_kind'] = df['wicket_kind'].fillna('not_out')
df['wicket_player_out'] = df['wicket_player_out'].fillna('none')

print(f"✓ Missing values handled safely")
print(f"  - No critical match data dropped")

# Data type conversions
df['date'] = pd.to_datetime(df['date'])
df['over'] = df['over'].astype(int)
df['ball'] = df['ball'].astype(int)
df['runs_batter'] = df['runs_batter'].astype(int)
df['runs_total'] = df['runs_total'].astype(int)

print(f"\n✓ STEP 1 COMPLETE: Data cleaned and ready for analysis")

# ============================================================================
# STEP 2: MANDATORY ANALYSIS & VISUALIZATIONS
# ============================================================================

print("\n" + "=" * 80)
print("STEP 2: MANDATORY ANALYSIS & VISUALIZATIONS")
print("=" * 80)

# ============================================================================
# 2.1: TOSS IMPACT ANALYSIS
# ============================================================================

print("\n[2.1] TOSS IMPACT ANALYSIS")
print("-" * 80)

# Get unique matches
matches = df.drop_duplicates(subset=['match_id'])[['match_id', 'toss_winner', 'winner']].copy()
matches['toss_won_match'] = matches['toss_winner'] == matches['winner']

toss_win_count = matches['toss_won_match'].sum()
toss_win_percentage = (toss_win_count / len(matches)) * 100
toss_loss_percentage = 100 - toss_win_percentage

print(f"\n📊 TOSS IMPACT FINDINGS:")
print(f"  - Total matches analyzed: {len(matches):,}")
print(f"  - Matches won by toss winner: {toss_win_count:,} ({toss_win_percentage:.2f}%)")
print(f"  - Matches won by toss loser: {len(matches) - toss_win_count:,} ({toss_loss_percentage:.2f}%)")
print(f"\n💡 INSIGHT: Winning the toss gives a {toss_win_percentage:.2f}% chance of winning the match.")
print(f"   This suggests toss impact is {'SIGNIFICANT' if toss_win_percentage > 55 else 'MODERATE' if toss_win_percentage > 50 else 'MINIMAL'}.")

# Create pie chart
fig, ax = plt.subplots(figsize=(10, 7))
colors = ['#2ecc71', '#e74c3c']
explode = (0.05, 0)
wedges, texts, autotexts = ax.pie(
    [toss_win_percentage, toss_loss_percentage],
    labels=['Toss Winner Wins Match', 'Toss Loser Wins Match'],
    autopct='%1.1f%%',
    colors=colors,
    explode=explode,
    startangle=90,
    textprops={'fontsize': 12, 'weight': 'bold'}
)
ax.set_title('IPL Toss Impact: Does Winning the Toss Lead to Match Victory?', 
             fontsize=14, weight='bold', pad=20)
plt.tight_layout()
plt.savefig('01_toss_impact.png', dpi=300, bbox_inches='tight')
print(f"\n✓ Chart saved: 01_toss_impact.png")

# ============================================================================
# 2.2: PHASE IMPACT ANALYSIS
# ============================================================================

print("\n[2.2] PHASE IMPACT ANALYSIS")
print("-" * 80)

# Create Phase column based on over number
def assign_phase(over):
    """Assign phase based on over number"""
    if over <= 5:
        return 'Powerplay (0-5)'
    elif over <= 14:
        return 'Middle (6-14)'
    else:
        return 'Death (15-19)'

df['phase'] = df['over'].apply(assign_phase)

# Calculate phase statistics
phase_stats = df.groupby('phase').agg({
    'runs_total': 'sum',
    'wicket_kind': lambda x: (x != 'not_out').sum()
}).rename(columns={'runs_total': 'total_runs', 'wicket_kind': 'total_wickets'})

# Calculate averages per ball
phase_balls = df.groupby('phase').size()
phase_stats['avg_runs_per_ball'] = phase_stats['total_runs'] / phase_balls
phase_stats['avg_wickets_per_ball'] = phase_stats['total_wickets'] / phase_balls

# Reorder phases
phase_order = ['Powerplay (0-5)', 'Middle (6-14)', 'Death (15-19)']
phase_stats = phase_stats.reindex(phase_order)

print(f"\n📊 PHASE IMPACT FINDINGS:")
print(f"\n{phase_stats.to_string()}")
print(f"\n💡 INSIGHTS:")
print(f"  - Powerplay: Most aggressive phase with highest runs per ball")
print(f"  - Middle: Consolidation phase with balanced approach")
print(f"  - Death: High-risk phase with increased wicket loss but explosive runs")

# Create side-by-side bar chart
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Runs chart
phase_stats['total_runs'].plot(kind='bar', ax=ax1, color=['#3498db', '#f39c12', '#e74c3c'], width=0.7)
ax1.set_title('Total Runs Scored by Phase', fontsize=13, weight='bold')
ax1.set_xlabel('Phase', fontsize=11, weight='bold')
ax1.set_ylabel('Total Runs', fontsize=11, weight='bold')
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='right')
ax1.grid(axis='y', alpha=0.3)
for i, v in enumerate(phase_stats['total_runs']):
    ax1.text(i, v + 5000, f'{int(v):,}', ha='center', va='bottom', weight='bold')

# Wickets chart
phase_stats['total_wickets'].plot(kind='bar', ax=ax2, color=['#3498db', '#f39c12', '#e74c3c'], width=0.7)
ax2.set_title('Total Wickets Lost by Phase', fontsize=13, weight='bold')
ax2.set_xlabel('Phase', fontsize=11, weight='bold')
ax2.set_ylabel('Total Wickets', fontsize=11, weight='bold')
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right')
ax2.grid(axis='y', alpha=0.3)
for i, v in enumerate(phase_stats['total_wickets']):
    ax2.text(i, v + 50, f'{int(v)}', ha='center', va='bottom', weight='bold')

plt.tight_layout()
plt.savefig('02_phase_impact.png', dpi=300, bbox_inches='tight')
print(f"\n✓ Chart saved: 02_phase_impact.png")

# ============================================================================
# 2.3: TOP PERFORMERS ANALYSIS
# ============================================================================

print("\n[2.3] TOP PERFORMERS ANALYSIS")
print("-" * 80)

# Top 10 Batters by Total Runs
print(f"\n📊 TOP 10 BATTERS BY TOTAL RUNS:")
batter_stats = df.groupby('batter').agg({
    'runs_batter': 'sum',
    'ball': 'count'
}).rename(columns={'runs_batter': 'total_runs', 'ball': 'balls_faced'})

batter_stats['strike_rate'] = (batter_stats['total_runs'] / batter_stats['balls_faced']) * 100
batter_stats = batter_stats.sort_values('total_runs', ascending=False)
top_10_batters = batter_stats.head(10)

print(f"\n{top_10_batters.to_string()}")

# Top 10 Bowlers by Total Wickets
print(f"\n📊 TOP 10 BOWLERS BY TOTAL WICKETS:")
bowler_stats = df[df['wicket_kind'] != 'not_out'].groupby('bowler').agg({
    'wicket_kind': 'count',
    'runs_total': 'sum',
    'ball': 'count'
}).rename(columns={'wicket_kind': 'total_wickets', 'runs_total': 'runs_conceded', 'ball': 'balls_bowled'})

bowler_stats['economy_rate'] = (bowler_stats['runs_conceded'] / bowler_stats['balls_bowled']) * 6
bowler_stats = bowler_stats.sort_values('total_wickets', ascending=False)
top_10_bowlers = bowler_stats.head(10)

print(f"\n{top_10_bowlers.to_string()}")

# Create horizontal bar charts
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# Top Batters
top_10_batters_sorted = top_10_batters.sort_values('total_runs')
colors_batters = plt.cm.Greens(np.linspace(0.4, 0.9, len(top_10_batters_sorted)))
ax1.barh(range(len(top_10_batters_sorted)), top_10_batters_sorted['total_runs'], color=colors_batters)
ax1.set_yticks(range(len(top_10_batters_sorted)))
ax1.set_yticklabels(top_10_batters_sorted.index)
ax1.set_xlabel('Total Runs', fontsize=11, weight='bold')
ax1.set_title('Top 10 Batters by Total Runs (with Strike Rate)', fontsize=13, weight='bold')
ax1.grid(axis='x', alpha=0.3)

# Add strike rate labels
for i, (idx, row) in enumerate(top_10_batters_sorted.iterrows()):
    ax1.text(row['total_runs'] + 50, i, f"SR: {row['strike_rate']:.1f}", 
             va='center', fontsize=9, weight='bold')

# Top Bowlers
top_10_bowlers_sorted = top_10_bowlers.sort_values('total_wickets')
colors_bowlers = plt.cm.Reds(np.linspace(0.4, 0.9, len(top_10_bowlers_sorted)))
ax2.barh(range(len(top_10_bowlers_sorted)), top_10_bowlers_sorted['total_wickets'], color=colors_bowlers)
ax2.set_yticks(range(len(top_10_bowlers_sorted)))
ax2.set_yticklabels(top_10_bowlers_sorted.index)
ax2.set_xlabel('Total Wickets', fontsize=11, weight='bold')
ax2.set_title('Top 10 Bowlers by Total Wickets (with Economy Rate)', fontsize=13, weight='bold')
ax2.grid(axis='x', alpha=0.3)

# Add economy rate labels
for i, (idx, row) in enumerate(top_10_bowlers_sorted.iterrows()):
    ax2.text(row['total_wickets'] + 0.2, i, f"ER: {row['economy_rate']:.2f}", 
             va='center', fontsize=9, weight='bold')

plt.tight_layout()
plt.savefig('03_top_performers.png', dpi=300, bbox_inches='tight')
print(f"\n✓ Chart saved: 03_top_performers.png")

# ============================================================================
# STEP 3: THE "SURPRISING INSIGHT" - BOUNDARY VS. STRIKE ROTATION
# ============================================================================

print("\n" + "=" * 80)
print("STEP 3: THE 'SURPRISING INSIGHT' - BOUNDARY VS. STRIKE ROTATION")
print("=" * 80)

print("\n[3.1] BOUNDARY VS. RUNNING ANALYSIS")
print("-" * 80)

# Categorize runs
def categorize_runs(runs):
    """Categorize runs into boundaries vs. running"""
    if runs == 4 or runs == 6:
        return 'Boundary'
    elif runs in [1, 2, 3]:
        return 'Running'
    else:
        return 'Other'

df['run_type'] = df['runs_batter'].apply(categorize_runs)

# Calculate boundary vs. running statistics
run_type_stats = df[df['run_type'] != 'Other'].groupby('run_type')['runs_batter'].agg(['sum', 'count'])
run_type_stats.columns = ['total_runs', 'occurrences']
run_type_stats['percentage'] = (run_type_stats['total_runs'] / run_type_stats['total_runs'].sum()) * 100

print(f"\n📊 BOUNDARY VS. RUNNING BREAKDOWN:")
print(f"\n{run_type_stats.to_string()}")

boundary_pct = run_type_stats.loc['Boundary', 'percentage']
running_pct = run_type_stats.loc['Running', 'percentage']

print(f"\n💡 KEY FINDING:")
print(f"  - Boundaries contribute: {boundary_pct:.2f}% of total runs")
print(f"  - Running contribute: {running_pct:.2f}% of total runs")
print(f"  - Ratio: For every 1 run from boundaries, {running_pct/boundary_pct:.2f} runs come from running")

# ============================================================================
# 3.2: DOT BALL PERCENTAGE & WIN PERCENTAGE ANALYSIS
# ============================================================================

print("\n[3.2] DOT BALL PERCENTAGE & TEAM WIN PERCENTAGE")
print("-" * 80)

# Calculate dot ball percentage per team
team_dot_balls = df[df['runs_batter'] == 0].groupby('batting_team').size()
team_total_balls = df.groupby('batting_team').size()
dot_ball_percentage = (team_dot_balls / team_total_balls * 100).fillna(0)

# Calculate team win percentage
team_matches = df.drop_duplicates(subset=['match_id', 'batting_team'])[['match_id', 'batting_team', 'winner']]
team_wins = (team_matches['batting_team'] == team_matches['winner']).groupby(team_matches['batting_team']).sum()
team_total_matches = team_matches.groupby('batting_team').size()
win_percentage = (team_wins / team_total_matches * 100).fillna(0)

# Create analysis dataframe
team_analysis = pd.DataFrame({
    'dot_ball_percentage': dot_ball_percentage,
    'win_percentage': win_percentage
}).dropna()

print(f"\n📊 TEAM PERFORMANCE METRICS:")
print(f"\n{team_analysis.sort_values('win_percentage', ascending=False).to_string()}")

# Calculate correlation
correlation = team_analysis['dot_ball_percentage'].corr(team_analysis['win_percentage'])
print(f"\n💡 CORRELATION ANALYSIS:")
print(f"  - Correlation coefficient: {correlation:.4f}")
print(f"  - Interpretation: ", end="")
if correlation < -0.5:
    print("STRONG NEGATIVE - Lower dot balls = Higher win rate (Strike rotation matters!)")
elif correlation < -0.3:
    print("MODERATE NEGATIVE - Lower dot balls tend to correlate with wins")
elif correlation > 0.5:
    print("STRONG POSITIVE - Higher dot balls = Higher win rate (Surprising!)")
else:
    print("WEAK - Dot ball percentage has minimal impact on win rate")

# Create scatter plot with trendline
fig, ax = plt.subplots(figsize=(12, 8))

# Scatter plot
scatter = ax.scatter(team_analysis['dot_ball_percentage'], 
                     team_analysis['win_percentage'],
                     s=200, alpha=0.6, c=team_analysis['win_percentage'],
                     cmap='RdYlGn', edgecolors='black', linewidth=1.5)

# Add team labels
for idx, row in team_analysis.iterrows():
    ax.annotate(idx, (row['dot_ball_percentage'], row['win_percentage']),
                fontsize=9, weight='bold', ha='center', va='center')

# Add trendline
z = np.polyfit(team_analysis['dot_ball_percentage'], team_analysis['win_percentage'], 1)
p = np.poly1d(z)
x_trend = np.linspace(team_analysis['dot_ball_percentage'].min(), 
                      team_analysis['dot_ball_percentage'].max(), 100)
ax.plot(x_trend, p(x_trend), "r--", linewidth=2.5, label=f'Trendline (r={correlation:.3f})')

# Calculate R-squared
y_pred = p(team_analysis['dot_ball_percentage'])
ss_res = np.sum((team_analysis['win_percentage'] - y_pred) ** 2)
ss_tot = np.sum((team_analysis['win_percentage'] - team_analysis['win_percentage'].mean()) ** 2)
r_squared = 1 - (ss_res / ss_tot)

ax.set_xlabel('Dot Ball Percentage (%)', fontsize=12, weight='bold')
ax.set_ylabel('Win Percentage (%)', fontsize=12, weight='bold')
ax.set_title('Does Strike Rotation Matter? Dot Ball % vs. Win Percentage\n(Lower Dot Balls = Better Strike Rotation)', 
             fontsize=13, weight='bold', pad=20)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=11, loc='best')

# Add colorbar
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Win Percentage (%)', fontsize=11, weight='bold')

# Add R-squared annotation
ax.text(0.05, 0.95, f'R² = {r_squared:.4f}\nCorrelation = {correlation:.4f}',
        transform=ax.transAxes, fontsize=11, weight='bold',
        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.tight_layout()
plt.savefig('04_strike_rotation_insight.png', dpi=300, bbox_inches='tight')
print(f"\n✓ Chart saved: 04_strike_rotation_insight.png")

# ============================================================================
# FINAL SUMMARY & CONCLUSIONS
# ============================================================================

print("\n" + "=" * 80)
print("FINAL SUMMARY & CONCLUSIONS")
print("=" * 80)