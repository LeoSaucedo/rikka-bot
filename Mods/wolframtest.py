import wolframalpha

client = wolframalpha.Client("JUWJU7-XLKG8VWUX8")

res = client.query('temperature in Tallahassee, FL')

result = next(res.results).text

print(result)