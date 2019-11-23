DC@LAK20 Dataset Description:
---
There are two datasets: train and predict. Train has learning data from the previous year's course and contains four main types of files: EventStream, LectureMaterial, LectureTime, QuizScore. Predict contains the same files except QuizScore, which is the prediction target.
The details of the file columns are described below.
Course_#_EventStream.csv (Reading event logs):
----
userid      Anonymized student userid, eg: 335b81af-7e60-4a04-8712-ed734eccbf62
contentsid  The id of the e-book that is being read
operationname   The action that was done, eg:
            OPEN : opened the book
            CLOSE : closed the book
            NEXT : went to the next page
            PREV : went to the previous page
            PAGE_JUMP : jumped to a particular page
            ADD BOOKMARK : added a bookmark to current page
            ADD MARKER : added a marker to current page
            ADD MEMO : added a memo to current page
            CHANGE MEMO : edited an existing memo
            DELETE BOOKMARK : deleted a bookmark on current page
            DELETE MARKER : deleted a marker on current page
            DELETE_MEMO : deleted a memo on current page
            LINK_CLICK : clicked a link contained in the e-book current page
            SEARCH : searched for something within the e-book
            SEARCH_JUMP : jumped to a page from the search results
pageno      The current page where the action was performed
marker      The reason for the marker added to a page, eg: important, difficult (contents are not understood)
memo_length The length of the memo that was written on the page
devicecode  type of device used to view BookRoll, eg: mobile, pc
eventtime   the timestamp of when the event occurred
Course_#_LectureMaterial.csv (Contents and lecture details):
----
lecture     The lecture number
contentsid  The id of the contents used in the lecture
pages       The total number of pages in the contents
Course_#_LectureTime.csv (Lecture details):
----
starttime   The time at which the lecture started
endtime     The time at which the lecture ended
lecture     The lecture number
Course_#_QuizScore.csv (Student performance details):
----
userid      Anonymized student userid, eg: 335b81af-7e60-4a04-8712-ed734eccbf62
score       The final total score out of 100 that the student received for the course
