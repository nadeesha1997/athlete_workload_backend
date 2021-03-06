from datetime import date


##################################################################
# Return weekly workloads as a set of values from list of workloads
###################################################################
def workload_measurement(workloadlist):
    first_week = []
    second_week = []
    third_week = []
    fourth_week = []
    today = date.today()
    for item in workloadlist:
        day_difference = (today - item.date).days
        if day_difference < 29:  # date difference
            if day_difference > 21:
                fourth_week.append(item)
            elif day_difference > 14:
                third_week.append(item)
            elif day_difference > 7:
                second_week.append(item)
            else:
                first_week.append(item)
    first_week_workload = weekly_workload(first_week)  # taking the weekly sum of workloads
    second_week_workload = weekly_workload(second_week)
    third_week_workload = weekly_workload(third_week)
    fourth_week_workload = weekly_workload(fourth_week)
    return first_week_workload, second_week_workload, third_week_workload, fourth_week_workload


###################################
# Return ACWR for specific activity
###################################
def acwr(first_week, second_week, third_week, forth_week):
    if not first_week + second_week + third_week + forth_week == 0:  # checking if the total workload in month is 0
        return (4 * first_week) / (first_week + second_week + third_week + forth_week)  # returning acwr
    return 0


#################################
# Return ACWR for all activities
##################################
def activity_acwr(workload_list):
    w_list = list(workload_list)
    acwr_val = {}
    for key in w_list[0].workload_data["har"]:  # iterating over activities
        first_week_workload, second_week_workload, third_week_workload, fourth_week_workload = workload_measurement(
            workload_list)
        acwr_val[key] = acwr(first_week_workload[key], second_week_workload[key], third_week_workload[key],
                             fourth_week_workload[key])
        # print("first_week_workload" + str(first_week_workload[key]))
        # print("second_week_workload" + str(second_week_workload[key]))
        # print("third_week_workload" + str(third_week_workload[key]))
        # print("fourth_week_workload" + str(fourth_week_workload[key]))
        # print(acwr_val[key])
    return acwr_val


##############################################
# Return weekly workload from daily workloads
##############################################
def weekly_workload(workload_list):
    total_workload = {}
    for key in workload_list[0].workload_data["har"]:
        total_workload[key] = 0
    for daily_workload in workload_list:  # summing the workloads over the week
        for key in daily_workload.workload_data["har"]:
            if daily_workload.workload_data["har"][key]:
                total_workload[key] += daily_workload.workload_data["har"][key]
    return total_workload


############################################################
# Return next day workload for given activity and given ACWR
#############################################################
def workload_for_acwr(acwr, last_six, second, third, forth):
    last_three = second + third + forth
    nominator = acwr * (last_six + last_three) - last_six
    return nominator / (acwr + 1)


############################################################################
# Return next day workload for all activities from a list of daily workloads
############################################################################
def next_day_workload(workloadlist, acwr, activities):
    work_list = list(workloadlist)
    first_week = []
    second_week = []
    third_week = []
    fourth_week = []
    today = date.today()
    for item in work_list:
        ########## checking date differences for next day workload calculation ##########
        day_difference = (today - item.date).days
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
    weekly_workloads = {'1': weekly_workload(first_week), '2': weekly_workload(second_week),#weekly workload for each week
                        '3': weekly_workload(third_week), '4': weekly_workload(fourth_week)}
    activity_workloads = {}
    for key1 in weekly_workloads['1']:
        activity_workloads[key1] = []
    for key1 in weekly_workloads['1']:
        for key in weekly_workloads:
            activity_workloads[key1].append(weekly_workloads[key][key1])

    final_data = {}
    for key in activity_workloads:
        final_data[key] = workload_for_acwr(acwr, activity_workloads[key][0], activity_workloads[key][1],
                                            activity_workloads[key][2], activity_workloads[key][3])

    return final_data
