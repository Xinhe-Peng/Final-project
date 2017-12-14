import numpy as np


def mod_pert_random(low, likely, high, confidence=4, samples=30):
    """Produce random numbers according to the 'Modified PERT'
    distribution.

    :param low: The lowest value expected as possible.
    :param likely: The 'most likely' value, statistically, the mode.
    :param high: The highest value expected as possible.
    :param confidence: This is typically called 'lambda' in literature
                        about the Modified PERT distribution. The value
                        4 here matches the standard PERT curve. Higher
                        values indicate higher confidence in the mode.
    :param samples: The amount of number to generate, default value is 30.
    Formulas from "Modified Pert Simulation" by Paulo Buchsbaum.
    """
    # Check minimum & maximum confidence levels to allow:
    confidence = min(8, confidence)
    confidence = max(2, confidence)

    mean = (low + confidence * likely + high) / (confidence + 2)

    a = (mean - low) / (high - low) * (confidence + 2)
    b = ((confidence + 1) * high - low - confidence * likely) / (high - low)

    beta = np.random.beta(a, b, samples)
    beta = beta * (high - low) + low
    return beta


class Queue:
    def __init__(self):
        self.groups = []

    def queue_size(self):
        return len(self.groups)

    def isEmpty(self):
        if len(self.groups) > 0:
            return False
        else:

            return True

    def add_queue(self, group):
        if group.get_vip():  # If current group is a VIP group, move it forward by four groups,
            enterQueue = False
            if len(self.groups) >= 4:
                for i in range(0, 4):
                    if self.groups[i].get_vip():
                        self.groups.insert(i, group)
                        enterQueue = True
                        break
                if (enterQueue is False):
                    self.groups.insert(4, group)
            elif len(self.groups) > 1 and len(self.groups) < 4:
                for i in range(0, len(self.groups)):
                    if self.groups[i].get_vip():
                        self.groups.insert(i, group)
                        enterQueue = True
                        break
                if (enterQueue is False):
                    self.groups.insert(1, group)
            elif len(self.groups) <= 1:
                self.groups.insert(0, group)
        elif group.get_vip() is False:
            self.groups.insert(0, group)

    def del_queue(self):  # delete last=delete first come group
        return self.groups.pop()


class Table:
    def __init__(self, num, size):
        self.num = num  # No. of the table
        self.size = size  # Size of the table: for group of up to 2, 4 or 6.

        self.currentGroup = None  # Is the table occupied or not.

    def busy(self):
        if self.currentGroup != None:
            return True
        else:
            return False

    def startNext(self, newGroup):
        self.currentGroup = newGroup

    def cleanTable(self):  # when one group finish their meal, set their table's current group to none
        self.currentGroup = None

    def get_num(self):
        return self.num


class Group:
    def __init__(self, time, size, vip, groupID):
        self.timestamp = time  # Time when group registered (entered into the queue)
        self.size = size  # randomly define size from 1 - 6
        self.vip = vip  # Whether the group is a vip group
        self.table = None  # Which table the group will be assigned to
        self.timeRequest = mod_pert_random(0, 45, 120, samples=1).astype(int)  # How long will the group spend
        self.groupID = groupID

    def get_groupID(self):
        return self.groupID

    def get_stamp(self):
        return self.timestamp

    def get_size(self):
        return self.size

    def wait_time(self, current_time):
        return current_time - self.timestamp

    def get_vip(self):
        return self.vip

    def get_time_request(self):
        return self.timeRequest


def tablesSetting(number_tables_2, number_tables_4, number_tables_6):
    """

    :param number_tables_2: number of tables for groups with one or two customers. (6)
    :param number_tables_4: number of tables for groups with three or four customers. (4)
    :param number_tables_6: number of tables for groups with five or six customers. (2)
    :return: three lists, each for one type of tables, and the elements in every list are Table Objects.
    >>> t2,t4,t6 = tablesSetting(6,4,2)
    >>> len(t2)
    6
    >>> len(t4)
    4
    >>> len(t6)
    2
    """
    table_2_list = []
    table_4_list = []
    table_6_list = []
    for i in range(number_tables_2):
        table_2_list.append(Table(i, 2))

    for i in range(number_tables_4):
        table_4_list.append(Table(i + number_tables_2, 4))

    for i in range(number_tables_6):
        table_6_list.append(Table(i + number_tables_4 + number_tables_2, 6))

    return (table_2_list, table_4_list, table_6_list)


def TableFinish(current_time, nextGroup_endTime, table_type):
    if (current_time in nextGroup_endTime.values()):
        for n in list(nextGroup_endTime.keys()):
            if current_time == int(nextGroup_endTime[n]):
                if len(table_type)==6:
                    table_type[n].cleanTable()
                elif len(table_type)==4:
                    table_type[n-6].cleanTable()
                elif len(table_type)==2:
                    table_type[n-10].cleanTable()


def simulation(current_time, table, queue, total_time, total_timeR, nextGroup_endTime):
    """
    Simulation at one specific time point (current_time)
    :param current_time: time point, at which current simulation is running.
    :param table:
    :param queue: queue for groups
    :param total_time:
    :param total_timeR: list, storing waiting time for each group served or is being served
    :param nextGroup_endTime:
    """
    TableFinish(current_time, nextGroup_endTime, table)

    for t in table:
        if (t.busy() == False) and (not queue.isEmpty()):
            nextGroup = queue.del_queue()
            t.startNext(nextGroup)
            print('Group No.', nextGroup.get_groupID(), 'will be assigned to Table', t.get_num(), '.\n'
                                                                                                  'Their waiting time is',
                  nextGroup.wait_time(current_time), 'minute(s).\n')
            # Update the ending time for tables
            nextGroup_endTime[t.get_num()] = current_time + nextGroup.get_time_request() + 2
            total_timeR.append(int(nextGroup.get_time_request()) + 2)

            # Simulation duartion is done, for groups who are not assigned
    if current_time == total_time - 1:  # total_time: Duration
        at_least_waittime = []
        for i in range(queue.queue_size()):
            if len(nextGroup_endTime) > 0:
                next_finish_time = min(nextGroup_endTime.values())
                next_finish_table = min(nextGroup_endTime, key=nextGroup_endTime.get)
                unpro_next = queue.del_queue()

                print('Group', unpro_next.get_groupID(), 'needs to wait',
                      int(unpro_next.wait_time(next_finish_time)), 'minute(s) to be assigned.')
                at_least_waittime.append(int(unpro_next.wait_time(next_finish_time)))
                nextGroup_endTime.pop(next_finish_table)
            else:
                unpro_next = queue.del_queue()
                print('There are still', i, 'Groups in front of Group No.',
                      unpro_next.get_groupID(), 'they need to wait at least', max(at_least_waittime),
                      'minute(s) to be assigned.')
        # avg_timeR = sum(total_timeR)/len(total_timeR)


def generation(Duration, amount):
    """

    :param Duration:
    :param amount:
    """
    # Generate group sizes, the total group number is "amount"， the number of people in each group is between 1 and 6
    size = np.random.randint(1, 7, amount)
    # Generate vip situation, based on the probability of 8%
    vip = []
    for i in range(amount):
        num = np.random.randint(0, 101, 1)
        if (num >= 0) & (num <= 8):
            vip.append(True)
        else:
            vip.append(False)
    # Generate the registration time for each group
    timestamp_list = mod_pert_random(0, Duration // 2, Duration, samples=amount).astype(int)
    timestamp_list = list(timestamp_list)

    counter = 0
    queue_2 = Queue()
    queue_4 = Queue()
    queue_6 = Queue()

    table_2, table_4, table_6 = tablesSetting(6, 4, 2)  # Initializing tables

    total_timeR_2 = []  # For calculating total average waiting time
    nextGroup_endTime_2 = {}  # {No. of table: the ending time of the table}

    total_timeR_4 = []
    nextGroup_endTime_4 = {}
    total_timeR_6 = []
    nextGroup_endTime_6 = {}

    groupNumb = 0  # all group have their unique ID

    for i in range(Duration):
        # print(i,'/n')
        while i in timestamp_list:
            # print(size[counter],'**')
            if size[counter] == 1 or size[counter] == 2:
                queue_2.add_queue(Group(i, 2, vip[counter], groupNumb))
                counter += 1
                groupNumb += 1
            elif size[counter] == 3 or size[counter] == 4:
                queue_4.add_queue(Group(i, 4, vip[counter], groupNumb))
                counter += 1
                groupNumb += 1
            elif size[counter] == 5 or size[counter] == 6:
                queue_6.add_queue(Group(i, 6, vip[counter], groupNumb))
                counter += 1
                groupNumb += 1
            timestamp_list.remove(i)  # Deal with the situation that several groups arrive at the same time point

        # Run the simulation
        simulation(i, table_2, queue_2, Duration, total_timeR_2, nextGroup_endTime_2)
        simulation(i, table_4, queue_4, Duration, total_timeR_4, nextGroup_endTime_4)
        simulation(i, table_6, queue_6, Duration, total_timeR_6, nextGroup_endTime_6)

        # Summary
        if i == Duration-1:
            print("Total groups served (groups who finished their meal or on the table currently):",
                  len(total_timeR_2)+len(total_timeR_4)+len(total_timeR_6))
            avg=(sum(total_timeR_2)+sum(total_timeR_4)+sum(total_timeR_6))/(len(total_timeR_2)+len(total_timeR_4)+len(total_timeR_6))
            print('Average waiting time for groups served: {0:.2f}'.format(avg), "minute(s)")


def client():
    print('Welcome to Restaurant Queuing Simulation System!')
    print('Please enter the total time (integer) you want for simulation:')
    duration=int(input())
    print('Please enter the total groups of customers you predict the restaurant would have:')
    groups=int(input())
    generation(duration, groups)

client()
