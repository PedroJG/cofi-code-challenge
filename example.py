from store import Store

app = Store()

app.scan("VOUCHER")
app.scan("VOUCHER")
app.scan("VOUCHER")
app.scan("TSHIRT")
app.scan("MUG")

print(app.total())