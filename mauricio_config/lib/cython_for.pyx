import math
import pompy

def read_sensor(x,y,_intensity,_sensor_x,_sensor_y,_sensor_dimention,_sum_reads):
    w = 1
    mean_reads = 0
    for i in range(len(_intensity)):
		
        if ((x[i] >= (_sensor_x - _sensor_dimention)) and (x[i] <= (_sensor_x + _sensor_dimention)) and (y[i] >= (_sensor_y - _sensor_dimention)) and (y[i] <= (_sensor_y + _sensor_dimention))):
                
                #for j in range(len(_intensity)): 

                    #if ((_points[j].y >= (_sensor_y - _sensor_dimention)) and (_points[j].y <= (_sensor_y + _sensor_dimention))):
                    
            _sum_reads += _intensity[i]          
             
                        
    mean_reads = _sum_reads/w
    w += 1 
    return mean_reads

def fix_read_sensor(x,y,_intensity,_sensor_x,_sensor_y,_sensor_dimention,_sum_reads):
        w = 1
        mean_reads = 0
        for i in range(len(_intensity)):
            
            if ((x[i] >= (_sensor_x - _sensor_dimention)) and (x[i] <= (_sensor_x + _sensor_dimention)) and (y[i] >= (_sensor_y - _sensor_dimention)) and (y[i] <= (_sensor_y + _sensor_dimention))):
                    
                    #for j in range(len(_intensity)): 

                        #if ((_points[j].y >= (_sensor_y - _sensor_dimention)) and (_points[j].y <= (_sensor_y + _sensor_dimention))):
                        
                _sum_reads += _intensity[i]          
                w += 1 
                            
        mean_reads = _sum_reads/w
        
        return mean_reads


def read_pompy_sensor(dictionary,_sensor_x,_sensor_y,_sensor_dimention,_sum_reads):
    _sum_reads = 0
    mean_reads = 0
    wind_angle = 0
    w = 0
    for i in range(len(dictionary)):
        if ((dictionary[i][0] >= (_sensor_x - _sensor_dimention)) and (dictionary[i][0] <= (_sensor_x + _sensor_dimention)) and (dictionary[i][1] >= (_sensor_y - _sensor_dimention)) and (dictionary[i][1] <= (_sensor_y + _sensor_dimention))):
            w += 1
            _sum_reads += dictionary[i][2]
    if w == 0:
        mean_reads = 0
    else:
        mean_reads = _sum_reads/w

    for a in range(len(dictionary)):
        if ((dictionary[a][0] >= (_sensor_x - 0.05)) and (dictionary[a][0] <= (_sensor_x + 0.05)) and (dictionary[a][1] >= (_sensor_y - 0.05)) and (dictionary[a][1] <= (_sensor_y + 0.05))):
            wind_angle = dictionary[a][3]
    return mean_reads, wind_angle

def angle_dist(vel_x, vel_y):
    distance = ( ( ( (vel_x) ** 2 ) + ( (vel_y) ** 2 ) ) ** (1/2) )
    if distance == 0:
        angle = 0
    else:
        angle = ( ( vel_y / distance ) + 1 ) / 2 
    return angle

def update(array_gen, wind_model, plume_model, dt):
    for q in range(10):

        wind_model.update(dt)
        plume_model.update(dt)

    _conc_array = array_gen.generate_single_array(plume_model.puff_array)

        
        # Initiation of variables temporary variables
    x =[]
    y = []
    inten = []
    d = {}
    vel_x, vel_y, norm = [],[],[]

    for i in range(_conc_array.T.shape[0]):

        for j in range(_conc_array.T.shape[1]):

            if (_conc_array.T[i][j] != 0):

                x.append(i*0.01 + 1.675)
                y.append(j*0.01 + 2.35)
                inten.append(_conc_array.T[i][j]*0.001)
                vel = wind_model.velocity_at_pos(i,j)
                    # vel_x.append(vel[0])
                    # vel_y.append(vel[1])
                norm.append(angle_dist(vel[0],vel[1]))


    for h in range(len(x)):
        d[h] = (x[h],y[h],(inten[h]/1000.0),norm[h])

    return d, array_gen, wind_model, plume_model

## Alto custo computacional
def cython_distance(_points,_intensity,_sensor_x,_sensor_y,_sensor_dimention,_sum_reads):
    
    for i in range(len(_points)):
        dist = math.sqrt(math.pow(_points[i].x - _sensor_x, 2) + math.pow(_points[i].y - _sensor_y, 2))
        if (dist < (_sensor_dimention*2)):
            _sum_reads += _intensity[i]
    return _sum_reads

def cython_distance1(x,y,_intensity,_sensor_x,_sensor_y,_sensor_dimention,_sum_reads):
    
    for i in range(len(x)):
        dist = math.sqrt(math.pow(x[i] - _sensor_x, 2) + math.pow(y[i] - _sensor_y, 2))
        if (dist < (_sensor_dimention*2)):
            _sum_reads += _intensity[i]
    return _sum_reads

