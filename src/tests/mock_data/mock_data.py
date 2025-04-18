from pathlib import Path

BASE_URL = "https://www.scrapethissite.com/pages/forms/"

current_dir = Path(__file__).parent.resolve()
html_file_dir = Path.joinpath(current_dir, "html")


def get_file_data(path):
    with open(path) as file:
        data = file.read()
    return data


def get_mocked_base_url_html():
    base_file_path = Path.joinpath(html_file_dir, "base.txt")
    html = get_file_data(base_file_path)
    response = {BASE_URL: html}
    return response


def get_mocked_pagination_url_html():
    file_path_1 = Path.joinpath(html_file_dir, "1.html")
    html_1 = get_file_data(file_path_1)
    file_path_2 = Path.joinpath(html_file_dir, "2.html")
    html_2 = get_file_data(file_path_2)
    file_path_3 = Path.joinpath(html_file_dir, "3.html")
    html_3 = get_file_data(file_path_3)
    file_path_4 = Path.joinpath(html_file_dir, "4.html")
    html_4 = get_file_data(file_path_4)
    file_path_5 = Path.joinpath(html_file_dir, "5.html")
    html_5 = get_file_data(file_path_5)
    file_path_6 = Path.joinpath(html_file_dir, "6.html")
    html_6 = get_file_data(file_path_6)
    file_path_7 = Path.joinpath(html_file_dir, "7.html")
    html_7 = get_file_data(file_path_7)
    file_path_8 = Path.joinpath(html_file_dir, "8.html")
    html_8 = get_file_data(file_path_8)
    file_path_9 = Path.joinpath(html_file_dir, "9.html")
    html_9 = get_file_data(file_path_9)
    file_path_10 = Path.joinpath(html_file_dir, "10.html")
    html_10 = get_file_data(file_path_10)

    response = {
        f"{BASE_URL}?page_num=1": html_1,
        f"{BASE_URL}?page_num=2": html_2,
        f"{BASE_URL}?page_num=3": html_3,
        f"{BASE_URL}?page_num=4": html_4,
        f"{BASE_URL}?page_num=5": html_5,
        f"{BASE_URL}?page_num=6": html_6,
        f"{BASE_URL}?page_num=7": html_7,
        f"{BASE_URL}?page_num=8": html_8,
        f"{BASE_URL}?page_num=9": html_9,
        f"{BASE_URL}?page_num=10": html_10,
    }
    return response


def get_zipped_files_list():
    response = [
        "1.html",
        "2.html",
        "3.html",
        "4.html",
        "5.html",
        "6.html",
        "7.html",
        "8.html",
        "9.html",
        "10.html",
    ]
    return response


def get_excel_sheet_names():
    response = ["NHL Stats 1990-2011", "Winner and Loser per Year"]
    return response


def get_analytics_sheet_name():
    response = "Winner and Loser per Year"
    return response


def get_mocket_analytical_data():
    response = [
        ("Year", "Winner", "Winner Num. of Wins", "Loser", "Loser Num. of Wins"),
        (1990, "Chicago Blackhawks", 49, "Quebec Nordiques", 16),
        (1991, "New York Rangers", 50, "San Jose Sharks", 17),
        (1992, "Pittsburgh Penguins", 56, "Ottawa Senators", 10),
        (1993, "New York Rangers", 52, "Ottawa Senators", 14),
        (1994, "Detroit Red Wings", 33, "Ottawa Senators", 9),
        (1995, "Detroit Red Wings", 62, "Ottawa Senators", 18),
        (1996, "Colorado Avalanche", 49, "Boston Bruins", 26),
        (1997, "Dallas Stars", 49, "Tampa Bay Lightning", 17),
        (1998, "Dallas Stars", 51, "Tampa Bay Lightning", 19),
        (1999, "St. Louis Blues", 51, "Atlanta Thrashers", 14),
    ]
    return response
