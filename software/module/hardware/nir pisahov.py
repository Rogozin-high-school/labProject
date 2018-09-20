import supplies

zup = supplies.ZUP()

zup.connect()
zup.clear()
zup.set_remote(1)
max = 30
avg = 16
min = 2

while max != avg:
    for b in range(min, max):
        zup.set_volt(b)
    min += 1
    max -= 1
