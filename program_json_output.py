#!/usr/local/bin/python3
import json
import os
import xml.etree.ElementTree as ET
import timeit
from logger import Logger
import numpy as np
import re

# create a function that looks up current directory

class Program:
    def __init__(self):
        this_folder = os.path.dirname(__file__)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        print(dir_path)

        # delete parent directories to make it faster
        # data_folder = os.path.join(this_folder, os.pardir, os.pardir, "data")
        data_folder = os.path.join(this_folder, "data")
        self.data_folder = os.path.abspath(data_folder)
        self.logger = Logger(os.path.join(self.data_folder, "log.txt"))

    def run(self):
        try:
            self.log_startup()
            self.load_xml()
            # self.load_json()
            # self.load_csv()
        except Exception as e:
            print(e.__repr__())


    def log_startup(self):
        self.logger.log("Application starting up...")
        self.logger.log("Data folder: {0}".format(self.data_folder))

    def load_xml(self):
        filename = os.path.join(self.data_folder, "michael-kennedy-blog.xml")
        # filename = os.path.join(self.data_folder, "micheal-ken-notes.xml")

        # https://docs.python.org/3/library/re.html
        modified_string = re.findall("""http://0.gravatar.com/avatar/cb053688f95dbebf60e5c19a3d05110c?
            s=96&amd;d=identicon&amd;r=G" medium="image""", filename)

        print('MODIFIEDSTRING**************************',modified_string)
        self.logger.log("Loading XML file: {0}".format(filename))
        dom = ET.ElementTree()
        print(dom)
        dom.parse(filename)
        root = dom.getroot()
        print(root)     
        # root = dom.fromstring(filename)
        # print(root)

        print("Titles of recent posts:")
        items = list(dom.findall("channel/item"))
        self.logger.log("Found {0} titles in RSS feed.".format(len(items)))
        for item in items:
            print("{0} [{1}]".format(
                item.find("title").text,
                item.find("link").text))
        print()

    def load_json(self):
        filename = os.path.join(self.data_folder, "python-course.json")
        self.logger.log("Loading JSON file: {0}".format(filename))



        with open(filename, "r") as fin:
            data = json.loads(fin.read())
            print("Course title: {0}".format(data["Name"]))
            self.logger.log("Found course title to be: {0}".format(data["Name"]))
            engagements = data["Engagements"]
            print("Number of engagements: {0}".format(len(engagements)))
            print("Locations:")
            with open('data/json_output.txt', 'w') as output_file:
                    json.dump(engagements, output_file)
                    # json.dump(data, output_file)
            for e in engagements:
                print("\t" + e["City"] + " on " + e["StartDate"] + " [active? " + str(e["ActiveEngagement"]) + "]")



        print()


    def load_csv(self):
        filename = os.path.join(self.data_folder, "fx-seven-day.csv")
        self.logger.log("Loading CSV file: {0}".format(filename))

        # Answer what is the 7 day average for RUPEEs to USD?
        # (need to go from rupees -> canadian dollars -> usd)

        lookup = self.build_currency_lookup(filename)
        rupee = lookup["INR"]
        usd = lookup["USD"]
        rupees_per_canadian_dollar = self.average(rupee["values"])
        usa_per_canadian_dollar = self.average(usd["values"])

        rupee_per_usd = usa_per_canadian_dollar / rupees_per_canadian_dollar

        print("1 USD is worth {0} Rupees.".format(rupee_per_usd))
        self.logger.log("1 USD is worth {0} Rupees.".format(rupee_per_usd))

        ##########################

        # df = pd.read_csv('data/fx-seven-day.csv')
        # print(df)

    # try one lining it 
    @staticmethod
    def build_currency_lookup(filename):
        lookup = dict()
        with open(filename, "r") as fin:
            for line in fin:
                if line is None:
                    continue
                if line.strip().startswith("#"):
                    continue
                if line.strip().startswith("Date"):
                    continue

                parts = line.split(sep=',')
                nums = np.arange(2,9)
                for i in nums:
                    entry = {
                        "name": parts[0].strip(),
                        "key": parts[1].strip(),
                        "values": [
                            float(parts[i])
                        ]
                    }

                lookup[entry["key"]] = entry
        return lookup

    @staticmethod
    def average(numbers):
        if len(numbers) <= 0:
            return float('nan')

        return sum(numbers) / float(len(numbers))


if __name__ == "__main__":
    p = Program()
    p.run()

