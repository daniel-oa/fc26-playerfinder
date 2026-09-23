# FC26 PlayerFinder

A Streamlit web application for filtering and exploring FC 26 player data based on player attributes and preferences.

**Live App:** [FC26 PlayerFinder](https://fc26-playerfinder.streamlit.app/)

## Features

- Search players by name
- Filter by position
- Filter by age, overall, and potential
- Filter by player value in millions of euros
- Filter by league and club
- Filter by nationality and height
- Filter by weak foot and skill moves
- View filtered players in a sortable results table
- Reset all filters with one click
- Handle players with unavailable market values

## Dataset

This project uses the [**FC 26 (FIFA 26) Player Data**](https://www.kaggle.com/datasets/rovnez/fc-26-fifa-26-player-data) dataset by **Rovnez**, available on Kaggle.

The dataset is provided under the license specified by the dataset author. Please refer to the original Kaggle dataset page for the applicable licensing terms and attribution requirements.

The dataset is included in this repository for use by the application.

## Project Structure

```text
FC26/
├── app.py
├── FC26_20250921.csv
├── fc26_exploration.ipynb
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation

Clone the repository:

```bash
git clone https://github.com/daniel-oa/fc26-playerfinder.git
cd fc26-playerfinder
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Start the Streamlit application with:

```bash
streamlit run app.py
```

The application will open in your browser.

## Tech Stack

- Python
- Pandas
- Streamlit
- NumPy
- Jupyter Notebook

## Project Scope

This is **Version 1** of the FC26 PlayerFinder.

The current version focuses on player filtering and data exploration. Features such as player comparison, player similarity, ranking systems, scouting recommendations, and machine learning are outside the scope of this version.

## Future Development

Future versions may introduce additional player analysis and discovery features.