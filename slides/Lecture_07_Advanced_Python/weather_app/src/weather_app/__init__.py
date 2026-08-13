from .convert import celsius_to_fahrenheit

def main() -> None:
    temperature = 26.5
    result = celsius_to_fahrenheit(temperature)
    print(f"{temperature} °C = {result} °F")

if __name__ == "__main__":
    main()