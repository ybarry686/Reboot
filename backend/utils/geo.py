import math

_nomi = None


def haversine_miles(lat1, lng1, lat2, lng2):
    if None in (lat1, lng1, lat2, lng2):
        return None
    r = 3958.8
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lng2 - lng1)
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    return r * 2 * math.asin(math.sqrt(a))


def zip_to_latlng(zip_code):
    global _nomi
    try:
        if _nomi is None:
            import pgeocode

            _nomi = pgeocode.Nominatim("us")
        result = _nomi.query_postal_code(str(zip_code).strip())
    except Exception as exc:
        print(f"[geo] zip lookup failed for '{zip_code}': {exc}")
        return None, None

    if result is None or math.isnan(result.latitude):
        return None, None
    return result.latitude, result.longitude