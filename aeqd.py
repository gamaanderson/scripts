import numpy as np

def aeqd_to_latlon(x, y, lat_0, lon_0):
    """
    Parameters
    ----------
    x, y: narray
        Coordinates in Azimuthal Equidistant projection
    lat_0, lon_0: scalar
        Center of the projection

    Returns
    -------
    lat, lon: narray
        Corresponding latitude and longitude

    Notes
    -----
    The projection conversion is manual implemented for a spherical earth.
    It uses the mean radius of earth (6371 km).

    .. math::

        c = \\sqrt(x^2 + y^2)/R

        azi = \\arctan2(y,x) \\text{  # from east to north}

        lat = \\arcsin(\\cos(c)*\\sin(lat0)+\\sin(azi)*\\sin(c)*\\cos(lat0))

        lon = \\arctan2(\\cos(azi)*\\sin(c),\\cos(c)*\\cos(lat0)-\\sin(azi)*\\sin(c)*\\sin(lat0)) + lon0

    Where x, y are the cartesian position from the center of projection;
    lat, lon the corresponding latitude and longitude; lat0, lon0 the latitude
    and longitude of the center of the projection; R the mean radius of the
    earth (6371 km)

    References
    ----------
    .. [1] Snyder, J. P. Map Projections--A Working Manual. U. S. Geological
        Survey Professional Paper 1395, 1987, pp. 191-202.
    """
    R = 6371.0 * 1000.0  # radius of earth in meters.

    c = np.sqrt(x*x + y*y) / R
    phi_0 = lat_0 * np.pi / 180
    azi = np.arctan2(y, x)  # from east to north

    lat = np.arcsin(np.cos(c) * np.sin(phi_0) +
                    np.sin(azi) * np.sin(c) * np.cos(phi_0)) * 180 / np.pi
    lon = (np.arctan2(np.cos(azi) * np.sin(c), np.cos(c) * np.cos(phi_0) -
            np.sin(azi) * np.sin(c) * np.sin(phi_0)) * 180 /
            np.pi + lon_0)
    lon = np.fmod(lon + 180, 360) - 180

    return lat, lon


def latlon_to_aeqd(lat, lon, lat_0, lon_0):
    """
    Parameters
    ----------
    lat, lon: narray
        Latitude and LongitudeCoordinates in Azimuthal Equidistant projection
    lat_0, lon_0: scalar
        Center of the projection

    Returns
    -------
    lat, lon: narray
        Corresponding coordinates in Azimuthal Equidistant projection

    Notes
    -----
    The projection conversion is manual implemented for a spherical earth.
    It uses the mean radius of earth (6371 km).

    .. math::

        c = \\arccos(\\sin(lat0)*\\sin(lat)+\\cos(lat0)*\\cos(lat)*\\cos(lon-lon0))

        k = c / \\sin(c)

        x = R*k*\\cos(lat)\\sin(lon-lon0)

        y = R*k*(\\cos(lat0)*\\sin(lat)-\\sin(lat0)*\\cos(lat)*\\cos(lon-lon0))

    Where x, y are the cartesian position from the center of projection;
    lat, lon the corresponding latitude and longitude; lat0, lon0 the latitude
    and longitude of the center of the projection; R the mean radius of the
    earth (6371 km)

    References
    ----------
    .. [1] Snyder, J. P. Map Projections--A Working Manual. U. S. Geological
        Survey Professional Paper 1395, 1987, pp. 191-202.
    """
    R = 6371.0 * 1000.0  # radius of earth in meters.

    phi_0 = lat_0 * np.pi / 180
    phi = lat * np.pi / 180
    lambda_ = (lon - lon_0) * np.pi / 180

    c =  np.arccos(np.sin(phi_0) * np.sin(phi) +
                   np.cos(phi_0) * np.cos(phi) * np.cos(lambda_))

    k = c / np.sin(c)

    x = R * k * np.cos(phi) * np.sin(lambda_)

    y = R * k * (np.cos(phi_0) * np.sin(phi) -
                 np.sin(phi_0) * np.cos(phi) * np.cos(lambda_))

    return x, y
