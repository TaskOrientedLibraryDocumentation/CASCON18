# CASCON18



This is the repository accompanying the paper titled “Crowd-sourced Task-oriented Library Documentation” submitted to CASCON ’18. In this repo, you will find the scripts used to automatically create library documentation using data gathered from Stack Overflow as well as the set of results produced by our methodology and used in our survey. 

You can execute the code by running main.py as follows: `python3 main.py`. The following is a description of the components in `main.py`.

## Installing requirements 

First, make sure that CoreNLP's server is running on your computer and listening to requests on port 9000. You also need to install the python requirements to run the project. You can do so by running the following line: 

pip3 install requirements.txt


The requirements.txt file contains a list of packages needed to run the project. 

## Acquisition of related threads, task extraction and code extraction 

In order to gather all related threads of a library, we used the Stack Exchange data explorer, as well as the Stack Exchange API. The first step to gathering data about related threads is to go to [this url](https://data.stackexchange.com/stackoverflow/query/new) and use the following query to gather all the threads related to your intended library. You must replace "junit" in the following query with the tag describing your target library. 



    DECLARE @tag0 nvarchar(25) = ##tag0:string?junit##

    SELECT
      p.id as [Post Link], p.title, p.Body, p.Tags
    FROM Tags t
    JOIN PostTags pt ON pt.TagId = t.Id 
    JOIN Posts as p ON p.Id = pt.PostId
    WHERE TagName = @tag0
    ORDER BY p.ViewCount DESC


This step will gather all the information related to the threads other than their answers. After the results of the query are ready, you can download the data in a .csv file. This csv file will be used for second step of data collection. In the second step, we use the `run()` function in `main.py`. This step will identify the development tasks from the collection of threads in the .csv file, collect a list of answers for the identified task threads, extract all the code snippets from those answers, and store the results in a mongodb database. 

## Similarity detection
In order to identify all similar threads in the database, use the `find_similars()` function in `main.py`. This function will identify and store information about similar threads in the database. 

## Insights extraction
In order to train the insights classifier we use the code in `learning/nltk_classifier.py`. If you wish only to use the classifier and not train it, use [pickle](https://docs.python.org/3/library/pickle.html) to load the module stored in `learning/res.model`.

The insights used in our survey were classified per HTTP request and we did not store the insight sentences before hand. 


## Results of the methodology
We have provided a dump of our database contatining the documentation for ten well known Java libraries. You can access these results in the `dump/` folder in the repository. 

In order to restore the database you can refer to this page: https://docs.mongodb.com/manual/reference/program/mongorestore/

Also, since the tasks.bson file was larger than GitHub's limit on the file size, we had to compress the file and upload its compressed version in tasks.bson.zip. Make sure you decompress this and add it to the contents of the dump/ folder before you restore the database. The database name is "librarytasks" and there are two collections inside: "survey" which includes the survey responses and "tasks" which contains the tasks extracted using our methodology. 
