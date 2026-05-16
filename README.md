# IPL Data Analytics 🏏

This project is a comprehensive data analysis of the Indian Premier League (IPL) ball-by-ball dataset (spanning from 2008 to 2026). The goal is to clean the dataset, uncover statistical insights, discover a "secret winning strategy".

## 🚀 Project Overview

The project is broken down into four distinct phases:

### Phase 1: Organizing the Mess (Data Cleaning)
Historical sports data often contains inconsistencies due to franchise name changes. We built a robust mapping system to standardize the following active franchises while keeping historically distinct temporary teams (like Gujarat Lions and Pune Warriors) separate:
- **Delhi Daredevils** ➔ **Delhi Capitals**
- **Kings XI Punjab** ➔ **Punjab Kings**
- **Royal Challengers Bangalore** ➔ **Royal Challengers Bengaluru**
- **Rising Pune Supergiants** ➔ **Rising Pune Supergiant** (consolidating a pluralization typo)

### Phase 2: Answering the Obvious Questions
We conducted exploratory data analysis on the 2.8+ lakh deliveries to answer three mandatory questions:
1. **The Toss**: Does winning the coin toss actually matter? (Calculated win percentage based on toss outcome).
2. **The Phases**: Is it more important to score big in the Powerplay (first 6 overs) or the Death Overs (last 5)? (Analyzed run rates and wicket drops across three match phases).
3. **The Best Players**: Who are the MVP batters and bowlers? (Ranked top 10 by runs/strike-rate and wickets/economy).

### Phase 3: Finding the Secret Insight
While boundaries (fours and sixes) are entertaining, we wanted to find a deeper strategy. We hypothesized that **Strike Rotation** is actually more critical.
- We analyzed the **Dot Ball Percentage** for each franchise.
- We compared it against their overall **Win Percentage**.
- **The Result**: We found a strong correlation proving that teams that waste fewer balls (lower dot ball percentage) consistently win more matches. Strike rotation is a hidden key to IPL success!

### Phase 4: Telling the Story (Visualization & Presentation)

## 🎯 Interactive Dashboard

We built an advanced interactive dashboard that brings the data to life! The dashboard features:

✨ **Live Analytics Dashboard** - Deployed on Vercel
- **URL**: [https://ipl-neon-pi.vercel.app/]
- **Season-by-Season Analysis**: Filter and analyze any IPL season
- **Key Metrics**:
  - Tournament Winner
  - Total Matches Played
  - Total Runs Scored
  - Orange Cap Holder (Highest Scorer)
- **Advanced Visualizations**:
  - Runs Evolution Across Seasons (Line Chart)
  - Sixes Hit Per Season (Bar Chart)
  - Toss Impact Analysis (Doughnut Chart)
  - Phase Impact - Powerplay vs Middle vs Death (Dual-axis Bar Chart)
  - Top 10 Batters (Bar Chart)
  - Top 10 Bowlers (Bar Chart)
  - Boundary vs Strike Rotation Analysis
  - Dot Ball % vs Win Rate (Scatter Plot)

The dashboard is **fully functional** and processes 280,000+ ball-by-ball records in real-time using JavaScript with Chart.js for beautiful visualizations.

## 📂 File Structure & Generated Artifacts

### Scripts
- `ipl_analysis.py`: The core data engine. Cleans the data, runs the math, and generates the charts.

### Web Applications
- `index.html`: Interactive dashboard application (deployed on Vercel)

### Outputs
- `01_toss_impact.png`: A pie chart showing the impact of winning the toss.
- `02_phase_impact.png`: A bar chart comparing total runs and wickets across the Powerplay, Middle, and Death overs.
- `03_top_performers.png`: Horizontal bar charts ranking the top 10 historical batters and bowlers.
- `04_strike_rotation_insight.png`: A scatter plot with a trendline proving the correlation between Dot Ball % and Win %.

