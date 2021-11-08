from datetime import datetime


# Transforming the date to timestamp - this is how the Facebook API accepts dates.
def transform_date(day, month, year):
    input_date = f"{day}/{month}/{year}"
    parsed_date = datetime.strptime(input_date,"%d/%m/%Y")
    converted_date = str(round(float(parsed_date.timestamp())))
    return converted_date



if __name__ == "__main__":
    print(transform_date(26,10,2021))

