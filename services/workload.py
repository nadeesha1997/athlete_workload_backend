from datetime import date


def workload_measurement(workloadlist):
    first_week = []
    second_week = []
    third_week = []
    fourth_week = []
    today = date.today()
    for item in workloadlist:
        if today - item.date > 21:
            fourth_week.append(item)
        elif today - item.date > 14:
            third_week.append(item)
        elif today - item.date > 7:
            second_week.append(item)
        else:
            first_week.append(item)
    first_week_workload = weekly_workload(first_week)
    second_week_workload = weekly_workload(second_week)
    third_week_workload = weekly_workload(third_week)
    fourth_week_workload = weekly_workload(fourth_week)
    # return {
    #     "first": first_week_workload,
    #     "second": second_week_workload,
    #     "third": third_week_workload,
    #     "fourth": fourth_week_workload
    # }
    return first_week_workload, second_week_workload, third_week_workload, fourth_week_workload


def weekly_workload(workload_list):
    total_workload = {}
    for key in workload_list[0].workload_data["har"]:
        total_workload[key] = 0
    for daily_workload in workload_list:
        for key in daily_workload.workload_data["har"]:
            total_workload[key] += daily_workload.workload_data["har"][key]
    return total_workload


def workload_for_acwr(acwr, last_six, second, third, forth):
    last_three = second + third + forth
    nominator = acwr * (last_six + last_three) - last_six
    return nominator / (acwr + 1)


def next_day_workload(workloadlist, acwr, activities):
    work_list = list(workloadlist)
    first_week = []
    second_week = []
    third_week = []
    fourth_week = []
    today = date.today()
    for item in work_list:
        day_difference=(today-item.date).days
        if day_difference > 27:
            work_list.remove(item)
        else:
            if day_difference > 20:
                fourth_week.append(item)
            elif day_difference > 13:
                third_week.append(item)
            elif day_difference > 6:
                second_week.append(item)
            else:
                first_week.append(item)
    weekly_workloads = {'1': weekly_workload(first_week), '2': weekly_workload(second_week),
                        '3': weekly_workload(third_week), '4': weekly_workload(fourth_week)}
    activity_workloads={}
    for key1 in weekly_workloads['1']:
        activity_workloads[key1]=[]
    for key1 in weekly_workloads['1']:
        for key in weekly_workloads:
            activity_workloads[key1].append(weekly_workloads[key][key1])

    final_data={}
    for key in activity_workloads:
        final_data[key]=workload_for_acwr(acwr,activity_workloads[key][0],activity_workloads[key][1],activity_workloads[key][2],activity_workloads[key][3])

    return final_data
