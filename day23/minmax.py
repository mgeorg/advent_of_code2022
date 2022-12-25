_sentinel = object()

def minmax(*args, key=None, default=_sentinel):
    if len(args) > 1:
        if default is not _sentinel:
            raise ValueError(
                "Cannot specify a default for minmax() with "
                "multiple positional arguments"
           )
        v = args
    else:
        v = args[0]

    minval = minitem = maxval = maxitem = None
    for item in v:
        val = key(item) if key is not None else item
        if minval is None or val < minval:
            minval, minitem = val, item
        if maxval is None or val > maxval:
            maxval, maxitem = val, item
    
    if minval is None:
        assert minitem is maxval is maxitem is None
        if default is _sentinel:
            raise ValueError("minmax() arg is an empty sequence")
        minitem = maxitem = default
    
    return minitem, maxitem
