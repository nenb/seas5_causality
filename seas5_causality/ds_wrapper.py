class my_ds_wrapper:
    '''Basic wrapper around a dataset for computing a temporal average over a given
    spatial and temporal range. See compute_time_av method for details.'''
    
    def __init__(self, ds):
        self.ds = ds
        
    def shift_meridian(self):
        '''Shift longitude coordinates from (0, 360) to (-180, 180)'''
        
        lons = (((self.ds.longitude + 180) % 360) - 180)
        self.ds = self.ds.assign_coords(longitude = lons).sortby('longitude')

    def select_lon(self, lon1 = None, lon2 = None):
        '''Select a longitude range of values from a dataset'''
        
        if lon1 == None:
            lon1 = self.ds.longitude[0]
        if lon2 == None:
            lon2 = self.ds.longitude[-1]
        return self.ds.longitude[(self.ds.longitude >= lon1) & (self.ds.longitude <= lon2)]

    def select_lat(self, lat1 = None, lat2 = None):
        '''Select a latitude range of values from a dataset'''
        
        if lat1 == None:
            lat1 = self.ds.latitude[0]
        if lat2 == None:
            lat2 = self.ds.latitude[-1]
        return self.ds.latitude[(self.ds.latitude >= lat1) & (self.ds.latitude <=lat2)]
    
    def select_days(self, sday = None, eday = None):
        '''Select a day range from a dataset'''
        
        if sday == None:
            sday = self.ds.time.dt.dayofyear[0]
        if eday == None:
            eday = self.ds.time.dt.dayofyear[-1]
        return (self.ds.time.dt.dayofyear > sday) & (self.ds.time.dt.dayofyear < eday)
    
    def select_years(self, syear = None, eyear = None):
        '''Select a year range from a dataset'''
        
        if syear == None:
            syear = self.ds.time.dt.year[0]
        if eyear == None:
            eyear = self.ds.time.dt.year[-1]
        return (self.ds.time.dt.year > syear) & (self.ds.time.dt.year < eyear) 

    def compute_time_av(self, lats = None, lons = None, days = None, years = None,
                       shift = False):
        '''Compute a time average of a dataset over a given spatial and temporal range'''
        
        if shift:
            self.shift_meridian()
        if lats == None:
            lats = [self.ds.latitude[0], self.ds.latitude[-1]]
        if lons == None:
            lons = [self.ds.longitude[0], self.ds.longitude[-1]]
        if days == None:
            days = [self.ds.time.dt.dayofyear[0], self.ds.time.dt.dayofyear[-1]]
        if years == None:
            years = [self.ds.time.dt.year[0], self.ds.time.dt.year[-1]]
        time_range = (self.select_days(*days)) & (self.select_years(*years))
        lat_range = self.select_lat(*lats)
        lon_range = self.select_lon(*lons)
        
        _ds = self.ds.sel(time = time_range, latitude = lat_range, longitude = lon_range)
        return _ds.mean('time')
