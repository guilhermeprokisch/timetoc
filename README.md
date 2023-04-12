# Timetoc

Timetoc is a command-line tool for tracking work time in the timetac time tracking system. The tool allows users to add work days using the timetac API.

# Installation

To install the Timetoc Work Tracker tool, run the following command:

```console
pipx install git+https://github.com/guilhermeprokisch/timetoc.git
```

# Configuration

Add TIME_TRACK_BASE_URL as enviroment variable for the crawler works

```console
export TIME_TRACK_BASE_URL="https:\\some-timetac-login-page.com
```

# Usage



The following options are available:

  --day or -d: The date of the work day in the format yyyy-mm-dd.
  --day-str or -ds: The date of the work day in natural language. E.g 'today, yesterday'.
  --start or -s: The start time of the work day in the format hh:mm.
  --finish or -f: The finish time of the work day in the format hh:mm.
  --break-start or -bs: The start time of the break in the work day in the format hh:mm.
  --break-finish or -bf: The finish time of the break in the work day in the format hh:mm.
  --home-office or -h: Whether the day is a home office day.
  You can pass in either the --day option with a specific date or the --day-str option with a natural language date. If neither is specified, the script will prompt you for a default value of "yesterday".

You can provide the start and finish times of the work day using the --start and --finish options respectively. If you need to take a break during the work day, you can specify the start and finish times of the break using the --break-start and --break-finish options.

The --home-office option can be used to indicate whether the work day was done from home.

Once you have specified the required options, the script will use your Timetac access token to add the work day to your time tracking system. If your access token is not found, the script will prompt you to login and retrieve a new access token.

# Examples

To simply run interactively just invoke timetoc

```console
timetoc  
```

To add a work day for yesterday with a start time of 9:00 and a finish time of 17:00, you can run:

```console
timetoc  --day-str yesterday --start 9:00 --finish 17:00
```

To add a work day for a specific date, for example, March 15th, 2023, with a start time of 8:30, a finish time of 16:30, and a break from 12:00 to 12:30, you can run:

```console
timetoc  --day 2023-03-15 --start 8:30 --finish 16:30 --break-start 12:00 --break-finish 12:30```console
```

To add a work day for today that was done from home, you can run:

```console
timetoc  --day-str today --home-office
```


## Contributing

If you would like to contribute to the Timetoc Work Tracker tool, please fork the repository and submit a pull request. Contributions are always welcome!

## License

The Timetoc Work Tracker tool is licensed under the MIT License. See [LICENSE](https://chat.openai.com/chat/LICENSE) for more information.
