import requests
import os
import argparse
import json

def fetch_data(url, download_dir, data_format, year):
    """
    Fetch data from a remote URL and save it locally.

    Args:
        url (str): URL of the remote data file.
        download_dir (str): Directory where the data file will be saved.
        data_format (str): Format of the data file ("csv" or "json").
        year (str): Year for data retrieval.

    Returns:
        str: Path to the downloaded data file.
    """
    # Ensure the download directory exists; create it if necessary
    os.makedirs(download_dir, exist_ok=True)

    # Determine the file extension based on the selected format
    if data_format.lower() == "csv":
        file_extension = "csv"
    elif data_format.lower() == "json":
        file_extension = "json"
    else:
        raise ValueError("Invalid format. Supported formats are 'csv' and 'json'.")

    # Generate the filename based on year and format
    filename = os.path.join(download_dir, f"crime-data-{year}.{file_extension}")

    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Save the content of the response (the data file) to a local file
            with open(filename, "wb") as file:
                file.write(response.content)
            print(f"Downloaded data to {filename}")
            return filename
        else:
            print(f"Failed to download data. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Define command-line arguments for data format and year
    parser = argparse.ArgumentParser(description="Fetch data from a remote URL.")
    parser.add_argument("format", type=str, choices=["csv", "json"], help="Data format (csv or json)")
    parser.add_argument("year", type=str, help="Year for data retrieval")
    args = parser.parse_args()

    # Load the configuration file
    with open("config.json", "r") as config_file:
        config = json.load(config_file)

    # Extract the data URL based on the specified year and format
    data_format = args.format
    year = args.year

    # Check if the year is available in the configuration
    if year in config["urls"]:
        data_url = config["urls"][year]
    else:
        print(f"Year {year} not found in the configuration.")
        exit(1)

    # Use the current directory as the download directory
    download_dir = os.path.dirname(os.path.abspath(__file__))

    # Fetch data based on the specified format
    fetch_data(data_url, download_dir, data_format, year)
