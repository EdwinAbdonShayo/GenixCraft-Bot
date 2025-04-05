import astra

context = astra.AstraContext()
devices = context.get_devices()
print(devices)
