import geocoder

def geolocation(ip): #returns location from public ip
    if (ip):
        locale = []
        geolocation = geocoder.ip(ip)
        locale.append(geolocation.lat)
        locale.append(geolocation.lng)
        locale.append(geolocation.city)
        locale.append(geolocation.state)

        return locale