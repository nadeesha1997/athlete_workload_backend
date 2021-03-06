from device.models import SportMountPlace, Device
from mlmodel.serializers import TrainDataSerializer


def merge(datalist, sport):
    places = SportMountPlace.objects.filter(sport_id=sport.id)
    devices = Device.objects.all()
    device_selected = []
    for device in devices:
        for place in places:
            if device.mount_id == place.id:
                device_selected.append(device)
    read = {}
    for d in device_selected:
        read[d.id] = []
    for dataval in datalist:
        temp_data = dataval.data
        for temp_data_val in temp_data:
            read[temp_data_val['1']].append(temp_data_val)
    maximum_time = []
    minimum_length = []
    for key in read:
        temp = []
        temp.append(read[key])
        temp.sort(key=lambda x: x[0]['3'])
        read[key] = temp
        # print(read[key][0][0]['3'])
        maximum_time.append(read[key][0][0]['3'])
    maximum = max(maximum_time)
    # print('max' + str(maximum))
    for key in read:
        for val in read[key][0]:
            if val['3'] < maximum:
                read[key][0].remove(val)
    for key in read:
        minimum_length.append(len(read[key][0]))
    min_len = min(minimum_length)
    for key in read:
        length = len(read[key][0]) - min_len
        if length > 0:
            for i in range(length):
                read[key][0].pop(-1)
    har_data = {}
    heart_rate = []
    label=[]
    sport_place_list = list(places)
    place_list = []
    for place in sport_place_list:
        place_list.append(place.place)
    place_list.sort(key=lambda x: x.mounting_order)
    # print(len(read[device_selected[0].id][0]))
    for j in range(len(read[device_selected[0].id][0])):
        har_data[j] = []
    for j in range(len(read[device_selected[0].id][0])):
        for mount_place in places:
            for d in device_selected:
                if d.mount == mount_place.place:
                    har_data[j].append(read[d.id][0][j]['4'])
                    har_data[j].append(read[d.id][0][j]['5'])
                    har_data[j].append(read[d.id][0][j]['6'])
                    har_data[j].append(read[d.id][0][j]['7'])
                    har_data[j].append(read[d.id][0][j]['8'])
                    har_data[j].append(read[d.id][0][j]['9'])
                    if d.mount.mounting_order == 1:
                        if read[d.id][0][j]['10'] > 60:
                            heart_rate.append(read[d.id][0][j]['10'])
    final_data = {
        "har": har_data,
        "hr": heart_rate
    }
    # final_data= [har_data, heart_rate]
    export_data = {
        "data": final_data,
        "sport":sport
    }
    serializer = TrainDataSerializer(data=export_data)
    if serializer.is_valid(raise_exception=True):
        return export_data
    return []