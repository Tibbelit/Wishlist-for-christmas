from bottle import run, template, route, request, redirect, static_file
import json

def read_wishes_from_file():
    '''
    Returns a list of wishes,  from file: "wishes.json"
	
	Example result:
	[
        {
            "id": 1,
            "name": "iPhone",
            "price": 14000,
            "link": "https://www.apple.com/se/iphone-14/",
            "prio": 1
        },
        {
            "name": "Pixel 7 Pro",
            "price": "9990",
            "link": "https://store.google.com/se/product/pixel_7_pro?hl=sv&pli=1",
            "prio": "1",
            "id": 2
        }
	]

	Returns:
		list : The wishes
	'''
    try:
        my_file = open("wishes.json", "r")
        wishes = json.loads(my_file.read())
        my_file.close()

        return wishes
    except FileNotFoundError:
        my_file = open("wishes.json", "w")
        my_file.write(json.dumps([]))
        my_file.close()

        return []

def create_id(wishes):
    """
    Returns an integer representing the current highest id + 1
    
    Returns
        int : the current highest id + 1
    """
    highest_id = 1
    for wish in wishes:
        if wish["id"] >= highest_id:
            highest_id = wish["id"] + 1

    return highest_id

@route("/")
def index():
    '''Returns the start page
	
	Returns:
		template : index
	'''
    wishes = read_wishes_from_file()
    return template("index", wishes= wishes)

@route("/new-wish", method="post")
def new_wish():
    '''
    Registers a new wish, then redirects the user to the start page
	'''
    name = getattr(request.forms, "name")
    price = getattr(request.forms, "price")
    link = getattr(request.forms, "link")
    prio = getattr(request.forms, "prio")

    wishes = read_wishes_from_file()
    id = create_id(wishes)

    wishes.append({
        "name": name,
        "price": price,
        "link": link,
        "prio": prio,
        "id": id
    })

    my_file = open("wishes.json", "w")
    my_file.write(json.dumps(wishes, indent=4))
    my_file.close()

    redirect("/")

@route("/static/<filename>")
def static_files(filename):
    '''
    Handles the routes to our static files
	
	Returns:
		file : the static file requested by URL	
	'''
    return static_file(filename, root="static")

# Start our web server
run(host="127.0.0.1", port=8080, reloader=True)