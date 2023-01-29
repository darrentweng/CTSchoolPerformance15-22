# CT School Performance

This is a project to analyze the performance of Connecticut schools. The data is from the [Connecticut State Department of Education](https://public-edsight.ct.gov/Performance/Smarter-Balanced-Achievement-Participation?language=en_US).

## Data Sources
Use the following sources to get: Student Performance by grade/town/grade/year/race, income & school location dataset.
- [Connecticut State Department of Education](https://public-edsight.ct.gov/Performance/Smarter-Balanced-Achievement-Participation?language=en_US)
- [Smarter Balanced Assesment Scale Score Range For Grade 3-8](https://portal.ct.gov/-/media/SDE/Student-Assessment/Smarter-Results-Resources/smarter_balanced_scale_scores_and_achievement_levels_final.pdf)
- [List of Connecticut locations by per capita income](https://en.wikipedia.org/wiki/List_of_Connecticut_locations_by_per_capita_income)
- [Connecticut Educational Directory](https://data.ct.gov/Education/Education-Directory/9k2y-kqxn)

## Data Cleaning

### Manual Data Cleaning
Download `smarterbalanced.csv` and manually perform the following steps: 
- Remove first 4 row
- Delete District Code & all "Percentage Level 3 or 4 (Met or Exceeded)%" columns
- Replace the year "2016-17" with "2016", etc... and repeat the year row values to fill in the blanks on 1st row
- Insert 3rd row, and move the first 4 column headers down to 3rd line, to make it valid multiIndex format.
### Batch Data Cleaning
Run `python cleanup_smartbalance.py` to clean and generate "sb_final.csv". For detailed steps, see `cleanup_smartbalance.ipynb`.

Save sb_final.csv to a public github repo, and use the following public link to download the file.
## Data Analysis w/ Streamlit

### Development with Docker
Run the following commands to build the dev docker image and run the container that use local files throughout development process:
```
docker build -t stcharts .
docker run -p 8501:8501 -p 8888:8888 -v %cd%:/home/streamlit stcharts
```
Then visit [localhost:8501](http://localhost:8501/)
### Package with Docker
Run the following command to build the production docker image and test run it:
```
docker build -t stcharts .
docker run -p 8501:8501 stcharts:latest  # can be launched anywhere, no need to mount local files
```

## Other Resources
- [Accessing Data in a MultiIndex DataFrame in Pandas](https://towardsdatascience.com/accessing-data-in-a-multiindex-dataframe-in-pandas-569e8767201d)