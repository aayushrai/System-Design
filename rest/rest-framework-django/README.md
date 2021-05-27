# python_test


## Create instance

```
URL Format: ""
Example URL : http://127.0.0.1:8000
Request type : POST

Post-data-Format:-

{
"audioFileType":"audiofiletype",   
"audioFileMetadata":{}
}

Post-data-Example:-
 
{
"audioFileType":"audiobook",
"audioFileMetadata":{"Title":"AOT","Duration":50,"Author":"KK","Narrator":"UU"}
}


```

![image](https://github.com/aayushrai/python_test/blob/master/images/create.png)

## Update instance

```
URL format: "audiofiletype/id"
Example URL : http://127.0.0.1:8000/podcast/1
Request type : PUT

Put-data-Format:-

{
"audioFileType":"audiofiletype",   
"audioFileMetadata":{}
}

Post-data-Example:-
 
{
"audioFileType":"podcast",
"audioFileMetadata":{"Name":"AOT","Duration":50,"Host":"KK","Participants":[]}
}


```

![image](https://github.com/aayushrai/python_test/blob/master/images/update.png)

## Get all instance

```
URL: "audiofiletype"
Example URL : http://127.0.0.1:8000/song
Request type : GET

```

![image](https://github.com/aayushrai/python_test/blob/master/images/getAll.png)


## Get single instance

```
URL: "audiofiletype/id"
Example URL : http://127.0.0.1:8000/song/1
Request type : GET

```

![image](https://github.com/aayushrai/python_test/blob/master/images/getSingle.png)

## Delete single instance

```
URL: "audiofiletype/id"
Example URL : http://127.0.0.1:8000/song/1
Request type : DELETE

```

![image](https://github.com/aayushrai/python_test/blob/master/images/delete.png)


