import os
import numpy as np
import csv
import math
import matplotlib.pyplot as plt


# Functions
def chk_titles(list1, list2, log_file):
    # We want to compare the smaller list to the bigger list.
    # As long as the entry from short list isn't a duplicate then we will append the entry
    if len(list1) > len(list2):
        list_short = list2
        list_long = list1
    else:
        list_short = list1
        list_long = list2
    log_file.write("Comparing two lists.\nThe short list has length:\t"+str(len(list_short) - 1)+"\nThe long list has length:\t"+str(len(list_long) - 1)+"\n")
    list_temp = list_short.copy()
    dup_chk = False
    count = 0
    for i in range(len(list_short)):
        for j in range(len(list_long)):
            if list_short[i][0].lower() == list_long[j][0].lower():
                dup_chk = True
                count = count + 1
        if dup_chk:
            list_temp.pop(i - count + 1)
            dup_chk = False

    # Get rid of the header section before appending, doing this before would require an index adjustment.
    log_file.write("Checking is complete, "+str(count)+" duplicate entries were found.\n")
    log_file.write("New combined list is expanded from "+str(len(list_long) - 1)+" to "+str(len(list_long) + len(list_temp) - 2)+".\n")
    print_spacer(log_file)
    list_temp.pop(0)
    list_long = list_long + list_temp
    return list_long


def get_data(path, name):
    file_data = open(os.path.join(path, name), "r")
    temp = list(csv.reader(file_data))
    file_data.close()
    return temp


def get_years(year_start, year_end, data, save_opt, path_out):
    years = np.zeros(shape=(year_end - year_start + 1), dtype=int)
    for lines in data:
        if "Year" not in lines[1]:
            years[int(lines[1]) - year_start] = years[int(lines[1]) - year_start] + 1
    if save_opt > 0:
        get_year_plot(year_start, year_end, years, save_opt, path_out)
    return years


def get_year_plot(year_start, year_end, years, save_opt, path_out):
    # Eventually I would like to do this with the conference
    # papers https://matplotlib.org/stable/gallery/lines_bars_and_markers/bar_label_demo.html
    x_axis = np.zeros(shape=(year_end - year_start + 1), dtype=int)
    for i in range(year_end - year_start + 1):
        x_axis[i] = year_start + i
    fig_ref = plt.figure()
    plt.bar(x_axis, years, zorder=3)
    fig_ref = fig_config(year_start, year_end, fig_ref)

    if save_opt > 1:
        plt.savefig(os.path.join(path_out, "Query_Year_Dist.png"))
    else:
        plt.show()
    plt.close()
    return


def get_year_plot_sub(year_start, year_end, year1, year2, save_opt, path_out):
    # Eventually I would like to do this with the conference
    # papers https://matplotlib.org/stable/gallery/lines_bars_and_markers/bar_label_demo.html
    x_axis = np.zeros(shape=(year_end - year_start + 1), dtype=int)
    for i in range(year_end - year_start + 1):
        x_axis[i] = year_start + i

    fig_ref = plt.figure()
    plt.bar(x_axis, year1, zorder=3)
    plt.bar(x_axis, year2, bottom=year1, zorder=3)
    fig_ref = fig_config(year_start, year_end, fig_ref)
    plt.title('Document Query Year Split Distribution')
    plt.legend(["Conferences", "Articles"])

    if save_opt > 1:
        plt.savefig(os.path.join(path_out, "Query_Year_Dist_Split.png"))
    else:
        plt.show()
    plt.close()
    return


def fig_config(x_low, x_hig, fig_ref):
    x_delim = 5
    plt.grid(linestyle='dashed', zorder=0)
    plt.title('Document Query Year Distribution')
    plt.xlabel('Year of Publication')
    plt.ylabel('Number of relevant documents')
    plt.xticks(np.arange(round_base(x_low, x_delim, "floor"), round_base(x_hig, x_delim, "ceil") + x_delim, step=x_delim))
    plt.xlim(round_base(x_low, x_delim, "floor"), round_base(x_hig, x_delim, "ceil"))
    plt.yticks(np.arange(0, 23, step=2))
    return fig_ref


def split_list(list_in, criteria, log_file):
    list_temp = list_in.copy()
    count = 0
    for i in range(len(list_in)):
        if criteria not in list_in[i][2]:
            count += 1
            list_temp.pop(i - count + 1)
    if count > 0:
        log_file.write("The list is being split based on the DOCUMENT TYPE column.\n")
        log_file.write("The split will leave all entries with the term '" + str(criteria) + "'.\n")
        log_file.write("This new list has a length " + str(len(list_temp)) + ".\n")
    print_spacer(log_file)
    return list_temp


def change_name(list_in, criteria, exclude, rename, log_file):
    count = 0
    for i in range(len(list_in)):
        chk = False
        for j in range(len(criteria)):
            if criteria[j] in list_in[i][2]:
                chk = True
            for k in range(len(exclude)):
                if chk and not exclude[k] in list_in[i][2]:
                    list_in[i][2] = rename
                    count += 1
    if count > 0:
        log_file.write("Modification of the final_query list to change the DOCUMENT TYPE column.\n")
        log_file.write("Selected entries have the keywords, " + str(criteria) + ".\n")
        log_file.write("These are then replaced by the term, '" + str(rename) + "'.\n")
    print_spacer(log_file)
    return list_in


def print_spacer(log_file):
    log_file.write("--------------------------------------------------\n")
    return


def chk_path(path):
    for i in range(len(path)):
        if not os.path.exists(path[i]):
            os.makedirs(path[i])
    return


def setup_file_out(path):
    if not os.path.isfile(path):
        file_point = open(path, "x")
    else:
        file_point = open(path, "w")
    return file_point


def print_list(file_csv_out, list_in, log_file):
    write = csv.writer(file_csv_out)
    write.writerows(list_in)
    file_csv_out.close()
    log_file.write("The final_query data has now been written to a csv file in the output folder.\n")
    print_spacer(log_file)
    return


def round_base(in_val, base_val, opt):
    temp = base_val
    if opt == "floor":
        temp = base_val * math.floor(in_val / base_val)
    else:
        temp = base_val * math.ceil(in_val / base_val)
    return temp


# Path generation.
path_list = [os.path.join(os.getcwd(), "input"), os.path.join(os.getcwd(), "output")]
chk_path(path_list)
track_log = setup_file_out(os.path.join(path_list[1], "log_query_process.txt"))
csv_out = setup_file_out(os.path.join(path_list[1], "final_query.csv"))

# Variables.
data_scopus = get_data(path_list[0], "SCOPUS_search.csv")
data_wos = get_data(path_list[0], "WEBOFSCI_search.csv")
data_ieee = get_data(path_list[0], "IEEE_search.csv")
year_end = 2024
year_start = 1982

# Main body.
track_log.write("This script will analyse the data from the different queries.\n")
print_spacer(track_log)
data_final = chk_titles(chk_titles(data_scopus, data_wos, track_log), data_ieee, track_log)
year_dist = get_years(year_start, year_end, data_final, 2, path_list[1])
track_log.write("The distribution of articles against their published year is:\n"+str(year_dist)+"\n")
print_spacer(track_log)
# Homogenize the 3rd column of the final list to make sure the corresponding type shows up correctly.
list_final = change_name(data_final, ["Conference", "Proceeding"], ["Review"], 'Conference Proceeding', track_log)
list_final = change_name(list_final, ["Article", "Journal", "Review"], ["Proceeding"], 'Journal Article', track_log)

# Now this final list needs to be split by conference and journal article
list_conf = split_list(data_final, 'Conference Proceeding', track_log)
list_arti = split_list(data_final, 'Journal Article', track_log)

# Finish the plots.
year_conf = get_years(year_start, year_end, list_conf, 0, path_list[1])
year_arti = get_years(year_start, year_end, list_arti, 0, path_list[1])
get_year_plot_sub(year_start, year_end, year_conf, year_arti, 2, path_list[1])

# Clean up the open files and perform any final processing.
print_list(csv_out, data_final,track_log)
# Closing the log file should come last.
track_log.close()
