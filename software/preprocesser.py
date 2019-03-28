import csv

with open("dance_data/data_26-March/chicken_Harsh.txt","r") as fin:
    with open("dance_data/processed_data/chicken.txt","w") as fout:
        writer=csv.writer(fout)
        for row in csv.reader(fin):
            writer.writerow(row[:-1])