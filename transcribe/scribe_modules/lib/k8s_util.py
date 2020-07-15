
def remove_managed_fields(d):
    if "metadata" in d:
        d["metadata"].pop("managedFields", None)
