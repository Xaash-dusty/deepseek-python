from datetime import datetime, timedelta, timezone

print(datetime.now())
print(datetime.now(timezone.utc))
print(datetime.now().strftime("%d.%m.%Y %H:%M:%S"))

d = datetime(2000, 1, 1)
print((datetime.now() - d).days)

parsed_date = datetime.strptime("15.03.2024 09:45", "%d.%m.%Y %H:%M")
print(parsed_date.strftime("%A"))

future_date = datetime.now() + timedelta(days=365)
print(future_date.isoformat)