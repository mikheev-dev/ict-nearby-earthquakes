# nearby-earthquakes
[USGS Earthquake Hazards Program](https://earthquake.usgs.gov/) is an organization that analyzes earthquake threats around the world. They expose REST API outlining details of recent earthquakes happening around the world - location, magnitude, etc.  

We would like to write a program that for a given city (we will provide lat/lon) will find out 10 most nearby earthquakes (earthquakes that happened in the closest proximity of that city).

## Getting list of earthquakes
Web services for fetching Earthquakes are located here: https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php  
We are interested in all earthquakes that happened during last 30 days: https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson  

For each earthquake there is a lat/lon location of that earthquake. We would like the program to connect to this web service and pull the earthquake data.

## Calculating distance
We expect the program to correctly calculate curve distance between two lat/lon points.

## Program input
Program should accept two numbers on standard input: the latitude and longitude of a city. So for New York the program should be started with numbers:  
```
40.730610  
-73.935242  
```
Source: https://www.latlong.net/place/new-york-city-ny-usa-1848.html

## Program output
As an output, we want the program to list **10** earthquakes that happened in the closest proximity to input point, in the order from the closest to the furthest. For each earthquake we want to print the content of a `title` field followed by ` || ` and `distance` (rounded to full kilometers).  
```
title || distance  
title || distance  
title || distance  
```

Note that if two earthquakes happened in the same location (lat/lon) we only want it to appear only once on the list.

## Summary
We would like the solution to do the following:
* Read two float numbers from standard input that represent the lat/lon of a city
* Read a list of earthquakes that happened during last 30 days
* Calculate distance between given city and each of the earthquakes
* Print the 10 earthquakes with the shortest distance to the given city
* The output list should contain earthquake title and distance in kilometers
* If two earthquakes happened in exactly the same location (they have the same lat/lon) we only want one of them to be printed
* It is ok for a solution to use external libraries

## Example usage:
Example Input:  
```
40.730610  
-73.935242  
```

Example Output:
```
M 1.3 - 2km SSE of Contoocook, New Hampshire || 331  
M 1.3 - 2km ENE of Belmont, Virginia || 354  
M 2.4 - 83km ESE of Nantucket, Massachusetts || 406  
M 1.3 - 13km ENE of Barre, Vermont || 410  
M 0.7 - 18km NW of Norfolk, New York || 476  
M 2.0 - 17km NW of Norfolk, New York || 476  
M 1.7 - 19km NNW of Beaupre, Canada || 758  
M 1.9 - 13km SW of La Malbaie, Canada || 814  
M 2.4 - 16km N of Lenoir, North Carolina || 840  
M 2.4 - 12km ESE of Carlisle, Kentucky || 896  
```

## How to submit a great solution
* Make sure input and output are correct. Read requirements carefully.
* We will try to run your program. Make sure we will understand how to do it. We don't know the IDE you use, nor run environment you have. Reviewers can have totally different setup, so test with your friend if you're not sure if it will run on different machine. Add RUN.md file that describes how to start it (if not using standard ways to run a program).
* We will run a formal code review on your solution. Make sure your code is not only correct but also easy to read and reason about. Make it "production ready"-like, the fact that it's just a coding task does not mean you should omit good engineering practices.
* You can use external libraries but you should only use the tools that are right to do the job. You don't have to build UI,  web application or implement database access to get the job done. Showcasing how many libraries or frameworks you know is not the goal of the task.
* We accept solutions written in `Python`. Contact us if you would like to use any other language.

