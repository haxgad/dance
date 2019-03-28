import csv

#append chicken data - 1 
# with open("dance_data/data_26-March/chicken_J.txt","r") as fin:
#     with open("dance_data/processed_data/chicken.txt","a") as fout:
#         writer=csv.writer(fout)
#         for row in csv.reader(fin):
#             writer.writerow(row[0:15]+[1])

#append cowboy data - 2
# with open("dance_data/data_26-March/cowboy_YC_2.txt","r") as fin:
#     with open("dance_data/processed_data/cowboy.txt","a") as fout:
#         writer=csv.writer(fout)
#         for row in csv.reader(fin):
#             writer.writerow(row[0:15]+[2])

#append crab data - 2
# with open("dance_data/data_26-March/crab_YC.txt","r") as fin:
#     with open("dance_data/processed_data/crab.txt","a") as fout:
#         writer=csv.writer(fout)
#         for row in csv.reader(fin):
#             writer.writerow(row[0:15]+[3])

#append hunchback data - 4
# with open("dance_data/data_26-March/hunchback_YC.txt","r") as fin:
#     with open("dance_data/processed_data/hunchback.txt","a") as fout:
#         writer=csv.writer(fout)
#         for row in csv.reader(fin):
#             writer.writerow(row[0:15]+[4])

#append raffles data - 5
with open("dance_data/data_26-March/raffles_jason.txt","r") as fin:
    with open("dance_data/processed_data/raffles.txt","a") as fout:
        writer=csv.writer(fout)
        for row in csv.reader(fin):
            writer.writerow(row[0:15]+[5])

