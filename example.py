from store import store

app = store.Store()

app.scan("VOUCHER")
app.scan("VOUCHER")
app.scan("VOUCHER")
app.scan("TSHIRT")
app.scan("MUG")

print(app.total())