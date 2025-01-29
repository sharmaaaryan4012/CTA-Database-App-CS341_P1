"""
Name: Aaryan Sharma
Program-1: CTA Database Menu
CS - 341 (Spring 2024)
Professor: Ellen Kidane
"""


import sqlite3 as sq
import matplotlib.pyplot as plt

def stats ():                                                                                                           # This function is used to print out the basic statistics at the very start of the program.
    print("General Statistics:")

    query = "SELECT (SELECT COUNT(station_name) FROM stations), (SELECT COUNT(stop_ID) FROM stops), (SELECT COUNT(station_id) FROM ridership), (SELECT DATE(MIN(ride_date)) FROM ridership), (SELECT DATE(MAX(ride_date)) FROM ridership), (SELECT SUM(num_riders) FROM ridership)"
    con = sq.connect("CTA2_L_daily_ridership.db")                                                                       # Connecting to the database.
    cursor = con.cursor()
    cursor.execute(query)

    basicStats = cursor.fetchone()
    print("  # of stations:", f"{basicStats[0]:,}")
    print("  # of stops:", f"{basicStats[1]:,}")
    print("  # of ride entries:", f"{basicStats[2]:,}")
    print("  date range:", basicStats[3], "-", basicStats[4])
    print("  Total ridership:", f"{basicStats[5]:,}")

    con.close()


def stationCheck (stationName):                                                                                         # This function is used to perform initial checks on the databasae, to confirm whether a station "stationName" exists.
    check = "SELECT DISTINCT station_id, station_name FROM stations WHERE station_name LIKE \"" + stationName + "\""

    con = sq.connect("CTA2_L_daily_ridership.db")                                                                       # Connecting to the database.
    cursor = con.cursor()
    cursor.execute(check)
    stations = cursor.fetchall()

    if (len(stations) == 0):
        print("**No station found...")
        return False

    elif len(stations) > 1:
        print("**Multiple stations found...")
        return False

    return True


def func1 ():                                                                                                           # This function is used to run Command-1 for the program.
    stationName = input("\nEnter partial station name (wildcards _ and %): ")
    query = "SELECT station_id, station_name FROM stations WHERE station_name LIKE \"" + stationName +"\" ORDER BY station_name ASC"

    con = sq.connect("CTA2_L_daily_ridership.db")
    cursor = con.cursor()

    cursor.execute(query)
    stations = cursor.fetchall()

    if (len(stations) != 0):
        for i in stations:
            print(i[0], ":", i[1])

    else:
        print("**No stations found...")

    con.close()


def func2 ():                                                                                                           # This function is used to run Command-2 for the program.
    stationName = input("\nEnter the name of the station you would like to analyze: ")
    query = "SELECT SUM(CASE WHEN type_of_day = 'W' THEN num_riders ELSE 0 END), SUM(CASE WHEN type_of_day = 'A' THEN num_riders ELSE 0 END), SUM(CASE WHEN type_of_day = 'U' THEN num_riders ELSE 0 END) FROM ridership r INNER JOIN stations s ON r.station_id = s.station_id WHERE s.station_name = \"" + stationName + "\""

    con = sq.connect("CTA2_L_daily_ridership.db")
    cursor = con.cursor()

    cursor.execute(query)
    stations = cursor.fetchone()

    if (None not in stations):
        if (sum(stations) != 0):
            print("Percentage of ridership for the", stationName,"station:")
            print("  Weekday ridership:", f"{stations[0]:,}", f"({stations[0] / (sum(stations)) * 100:.2f}%)")
            print("  Saturday ridership:", f"{stations[1]:,}", f"({stations[1] / (sum(stations)) * 100:.2f}%)")
            print("  Sunday/Holiday ridership:", f"{stations[2]:,}", f"({stations[2] / (sum(stations)) * 100:.2f}%)")
            print("  Total ridership:", f"{sum(stations):,}")

    else:
        print("**No data found...")

    con.close()

def func3 ():                                                                                                           # This function is used to run Command-3 for the program.
    print("Ridership on Weekdays for Each Station")
    total = 0
    query = "SELECT s.station_name, SUM(r.num_riders) FROM ridership r JOIN stations s ON r.station_id = s.station_id WHERE r.type_of_day = 'W' GROUP BY s.station_name ORDER BY SUM(r.num_riders) DESC;"

    con = sq.connect("CTA2_L_daily_ridership.db")
    cursor = con.cursor()

    cursor.execute(query)
    stations = cursor.fetchall()

    for i in stations:
           total += i[1]

    for j in stations:
        print(f"{j[0]} : {j[1]:,} ({(j[1]/total) * 100:.2f}%)")

    con.close()


def func4 ():                                                                                                           # This function is used to run Command-4 for the program.
    color = input("\nEnter a line color (e.g. Red or Yellow): ")
    check = "SELECT line_id FROM lines WHERE LOWER(color) = \"" + color.lower() + "\""

    con = sq.connect("CTA2_L_daily_ridership.db")
    cursor = con.cursor()

    cursor.execute(check)
    exist = cursor.fetchone()

    if (exist == None):
        print("**No such line...")

    else:
        dir = input("Enter a direction (N/S/W/E): ")
        query = "SELECT stop_name, direction, ada FROM stops st JOIN stopdetails sd ON st.stop_id = sd.stop_id JOIN lines l ON sd.line_id = l.line_id WHERE LOWER(l.color) = \"" + color.lower() + "\" AND UPPER(st.direction) = \"" + dir.upper() + "\" ORDER BY stop_name ASC;"
        cursor.execute(query)
        stations = cursor.fetchall()

        if (len(stations) != 0):
            for i in stations:
                status = "(handicap accessible)" if i[2] else "(not handicap accessible)"
                print(i[0], ": direction =", i[1], status)

        else:
            print("**That line does not run in the direction chosen...")

    con.close()


def func5 ():                                                                                                           # This function is used to run Command-5 for the program.
    print("Number of Stops For Each Color By Direction")
    queryTotal = "SELECT COUNT(stop_id) FROM stops"
    query = "SELECT l.color, s.direction, COUNT(*) FROM stops s JOIN stopdetails sd ON s.stop_id = sd.stop_id JOIN lines l ON sd.line_id = l.line_id GROUP BY l.color, s.direction ORDER BY LOWER(l.color) ASC, UPPER(s.direction) ASC"

    con = sq.connect("CTA2_L_daily_ridership.db")
    cursor = con.cursor()

    cursor.execute(queryTotal)
    total = cursor.fetchone()
    total = total[0]

    cursor.execute(query)
    stations = cursor.fetchall()

    for i in stations:
        print(f"{i[0].capitalize()} going {i[1]} : {i[2]} ({(i[2]*100/total):.2f}%)")

    con.close()


def func6 ():                                                                                                           # This function is used to run Command-6 for the program.
    stationName = input("\nEnter a station name (wildcards _ and %): ")
    check = "SELECT DISTINCT station_id, station_name FROM stations WHERE station_name LIKE \"" + stationName + "\""

    con = sq.connect("CTA2_L_daily_ridership.db")
    cursor = con.cursor()

    cursor.execute(check)
    stations = cursor.fetchall()

    if (len(stations) == 0):
        print("**No station found...")

    elif (len(stations) > 1):
        print("**Multiple stations found...")

    else:
        query = "SELECT strftime('%Y', ride_date) AS Year, SUM(num_riders) FROM ridership WHERE station_id = \"" + str(stations[0][0]) + "\" GROUP BY Year ORDER BY Year;"
        title = "Yearly Ridership at " + stations[0][1]
        print(title)
        cursor.execute(query)
        ridership = cursor.fetchall()

        stationsY = []
        stationsR = []

        for i in ridership:
            stationsY.append(i[0])
            stationsR.append(i[1])
            print(i[0], ":", f"{i[1]:,}")

        choice = input("Plot? (y/n) \n")
        if (choice.upper() == 'Y'):
            title += " stations"
            plt.plot(stationsY, stationsR)
            plt.title(title)
            plt.ylabel('Number of Riders')
            plt.xlabel('Year')
            plt.show()

    con.close()


def func7 ():                                                                                                           # This function is used to run Command-7 for the program.
    stationName = input("\nEnter a station name (wildcards _ and %): ")
    check = "SELECT DISTINCT station_id, station_name FROM stations WHERE station_name LIKE \"" + stationName + "\""

    con = sq.connect("CTA2_L_daily_ridership.db")
    cursor = con.cursor()
    cursor.execute(check)
    stations = cursor.fetchall()


    if (len(stations) == 0):
        print("**No station found...")

    elif len(stations) > 1:
        print("**Multiple stations found...")

    else:
        year = input("Enter a year: ")
        query = "SELECT strftime('%m/%Y', r.ride_date), SUM(r.num_riders) FROM ridership r JOIN stations s ON r.station_id = s.station_id WHERE s.station_name = \"" + stations[0][1] + "\" AND strftime('%Y', R.ride_date) = \"" + year + "\" GROUP BY strftime('%m/%Y', r.ride_date)  ORDER BY r.ride_date;"
        cursor.execute(query)
        data = cursor.fetchall()
        dataY = []
        dataX = []

        print("Monthly Ridership at", stations[0][1], "for", year)

        for i in data:
            dataY.append(i[1])
            dataX.append((i[0])[0:2])
            print(i[0], ":", f"{i[1]:,}")


        choice = input("Plot? (y/n) \n")
        if (choice.upper() == 'Y'):
            title = "Monthly Ridership at " + stations[0][1] + " for " + str(year)
            plt.plot(dataX, dataY)
            plt.title(title)
            plt.ylabel('Number of Riders')
            plt.xlabel('Month')
            plt.show()


    con.close()


def func8 ():                                                                                                           # This function is used to run Command-8 for the program.
    year = input("\nYear to compare against? ")
    con = sq.connect("CTA2_L_daily_ridership.db")
    cursor = con.cursor()

    station1 = input("\nEnter station 1 (wildcards _ and %): ")
    if (stationCheck(station1)):
        station2 = input("\nEnter station 2 (wildcards _ and %): ")
        if (stationCheck(station2)):
            queryID1 = "SELECT station_id, station_name FROM stations WHERE station_name LIKE \"" + station1 + "\""
            queryID2 = "SELECT station_id, station_name FROM stations WHERE station_name LIKE \"" + station2 + "\""

            cursor.execute(queryID1)
            id1 = cursor.fetchone()
            cursor.execute(queryID2)
            id2 = cursor.fetchone()


            queryR1 = "SELECT strftime('%Y-%m-%d', ride_date), SUM(num_riders) FROM ridership WHERE station_id = \"" + str(id1[0]) + "\" AND strftime('%Y', ride_date) = \"" + year + "\" GROUP BY strftime('%Y-%m-%d', ride_date) ORDER BY ride_date"
            queryR2 = "SELECT strftime('%Y-%m-%d', ride_date), SUM(num_riders) FROM ridership WHERE station_id = \"" + str(id2[0]) + "\" AND strftime('%Y', ride_date) = \"" + year + "\" GROUP BY strftime('%Y-%m-%d', ride_date) ORDER BY ride_date"

            cursor.execute(queryR1)
            data1 = cursor.fetchall()
            cursor.execute(queryR2)
            data2 = cursor.fetchall()

            print("Station 1:", id1[0], id1[1])
            for day in data1[:5] + data1[-5:]:
                print(day[0], day[1])

            print("Station 2:", id2[0], id2[1])
            for day in data2[:5] + data2[-5:]:
                print(day[0], day[1])

            choice = input("Plot? (y/n) \n")
            if (choice.upper() == 'Y'):
                plt.title(f"Ridership Each Day of {year}")
                plt.plot([day[0] for day in data1], [day[1] for day in data1])
                plt.plot([day[0] for day in data2], [day[1] for day in data2])
                plt.xlabel("Day")
                plt.ylabel("Number of Riders")
                plt.legend([f"{station1}", f"{station2}"])
                plt.show()

    con.close()




def func9():
    lat = float(input("\nEnter a latitude: "))
    if (lat < 40 or lat > 43):
        print("**Latitude entered is out of bounds...")
    else:
        long = float(input("Enter a longitude: "))

        if (long < -88 or long > -87):
            print("**Longitude entered is out of bounds...")
        else:
            con = sq.connect("CTA2_L_daily_ridership.db")
            cursor = con.cursor()
            query = "SELECT DISTINCT station_name, latitude, longitude FROM stations s JOIN stops st ON s.station_id == st.station_id WHERE \"" + str(lat + round(1/69, 3)) + "\" > latitude AND latitude > \"" + str(lat - round(1/69, 3)) + "\" AND \"" + str(long + round(1/51, 3)) + "\" > longitude AND longitude > \"" + str(long - round(1/51, 3)) + "\"  ORDER BY station_name ASC"
            cursor.execute(query)
            data = cursor.fetchall()

            if len(data) == 0:
                print("**No stations found...")

            else:
                print("\nList of Stations Within a Mile")
                for i in data:
                    print(f"{i[0]} : ({i[1]}, {i[2]})")
                choice = input("Plot? (y/n) \n")

                if choice.upper() == 'Y':
                    x, y = [], []
                    for i in data:
                        x.append(i[2])
                        y.append(i[1])

                    xydims = [-87.9277, -87.5569, 41.7012, 42.0868]
                    plt.xlim(xydims[:2])
                    plt.ylim(xydims[2:])

                    plt.imshow(plt.imread("chicago.png"), extent=xydims)
                    plt.title("Stations near you")
                    plt.scatter(x, y)

                    for j in data:
                        plt.annotate(j[0], (j[2], j[1]))
                    plt.show()


def menu ():
    choice = input("Please enter a command (1-9, x to exit): ")

    while (choice != 'x'):
        if (choice.isnumeric() and (int(choice) > 0) and (int(choice) < 10)):
            if (int(choice) == 1):
                func1()

            elif (int(choice) == 2):
                func2()

            elif (int(choice) == 3):
                func3()

            elif (int(choice) == 4):
                func4()

            elif (int(choice) == 5):
                func5()

            elif (int(choice) == 6):
                func6()

            elif (int(choice) == 7):
                func7()

            elif (int(choice) == 8):
                func8()

            elif (int(choice) == 9):
                func9()

        else:
            print("**Error, unknown command, try again...")

        choice = input("Please enter a command (1-9, x to exit): ")


if __name__ == "__main__":
    print("** Welcome to CTA L analysis app **\n")

    stats()                                                                                                             # Function call to output the basic statistics.
    menu()                                                                                                              # Function call to start the menu-driven portion of the program.
