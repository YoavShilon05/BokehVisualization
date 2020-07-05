from bokeh import plotting
from typing import List, Dict
import warnings
import random

warnings.filterwarnings("ignore", category=DeprecationWarning)

class LongFormatItem:
    """a structure for an item of the "long" format."""
    def __init__(self, sample_name, wavelength, absorbance):
        self.sample_name = sample_name
        self.wavelength = wavelength
        self.absorbance = absorbance

class Plot:

    def __init__(self, title="Result"):
        plotting.output_file('result.html')

        self.plot = plotting.figure(
            title=title,
            x_axis_label = "Wavelength",
            y_axis_label="Absorbance"
        )

    def AddLine(self, sample_name, wavelengths, absorbances):

        # Generate a random color. chance of two
        color = [hex(random.randint(0, 255))[2:],
                 hex(random.randint(0, 255))[2:],
                 hex(random.randint(0, 255))[2:]]
        for i in range(len(color)):
            if len(color[i]) == 1:
                color[i] = "0" + color[i]

        color = "#" + "".join(color)
        self.plot.line(wavelengths, absorbances, legend=sample_name, color=color)

    def Save(self):
        plotting.save(self.plot)

class Formatting:
    """
    a static class for formatting csvs.
    """

    @staticmethod
    def FormatDataToLong(csv_table: Dict[str, List[float]]) -> List[LongFormatItem]:
        """
        take the given data.csv format and convert to the "long" format.
        example of the "long" format:
        [
            LongFormatItem(T001, 600, 3.20889)
            LongFormatItem(T001, 602, 3.20453)
            ...
        ]
        """
        new_csv = []

        for sample_name in csv_table.keys():
            for wavelength in range(600, len(csv_table[sample_name]) + 600, 2):
                new_csv.append(LongFormatItem(sample_name, wavelength, csv_table[sample_name][(wavelength - 600) // 2]))

        return new_csv

    @staticmethod
    def WriteLongData(long: List[LongFormatItem]):

        """
        write a long to a file.
        """

        long_content = ""

        for item in long:
            long_content += ",".join([item.sample_name, str(item.wavelength), str(item.absorbance)]) + "\n"

        with open('long.csv', 'w') as f:
            f.write(long_content)

    @staticmethod
    def ConvertOriginalCsvToDict(data : str) -> Dict[str, List[float]]:

        """Take the string of the original data.csv file and convert
        it to a dict with the name of the sample as a key and a list of
        percentages as values.
        for example:
        {
            'T001' : [3.20889,3.20453,3.20592,3.21138,3.22170,3.23109,3.23830,3.24631...]
        }
        """

        data = data.strip()
        matrix = []

        for sample in [row.split(",") for row in data.split("\n")]:
            new_sample = [sample[0]]
            for wavelength in sample[1:]:
                new_sample.append(float(wavelength))
            matrix.append(new_sample)

        dictionary = {}
        for sample in matrix:
            dictionary[sample[0]] = sample[1:]
        return dictionary

    @staticmethod
    def AddLinesToPlotByLong(plot : Plot, long : List[LongFormatItem]):

        """
        Add Lines to a plot by the "long" format.
        """

        lines : Dict[str, Dict[int : float]] = {}

        for sample in long:
            if sample.sample_name not in lines.keys():
                lines[sample.sample_name] = {}
            lines[sample.sample_name][sample.wavelength] = sample.absorbance

        for line in lines.keys():
            plot.AddLine(line, list(lines[line].keys()), list(lines[line].values()))


with open("data.csv", 'r') as f:
    processed_data = Formatting.ConvertOriginalCsvToDict(f.read())
print("formatting data to long.")
long = Formatting.FormatDataToLong(processed_data)
plot = Plot()
print("adding lines to plot")
Formatting.AddLinesToPlotByLong(plot, long)
print("writing long data to file")
Formatting.WriteLongData(long)
print("saving data to html.")
plot.Save()