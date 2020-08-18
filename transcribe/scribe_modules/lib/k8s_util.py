
def remove_unused_fields(d):
    if "metadata" in d:
        d["metadata"].pop("managedFields", None)
    if "metadata" in d and "annotations" in d["metadata"]:
        d["metadata"]["annotations"].pop("kubectl.kubernetes.io/last-applied-configuration", None)
