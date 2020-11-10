# to add item in session
request.session["key"] = "value"

# get item from session
a = request.session["key"]
a = request.session.get("key")

# remove item from session
del request.session["key"]
# del request.session.get("key") wrong