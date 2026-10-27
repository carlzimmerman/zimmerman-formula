"""Token dissimilarity and automatic known-result promotion are retired."""
def add_known(*args,**kwargs):
    raise RuntimeError('Model claims do not become known results automatically')
