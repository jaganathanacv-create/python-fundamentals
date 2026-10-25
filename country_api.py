
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import quote


API_URL = "https://restcountries.com/v3.1/name/"


def get_country_info(country_name):
    if not country_name.strip():
        print("Error: Country name cannot be empty.")
        return

    url = API_URL + quote(country_name.strip()) + "?fields=name,capital,population,region,currencies"

    request = Request(
        url,
        headers={"User-Agent": "PythonCountryInfoApp/1.0"}
    )

    try:
        with urlopen(request, timeout=10) as response:
            if response.status != 200:
                print("API unavailable. Please try again later.")
                return

            data = json.loads(response.read().decode("utf-8"))

        if not isinstance(data, list) or not data:
            print("Invalid API response.")
            return

        country = data[0]

        if not isinstance(country, dict) or "name" not in country:
            print("Invalid country data received.")
            return

        name = country.get("name", {}).get("common", "Not available")
        capitals = country.get("capital", [])
        capital = ", ".join(capitals) if capitals else "Not available"
        population = country.get("population", 0)
        region = country.get("region", "Not available")

        currencies = country.get("currencies", {})
        if currencies:
            currency_details = []
            for code, details in currencies.items():
                currency_name = details.get("name", code)
                currency_details.append(f"{currency_name} ({code})")
            currency = ", ".join(currency_details)
        else:
            currency = "Not available"

        print("\n===== COUNTRY INFORMATION =====")
        print("Name       :", name)
        print("Capital    :", capital)
        print("Population :", f"{population:,}")
        print("Region     :", region)
        print("Currency   :", currency)
        print("===============================")

    except HTTPError as error:
        if error.code == 404:
            print("No matching country found. Check the country name.")
        else:
            print(f"API error: HTTP {error.code}")

    except URLError:
        print("Network error. Check your internet connection.")

    except (json.JSONDecodeError, UnicodeDecodeError, KeyError, TypeError):
        print("Invalid API response received.")

    except TimeoutError:
        print("Request timed out. Please try again.")

    except OSError:
        print("Unable to connect to the API. Please try again later.")


def main():
    print("Country Information Finder")
    country_name = input("Enter country name: ")
    get_country_info(country_name)


if __name__ == "__main__":
    main()
