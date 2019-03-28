import csv

with open("dance_data/data_26-March/chicken_YC.txt","r") as fin:
    with open("dance_data/processed_data/chicken.txt","a") as fout:
        writer=csv.writer(fout)
        for row in csv.reader(fin):
            writer.writerow(row[0:15]+[1])