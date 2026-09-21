# Seasonal observations of Black-faced Spoonbills in Hong Kong


![Twelve monthly maps of Black-faced Spoonbill records in Hong Kong](out/plot.png)

## The phenomenon
Black-faced Spoonbills are migratory waterbirds that spend much of the winter in Hong Kong. I wanted to see how their recorded presence changes across the year and whether observations in different months appear in the same places. I therefore compared georeferenced occurrence records from the six complete years from 2020 to 2025. Using the same geographic scale for every month makes the seasonal rise and fall in records, as well as changes in their recorded locations, easy to compare.

## The source

The data comes from the [GBIF occurrence download](https://www.gbif.org/occurrence/download/0001661-260916113435855). The archive contains 8,235 occurrence records for *Platalea minor* in Hong Kong between 1981 and 2026. Each row represents one published occurrence record, not necessarily one individual bird. I used the year, month, decimal latitude and decimal longitude fields. Coordinates are measured in decimal degrees, and the analysis keeps 5,316 records from the complete years 2020–2025.

## What the picture shows

The picture shows a strong seasonal pattern. Records are most numerous from November to April, reaching more than 1,000 in both November and December, but falling to very low levels from June to September. Many observations remain concentrated around the Deep Bay and Mai Po area. However, the chart shows reported occurrences rather than the true bird population: observation effort varies, repeated visits may create multiple records, and overlapping points can hide how many observations share the same coordinates.

## Run it

```
uv run fetch.py
uv run plot.py
```
