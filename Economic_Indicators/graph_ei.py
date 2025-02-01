import matplotlib.pyplot as plt

EXIT_OK = 0
EXIT_FAIL = 1

def plot_real_gdp(data: dict):
    '''
    Generates a plot of the real GDP vs time

    Input:
    data: dict of the raw data from the API

    Output:
    exit status (0 for okay, 1 for fail)
    '''
    title = f"{data['name']} in the USA"
    x_axis_label = data['interval'] if data['interval'] == "Quarter" else "Year"
    y_axis_label = data["unit"].title()
    x_coords = [x["date"] for x in data["data"]]
    y_coords = [float(x["value"]) for x in data["data"]]
    x_coords.reverse()
    y_coords.reverse()

    if len(x_coords) == len(y_coords):
        plt.figure(figsize=(10, 6))
        plt.plot(x_coords, y_coords, marker='o', linestyle='-', color='b', label='Real GDP') 
        plt.title(title)
        plt.xlabel(x_axis_label)
        plt.ylabel(y_axis_label)

        interval = max(1, len(x_coords) // 10)
        plt.xticks(ticks=range(0, len(x_coords), interval), labels=x_coords[::interval], rotation=45)

        plt.legend()
        plt.tight_layout()

        plt.savefig("real_gdp_plot.png")
        plt.close()
        return EXIT_OK
    
    else:
        print("Error: mismatch between dates and real GDP data.")
        return EXIT_FAIL
    
def plot_real_gdp_per_capita(data: dict):
    '''
    Generates a plot of the real GDP per capita vs time

    Input:
    data: dict of the raw data from the API

    Output:
    exit status (0 for okay, 1 for fail)
    '''
    title = f"{data['name']} in the USA"
    x_axis_label = data['interval'] if data['interval'] == "Quarter" else "Year"
    y_axis_label = data["unit"].title()
    x_coords = [x["date"] for x in data["data"]]
    y_coords = [float(x["value"]) for x in data["data"]]
    x_coords.reverse()
    y_coords.reverse()

    if len(x_coords) == len(y_coords):
        plt.figure(figsize=(10, 6))
        plt.plot(x_coords, y_coords, marker='o', linestyle='-', color='b', label='Real GDP per Capita') 
        plt.title(title)
        plt.xlabel(x_axis_label)
        plt.ylabel(y_axis_label)

        interval = max(1, len(x_coords) // 10)
        plt.xticks(ticks=range(0, len(x_coords), interval), labels=x_coords[::interval], rotation=45)

        plt.legend()
        plt.tight_layout()

        plt.savefig("real_gdp_per_capita_plot.png")
        plt.close()
        return EXIT_OK
    
    else:
        print("Error: mismatch between dates and real GDP per capita data.")
        return EXIT_FAIL