class ThereIsNo(BaseException):
    def __init__(self, *args):
        super().__init__(*args)

def there_is(x):
    if x is None:
        raise ThereIsNo()
    return x

def into_none(pred, x):
    if pred(x):
        return x
    return None