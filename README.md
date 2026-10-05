#Inventory Mangement System

     >> A small Flask app that manages inventory — you can add products, view them, edit them, delete them, and pull real product info from OpenFoodFacts by barcode.

    I built it in Python 3.12 with Flask. It uses requests to talk to OpenFoodFacts and pytest for tests.

##What it does
   !>Full CRUD on inventory items (GET, POST, PATCH, DELETE)

   !>Fetches product data from OpenFoodFacts by barcode

   !>Imports fetched products straight into the inventory

   !>Menu-driven CLI (cli.py) that talks to the running API

   !>Test suite covering every helper and every route

##Files

   inventory.py       -- in-memory database + CRUD helper functions
   app.py             -- Flask routes
   external_api.py    -- OpenFoodFacts integration
   cli.py             -- command-line menu
   tests/             -- pytest suite
   requirements.txt   -- dependencies


##Setup
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

##Running it
>>Start the API in one terminal:
   python app.py
>>Then run the CLI in another terminal:
   python cli.py

"""The menu lets you list, view, add, update, and delete items, or import from OpenFoodFacts by barcode."""

*##Routes*
  Method	Route
  GET	/inventory
  GET	/inventory/<id>
  POST	/inventory
  PATCH	/inventory/<id>
  DELETE	/inventory/<id>
  GET	/external/product/<barcode>
  POST	/external/import/<barcode>
Example:
  >>bash
curl -X POST http://127.0.0.1:5000/inventory \
  -H "Content-Type: application/json" \
  -d '{"product_name": "Chips", "brands": "Lays", "price": 250.0, "stock": 20}'

##Tests
  pytest -v
>>Tests cover every route and every CRUD helper, plus the OpenFoodFacts routes with the external call mocked so tests run offline.

###Notes
>>>Database is in-memory — restarting the server clears any items you added.

>>>OpenFoodFacts blocks requests without a User-Agent header; external_api.py sends one.

>>>Some barcodes return product data in French. I didn't translate it where the Nutella barcode tested runs its ingredients in French.