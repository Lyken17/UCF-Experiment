class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

database_dir = "/Users/lykensyu/Documents/ucf_sports_actions/"
output_dir = "data/collection.json"