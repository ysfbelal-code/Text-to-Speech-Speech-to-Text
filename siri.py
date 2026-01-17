import requests, pyttsx3, datetime, sys

engine = pyttsx3.init()

def get_time_abroad():
    options = {
      'Asia': 1, 'Africa': 2, 'America': 3, 'Antarctica': 4, 'Arctic': 5,
      'Australia': 6, 'Brazil': 7, 'Canada': 8, 'Chile': 9, 'Cuba': 10,
      'Egypt': 11, 'Eire': 12, 'Europe': 13, 'Hongkong': 14, 'Iceland': 15,
      'Indian': 16, 'Iran': 17, 'Jamaica': 18, 'Japan': 19, 'Libya': 20,
      'Mexico': 21, 'Navajo': 22, 'Pacific': 23, 'Poland': 24, 'Portugal': 25,
      'Singapore': 26, 'Turkey': 27, 'US': 28, 'Universal': 29, 'Zulu': 30  
    }
    countries = ['Cuba','Egypt','Eire','Hongkong','Iceland','Iran','Japan',
                 'Jamaica','Kwajalein','Libya','Poland','Portugal','Singapore',
                 'Turkey','UCT','Universal','Zulu','Greenwich']

    try:
        area = int(input(f"Options: \n{options}\n>> "))
        region = list(options.keys())[area-1]   # FIX: get the string name, not the number

        if region in countries:
            url = f"http://worldtimeapi.org/api/timezone/{region}" 
        else:
            city = input("Enter a city\n>> ")
            url = f"http://worldtimeapi.org/api/timezone/{region}/{city}" 

        response = requests.get(url, timeout=5)
        data = response.json()
        print(f"Current time in {region}: {data['datetime']}")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error: {req_err}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def prompt(query):
    query = query.lower() 
    if 'time' in query:
        time_choice = input("Do you want to search for time from: abroad or local? ")
        if 'local' in time_choice:
            now = datetime.datetime.now().strftime('%H:%M')
            return f"The current time is {now}."
        elif 'abroad' in time_choice:
            get_time_abroad()
    elif 'date' in query:
        now = datetime.datetime.now().strftime('%D')
        return f"Today's date is {now}."
    elif 'exit' in query:
        print('Goodbye!')
        sys.exit()
    else:
        return "Error: Command not understood."

def main():
    print("PySiri is running. Enter your choice: time, date or exit.")
    while True:
        user = input('>> ')
        response = prompt(user)
        print(response)
        engine.say(response)
        engine.runAndWait()

main()