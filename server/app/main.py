'''
main module running the app.
'''
import datetime
from bson import ObjectId
from fastapi import FastAPI, status, responses, Request
from fastapi.middleware.cors import CORSMiddleware
from .database import db
from .models import Entry

app = FastAPI()
coll = db["calories"]

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
def ping():
    '''
    ping check
    '''
    return {"message": "ping test for calorie tracker!!"}

@app.get("/entries", response_description="Get all entries")
def get_entries():
    '''
    to get all entries
    '''
    try:
        all_entries = []
        cursor = coll.find({})
        for document in cursor:
            all_entries.append(document)

        for entry in all_entries:
            entry["_id"] = str(entry["_id"])

        return all_entries
        # return responses.JSONResponse(status_code=status.HTTP_200_OK, content=all_entries)

    except Exception as err:
        return responses.JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(err)},
        )

@app.post("/entry/add", response_description="Add new entry", response_model=Entry)
def add_entry(entry: Entry):
    '''
    add new entry
    '''
    try:
        utc_time_now = datetime.datetime.utcnow()
        entry.created_at = utc_time_now
        entry.updated_at = utc_time_now
        entry_dict = entry.dict(by_alias=True)
        coll.insert_one(entry_dict)
        entry_dict["_id"] = str(entry_dict["_id"])

        return entry_dict
        # return responses.JSONResponse(status_code=status.HTTP_200_OK, content=entry_dict)

    except Exception as err:
        return responses.JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(err)},
        )

@app.get("/entry/")
def get_entry_by_id(id: str):
    '''
    to get an entry by objectId of the document in collection.
    '''
    # id is a query parameter not a path parameter
    try:
        print("id=", id)
        entry = coll.find_one({"_id": ObjectId(id)})
        if entry is not None:
            entry["_id"] = str(entry["_id"])
            print(type(entry))
        return entry
        # return responses.JSONResponse(status_code=status.HTTP_200_OK, content=entry)

    except Exception as err:
        return responses.JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(err)},
        )

@app.put("/ingredient/update")
async def update_ingredients_by_id(id: str, request: Request):
    '''
    to update ingredients of an entry using the objectId of the document in collection.
    '''
    # id is a query parameter not a path parameter
    try:
        doc_id = ObjectId(id)
        # Update document in MongoDB
        update_time = datetime.datetime.utcnow()
        req_body = await request.json()
        result = coll.find_one_and_update(
            {"_id": doc_id, "softDeletedAt": None},
            {
                "$set": {
                    "ingredients": req_body["ingredients"],
                    "updatedAt": update_time,
                }
            },
            return_document=True,
        )

        # Return updated document
        if result:
            result["_id"] = str(result["_id"])
            return result
        return responses.JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content="entry not found"
        )
    except Exception as err:
        return responses.JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(err)},
        )

@app.put("/entry/update")
async def update_entry_by_id(id: str, request: Request):
    '''
    to update entry using the objectId of the document in collection.
    '''
    # id is a query parameter not a path parameter
    try:
        doc_id = ObjectId(id)
        # Update document in MongoDB
        update_time = datetime.datetime.utcnow()
        req_body = await request.json()
        result = coll.find_one_and_update(
            {"_id": doc_id, "softDeletedAt": None},
            {
                "$set": {
                    "dish": req_body["dish"],
                    "ingredients": req_body["ingredients"],
                    "fat": req_body["fat"],
                    "calories": req_body["calories"],
                    "updatedAt": update_time,
                }
            },
            return_document=True,
        )

        # Return updated document
        if result:
            result["_id"] = str(result["_id"])
            return result
        return responses.JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content="entry not found"
        )
    except Exception as err:
        return responses.JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(err)},
        )

@app.delete("/entry/softdelete/")
def soft_delete_entry(id: str):
    '''
    to softdelete entry using the objectId of the document in collection.
    '''
    # id is a query parameter not a path parameter
    try:
        doc_id = ObjectId(id)
        # Update document in MongoDB
        deleted_at_time = datetime.datetime.utcnow()
        result = coll.find_one_and_update(
            {"_id": doc_id, "softDeletedAt": None},
            {"$set": {"softDeletedAt": deleted_at_time}},
            return_document=True,
        )

        # Return updated document
        if result:
            result["_id"] = str(result["_id"])
            return result
        else:
            return responses.JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND, content="entry not found"
            )
    except Exception as err:
        return responses.JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(err)},
        )

@app.delete("/entry/delete/")
def delete_entry(id: str):
    '''
    to delete entry using the objectId of the document in collection.
    '''
    # id is a query parameter not a path parameter
    try:
        doc_id = ObjectId(id)
        # Update document in MongoDB
        result = coll.find_one_and_delete({"_id": doc_id})

        # Return updated document
        if result:
            result["_id"] = str(result["_id"])
            return result
        else:
            return responses.JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND, content="entry not found"
            )
    except Exception as err:
        return responses.JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(err)},
        )
