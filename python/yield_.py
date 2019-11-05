def cor1(name=None):       
        print("send value", name)
        yield
cor_ =  cor1("zj")
while True:

    print("next return", next(cor_))
