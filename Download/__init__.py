import meetingsParser
import RPDownloader
if __name__ == "__main__":
    import raceParser
    RPDownloader.setTestMode()
    print RPDownloader.getAvailableDates()
    mset = meetingsParser.parse(RPDownloader.getMeetingsHTML(""))
    print mset.date
    for course, meeting in mset.iteritems():
        print course
        for time, race in meeting.iteritems():
            print time, race.raceid, race.title
            try: race.download()
            except raceParser.NoRaceDataError:
                continue
            print race.race
