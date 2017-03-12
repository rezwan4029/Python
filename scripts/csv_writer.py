import tempfile

import cStringIO, codecs
import csv


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


file_location = tempfile.mkdtemp() + '/report.csv'
print "File create in location =>" + file_location

f = open(file_location, "wb")
output = UnicodeWriter(f)

output.writerow(['Id', 'Name', 'Email'])
for i in xrange(1, 21):
    ID = str(i)
    NAME = "Name_" + ("{0:0>3}".format(i))
    EMAIL = "user" + str(i) + "@gmail.com"
    output.writerow([ID, NAME, EMAIL])
