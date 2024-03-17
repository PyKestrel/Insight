from typing import Union, Annotated
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile
import Evtx.Evtx as evtx
import tempfile
class Log(BaseModel):
    name: str
    description: str | None = None

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/file/")
async def parse_file(file: UploadFile):
  if (".evtx" in file.filename):
    try:
      # Read uploaded file data
      content = await file.read()
      # Create a temporary file-like object
      with tempfile.NamedTemporaryFile() as temp_file:
        # Write uploaded file data (ensure successful write)
        temp_file.write(content)
        temp_file.seek(0)  # Move cursor to the beginning
        # Get the temporary file path (after successful write)
        file_path = temp_file.name
        # Open the EVTX file using the path
        with evtx.Evtx(file_path) as log:
          # Print the first record (XML data)
          print(log.records()[0].xml())

      return {"message": "Successfully parsed the first record of the EVTX file."}
    except Exception as e:
      print(str(e))
      return {"error": "An Error Occured"}