from anecAPI import anecAPI


def message():
    ane = str(anecAPI.random_joke())
    return ane
