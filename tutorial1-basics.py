from fastapi import FastAPI, Body

app = FastAPI()

cooks = {'one': 1,
         'two': 2,
         'three': 3}

books = [{'title' : 'John', 'category': 'A', 'value':100},
         {'title' : 'Wick', 'category': 'A', 'value':200},
         {'title' : 'John', 'category': 'B', 'value':300},
         {'title' : 'Wick',  'category': 'B','value':400}]


@app.get("/api-endpoints")
async def first_api():
    return {'message': 'Election 2024!'}


@app.get("/read_all_books")
async def first_api():
    return books


# STATIC parameter
@app.get("/books/one")
async def first_api():
    return {'message': 'Hello Thereee!'}


# DYNAMIC PARAMETER
# keep all DYNAMIC PATH PARAMETER after static
@app.get("/books/{dynamic_param}")
async def new_function(dynamic_param):
    return cooks[dynamic_param]


# DYNAMIC + QUERY PARAMETER
# Query parameter are taken automatically
@app.get("/booking/{dynamic_param}/")
async def new_function(dynamic_param, category):
    m = [x for x in books if x['title'] == dynamic_param and x['category'] == category][0]['value']
    return m

# POST
@app.post("/create_post")
async def create_new_books(new_book=Body()):
    books.append(new_book)


# PUT
@app.put("/update_book")
async def update_book(upd_book=Body()):
    for i in range(len(books)):
        if books[i][0]['value'] == upd_book['value']:
            books[i] = upd_book

# uvicorn books:app --reload (web server)

