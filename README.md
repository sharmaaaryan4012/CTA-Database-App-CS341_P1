# CTA-Database-App-CS341_P1

## Overview
The CTA Database App is a console-based Python application designed to interact with the CTA L daily ridership database using SQL queries. The app inputs commands from the user and outputs data relevant to CTA stations, stops, lines, and ridership.

## Database Schema
The database consists of five main tables:
- **Stations**: Contains `Station_ID` (primary key) and `Station_Name`.
- **Stops**: Includes `Stop_ID` (primary key), `Station_ID` (foreign key), `Stop_Name`, `Direction`, `ADA` status, and geographical coordinates (`Latitude` and `Longitude`).
- **Lines**: Comprises `Line_ID` (primary key) and `Color`.
- **StopDetails**: Joins stops with lines and includes `Stop_ID` and `Line_ID` as a composite primary key.
- **Ridership**: Tracks ridership data with fields like `Station_ID` (foreign key), `Ride_Date`, `Type_of_Day`, and `Num_Riders`.

## Features
The application supports multiple commands to interact with the database:
1. Search for stations by name using wildcards.
2. Analyze ridership by station for different days.
3. Compute total ridership on weekdays for each station.
4. Display stops for a given line and direction.
5. Count the number of stops per line by direction.
6. Display yearly ridership for a station.
7. Show monthly ridership for a station in a given year.
8. Compare daily ridership between two stations for a year.
9. Find stations within a one-mile radius of a given geographical point.

## Getting Started

### Prerequisites
- Python 3.x
- SQLite3
- Matplotlib (for plotting data)

### Installation
1. Clone the repository:
