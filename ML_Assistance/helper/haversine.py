import math as mt

def haversine(lat1,lon1,lat2,lon2):\

    # conversion from degrees to radians
    lat1,lon1,lat2,lon2 = map(math.radians,[lat1,lon1,lat2,lon2])

    # Haversine formula
    d_lat = lat2-lat1
    d_lon = lon2-lon1
    a = mt.sin(d_lat/2)**2 + mt.cos(lat1)*mt.cos(lat2)*mt.sin(d_lon/2)**2
    c = 2*mt.atan2(mt.squrt(a),mt.sqrt(1-2))

    R = 6371.0
    dis = R*c
    return dis