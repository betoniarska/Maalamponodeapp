import os
import sys
import json

class FileManager:
    def __init__(self, filename):
        self.filename = filename

    def file_exists(self):
        return os.path.isfile(self.filename)

class EntryManager:

    def __init__(self, entries):
        self.entries = entries
        
    @staticmethod
    def from_file(filename):
        with open(filename, "r") as tiedosto:
            rivit = tiedosto.readlines()
            
            entries = []
            count = 0
            entry = [0] * 6
            
            for rivi in rivit:
                rivi = rivi.strip()
                if rivi != "":

                    if count < 6:  
                        entry[count] = rivi
                    count += 1
                else:
                    if count > 0:  
                        entries.append(entry)
                        entry = [0] * 6
                        count = 0
                
            if count > 0:
                entries.append(entry)
            
            return EntryManager(entries)

    def getDates(self):
        return [entry[0] for entry in self.entries]

    def getNames(self):
        return [entry[1] for entry in self.entries]

    def getStatuses(self):
        return [entry[2] for entry in self.entries]

    def getMsgs(self):
        return [entry[4] for entry in self.entries]

    def getCounts(self, instances):

        counts = {}
        
        for instance in instances:

            if instance in counts:
                counts[instance] += 1
            else:
                counts[instance] = 1
        
        sorted_dict = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))
        return sorted_dict

    def filterByName(self, name):

        filtered = []

        for entry in self.entries:
            if entry[1] == name:

                filtered.append(entry)

        return filtered


    def filterByDate(self, date):

        filtered = []
        
        for entry in self.entries:
            onlyDate = entry[0].split(" ")
            if onlyDate[0] == date:
                filtered.append(entry)

        return filtered

    def filterByPriority(self, priority):

        filtered = []

        for entry in self.entries:
            entryPrio = entry[5]
            if priority == entryPrio[-1]:
                filtered.append(entry)

        return filtered

    def filterByStatus(self, status):

        filtered = []

        for entry in self.entries:
            if status == entry[2]:
                filtered.append(entry)

        return filtered



def main(): # testailuun
    filename = "data.txt"
    file_manager = FileManager(filename) 

    if file_manager.file_exists(): # onko file olemassa
        
        entry_manager = EntryManager.from_file(filename) # luokkainstanssi jolla on halutut tiedot

        dates = entry_manager.getDates()
        names = entry_manager.getNames()
        statuses = entry_manager.getStatuses()
        msgs = entry_manager.getMsgs()

        counts = entry_manager.getCounts(names)

        print()
        for key, value in counts.items():
            print(f'{key}: {value}', end='\n')
        print()

        data = entry_manager.filterByDate("15.05.2024")

        for entry in data:
            print(entry)
             

main()

 

