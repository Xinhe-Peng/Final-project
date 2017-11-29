# Title: Restaurant Queuing Simulation System

## Team Member(s): Mingwei Gao, Xinhe Peng, Yikai Deng

# Monte Carlo Simulation Scenario & Purpose:

### Hypothesis before running the simulation:

This is a simulation system to get :
- average waiting time of customers, 
- how many groups of customers are remained,
- and which table does current group of customers is assigned to.

Groups who came first would be served first. (FIFO)
Groups have to register and wait for being assigned to available tables.
No reservation.

The restaurant has:
- 6 tables for groups of up to two customers (No.1 to N0.6), 
- 4 tables for groups of up to four customers (No.7 to No.10), 
- and 2 tables for groups of up to six customers (No.11 and No.12).

Groups would be divided into three queues, based on the number of customers in th groups.

There are two types of groups: VIP, and non-VIP.
VIP groups have the privilege of jumping into the queue. VIP group could be moved forward by four steps.
For example, if one VIP group comes, and it should be the seventh in the queue of groups of up to two customers, it could be moved forward by four and become the third in queue. 


### Simulation's variables of uncertainty:

- Time (in minutes) each group of customers would spend:
  - unif(30,150) 
- The numbers of customers in groups:
  - minimum:1, maximum:6
  and whether this group is the VIP group
  - the probability that the group is a VIP group is 8%.
- Registration time

## Instructions on how to use the program:


## Sources Used:

