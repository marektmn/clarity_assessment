# Clarity.ai Assessment
### Execution instructions
Dependencies are managed using `pip` to install required packages/libraries execute  `pip3 install -r requirements.txt`

`python3 parser.py --help` to explore the possibilities/switches available for _parser.py_  
`python3 generator.py --help` to explore the possibilities/switches available for _generator.py_

Example usage:  

`python3 example-input.txt -p -t -host Adeline -init 1565647204351 -end 1565684881706`  
To parse `example-input.txt` for given hostname `Adeline` during given time period `-init` <-> `-end` using `-t` unix timestamps.

`python3 example-input.txt -p -host Adeline -init 2019-08-12T22:00:04+00:00 -end 2019-08-13T08:28:31Z`  
To parse `example-input.txt` for given hostname `Adeline` during given time period `-init` <-> `-end` using ISO formatted datetimes.

For _unlimited input parser_ is adviced to use `tmux` or two shell windows to run `generator.py` and `parser.py` concurrently.
`python3 generator.py example-input.txt` will start appending log entries to `example-input.txt`infinitely, while running
`python3 parser.py input.txt -host Suzu` would yield desired outputs for hostname `-host Suzu`. For further customization look for documentation in `--help` and into implementation.

### Author's notes
Some things I want to mention related to my solution. Regarding provided `input-file-10000.txt`, I've found the timestamps I little off, as their length seemed invalid (13) where valid unix timestamps have length of 10 characters. Trimming their length solved this issue. For the first goal I opted for ISO formatted UTC/Zulu/GMT datetimes as an input as well as unix timestamps. In the description you mentioned that timestamps are "roughly sorted" and they might differ by 5 minutes. To address I decided to extend the `initial` and `end` datetimes to cover possible leaks (I hope I did well).

To address _unlimited input parser_ issue I opted for creating a small script which would generate `input-file-10000.txt`-like log from a subset of `hosts` infinitely and randomly. To solve the the task and provide memory and CPU efficient solution, multiple approaches could be valid. I opted for simple, yet elegant using `subprocess` and `tail`, after some research using `mmap` or using python's context manager `.tell()`, `.seek()` approach appeared working, performance could be a subject for further investigation. I apologize for insufficient/partial test coverage.

### Example command line output
![cmd_output](https://github.com/marektmn/clarity_assessment/blob/master/img/cmd_output.png
