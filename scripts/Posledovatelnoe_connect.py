def posledovatelnoe_connect_om(spisok,slovar,fps):
    om = 0
    for i in spisok:
        x = i[0]
        y = i[1]
        elem = (x,y)
        if elem in slovar:
            om += slovar[elem][0]
    print('----')
    print(slovar)
    print(om)
    if om == 0:
        return fps
    return fps / om
