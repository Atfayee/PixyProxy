import uuid


def make_guid() -> str:
    guid = str(uuid.uuid4()).replace("-", "")
    return guid

# def make_filename() -> str:
#     # Implement the logic to generate a filename
#     filename = "generated_filename"+str(uuid.uuid4())
#     return filename