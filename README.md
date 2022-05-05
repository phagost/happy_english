# Happy English project

## Building database

All subtitles data from TEDtalks are stored inside `subtitles.db`. To renew it, the `SubtitleLoader` script may be used. The script downloads all subtitles from numerated TEDtalks. To change the interval for search, one has to change the following line in the `if __name__ == '__main__'` part of the code:

    sub_load.add_ids(first_video_id, last_video_id)

Currently, the interval is from 1 to 1000.

## Using web-interface

To run the server, `main.py` script should be invoked. The server will run on the http://127.0.0.1:5000/ address. Then:

* The desired phrase should be entered
* The input will provide the parts of subtitles with the desired phrase
* Link and timecodes to the corresponding TEDtalk will be provided