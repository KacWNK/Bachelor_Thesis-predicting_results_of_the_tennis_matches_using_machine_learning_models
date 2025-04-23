# Predicting results of the tennis matches using various types of machine learning models

## Abstract
The project’s goal was to develop a predictive model for high-quality forecasting of tennis
match results and create a user-friendly website presenting them.
We tested three machine learning models: logistic regression, XGBoost and a neural network. Input data included features related to the players and the environment. Experiments showed that the neural network outperformed the other methods and achieved only
a 0,0032 lower Brier score than bookmakers’ predictions. Additionally, the model achieved
a return on investment (ROI) of 5.62% and a percentage profit of 29.57%, confirming
its effectiveness in practical applications within the domain of sports betting.
An integral part of the project was the creation of a website based on the Django framework, which, for each selected match, presents the model’s predictions and various game
and player statistics that were used in the prediction process. The system included a complex data flow that included real-time data acquisition, iterative processing, and uploading
to the database used by the site.
The designed system combines an effective predictive model with a convenient platform
for visualization and reporting results.

The entire thesis can be found in the file BSc_Thesis.pdf

# Predicting Results of Tennis Matches Using Machine Learning Models

## Project Description

This project was developed as part of an engineering thesis and focuses on predicting the outcomes of tennis matches using various machine learning models. It leverages historical data on matches and players. The full pipeline includes data collection, preprocessing, feature engineering, model training, and results visualization.

## Repository Structure

- `Website_ss/` – screenshots or assets related to the web version of the project.
- `creating_dataframes_for_webpage/src/` – scripts for preparing data to be displayed on the web.
- `creating_graphs_for_paper/` – scripts generating plots used in the thesis.
- `feature_creation/` – code responsible for feature engineering based on raw data.
- `main_flow/` – the main logic pipeline connecting data processing and model components.
- `models/` – saved/trained models or configuration files.
- `old_data/` – archived versions of older data.
- `preparation_before_models/` – scripts preparing datasets for model training.
- `preprocessing/` – data cleaning, transformation, and standardization scripts.
- `raw_data/` – raw input datasets.
- `scraping/` – web scraping tools for collecting online data.
- `tennis_bets_website/` – codebase of the website presenting model predictions.
- `test_helpers/` – unit tests and utility functions for testing.

## Files

- `BSc_Thesis.pdf` – full version of the engineering thesis (in Polish).

## How to Run

1. Clone the repository:

```bash
git clone https://github.com/KacWNK/Bachelor_Thesis-predicting_results_of_the_tennis_matches_using_machine_learning_models.git
cd Bachelor_Thesis-predicting_results_of_the_tennis_matches_using_machine_learning_models
```
# Requirements
- Python 3.8+
- pandas
- numpy
- scikit-learn
- xgboost
- matplotlib
- seaborn
- optuna
- geopy
- PyTorch
- Django

2. Run the relevant Python scripts or Jupyter notebooks based on the stage of analysis.
# Data sources:
-https://github.com/JeffSackmann/tennis_atp – comprehensive database of ATP matches with detailed information about players, results, match locations, and surface types.

-Official ATP websites.

-http://www.tennis-data.co.uk/alldata.php – database containing historical match results and betting odds.

# Authors
The authors of the work are Kacper Wnęk and Paweł Świderski as part of their engineering thesis at Warsaw University of Technology.
_____________________________________________________________________________________
## Streszczenie
Celem projektu było opracowanie wysokiej jakości modelu predykcyjnego do prognozowania wyników meczów tenisowych oraz stworzenie strony internetowej prezentującej predykcje modelu w sposób przystępny dla użytkownika.
W ramach badań przetestowano trzy modele uczenia maszynowego: regresję logistyczną, XGBoost oraz sieć neuronową. Dane wejściowe obejmowały cechy związane z zawodnikami oraz ze środowiskiem. Wyniki eksperymentów wykazały, że sieć neuronowa
przewyższyła pozostałe metody oraz osiągnęła jedynie o 0,0032 niższy wskaźnik Briera
od predykcji bukmacherów. Dodatkowo model osiągnął zwrot z inwestycji (ROI) na poziomie 5,62% oraz procentowy zysk wynoszący 29,57%, co potwierdza jego skuteczność
w praktycznych zastosowaniach w obszarze zakładów bukmacherskich.
Integralną częścią projektu było stworzenie strony internetowej przy użyciu Django,
na której dla każdego wybranego meczu prezentowane są prognozy modelu oraz różnorodne statystyki — zarówno dla danej rozgrywki, jak i zawodników — wykorzystywane
w procesie predykcji. System uwzględniał złożony przepływ danych, który obejmował pozyskiwanie danych w czasie rzeczywistym, iteracyjne przetwarzanie oraz wgrywanie do
bazy danych używanej przez stronę.
Zaprojektowany system łączy skuteczny model predykcyjny z wygodną platformą raportowania wyników, co potwierdza jego potencjał w zastosowaniach praktycznych, szczególnie w analizie danych tenisowych.

Opracowanie całej pracy znajduje się w pliku BSc_Thesis.pdf



# Predicting Results of Tennis Matches Using Machine Learning Models

## Opis projektu

Projekt stanowi część pracy inżynierskiej i dotyczy przewidywania wyników meczów tenisowych z użyciem różnych modeli uczenia maszynowego. Dane pochodzą z historycznych statystyk meczowych i zawodników, a cały proces obejmuje zbieranie danych, ich przetwarzanie, tworzenie cech, trenowanie modeli i wizualizację wyników.

## Struktura repozytorium

- `Website_ss/` – zrzuty ekranu lub pliki związane z wersją webową projektu.
- `creating_dataframes_for_webpage/src/` – skrypty przygotowujące dane do prezentacji na stronie internetowej.
- `creating_graphs_for_paper/` – skrypty generujące wykresy do pracy dyplomowej.
- `feature_creation/` – kod odpowiedzialny za inżynierię cech (tworzenie zmiennych na podstawie danych źródłowych).
- `main_flow/` – główny przepływ logiki projektu, prawdopodobnie spinający przetwarzanie danych i modele.
- `models/` – zapisane/trenowane modele lub konfiguracje modelowe.
- `old_data/` – starsze wersje danych (archiwum).
- `preparation_before_models/` – skrypty przygotowujące dane do trenowania modeli.
- `preprocessing/` – kod związany z czyszczeniem, przekształcaniem i standaryzacją danych.
- `raw_data/` – surowe dane wejściowe.
- `scraping/` – kod odpowiedzialny za web scraping (pobieranie danych z internetu).
- `tennis_bets_website/` – struktura strony internetowej prezentującej wyniki modelu.
- `test_helpers/` – testy jednostkowe i/lub funkcje pomocnicze do testowania.

## Pliki

- `BSc_Thesis.pdf` – pełna wersja pracy inżynierskiej.
  
## Jak uruchomić

1. Sklonuj repozytorium:

```bash
git clone https://github.com/KacWNK/Bachelor_Thesis-predicting_results_of_the_tennis_matches_using_machine_learning_models.git
cd Bachelor_Thesis-predicting_results_of_the_tennis_matches_using_machine_learning_models
```
## Wymagania

Do uruchomienia projektu potrzebne są:

- Python 3.8+
- pandas
- numpy
- scikit-learn
- xgboost
- matplotlib
- seaborn
- optuna
- geopy
- PyTorch
- Django
2. Uruchom odpowiednie skrypty Pythona lub notebooki Jupyter w zależności od etapu analizy
# Źródła danych:
-https://github.com/JeffSackmann/tennis_atp -- obszerna baza danych o meczach ATP, zawierająca szczegółowe informacje na temat zawodników, wyników, lokalizacji meczów oraz rodzajów nawierzchni.

-Oficjalne strony ATP.

-http://www.tennis-data.co.uk/alldata.php  -- baza danych zawierająca wyniki meczów i kursy bukmacherskie.

# Autorzy
Autorami pracy są Kacper Wnęk oraz Paweł Świderski w ramach pracy inżynierskiej na Politechnice Warszawskiej.
