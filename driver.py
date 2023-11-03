from greenbutton.parse import *
import matplotlib.pyplot as plt
import re

if __name__ == '__main__':
    usage_plots = []
    total_usages = []
    averages = []
    names = []

    customers = ['testdata/Desert_Multi_Family_Jan_1_2011_to_Jan_1_2012_RetailCustomer_6.xml', 'testdata/Coastal_Multi_Family_Jan_1_2011_to_Jan_1_2012_RetailCustomer_5.xml', 'testdata/Inland_Multi_Family_Jan_1_2011_to_Jan_1_2012_RetailCustomer_8.xml']
    for i in range(len(customers)):
        customer = parse_feed(customers[i])
        usage_plots.append([])
        total_usages.append(0)

        pattern = re.compile(r'\/(.*?)_(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)')
        match = pattern.search(customers[i])
        if match:
            names.append(match.group(1).replace('_', ' '))
        else:
            names.append('Not Found')

        for data in customer:
            print(data.title)
            print(data.serviceCategory)
            print('Meter Readings:')
            for reading in data.meterReadings:
                for block in reading.intervalBlocks:
                    print('Interval: '+ str(block.interval))
                    print('Readings: ')
                    for intervalReading in block.intervalReadings:
                        print('Value: ' + str(intervalReading.value) + ' Wh, Time Period: ' + str(intervalReading.timePeriod))
                        usage_plots[i].append(intervalReading.value)
                        total_usages[i] += intervalReading.value

                    print()

        average_hour_use = total_usages[i] / len(usage_plots[i])
        averages.append(average_hour_use)
        print('Average use: ' + str(average_hour_use) + ' Wh/h')

    fig, axs = plt.subplots(len(usage_plots))

    for i in range(len(usage_plots)):
        axs[i].plot(usage_plots[i])
        axs[i].set_title('Hourly Energy Usage For a '+names[i]+' Household')
        axs[i].set_xlabel('Total Hours (h)')
        axs[i].set_ylabel('Energy Usage (Wh)')

    fig.tight_layout()
    plt.show()