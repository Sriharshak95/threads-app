# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* Quick summary
* Version
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### How do I get set up? ###

* Summary of set up
* Configuration
* Dependencies
* Database configuration
* How to run tests
* Deployment instructions

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact

### Urls/api list :

* Card/Bookcover 
	
	1.To create the 
	  Url= /threadcard/api/addbookcover/

	json formate:
		{  
		"name": "Name of the card",
		"description": "just give brief about card",
		"image": upload single image,
		"created_by": pass the creator user ID, 
		}
	created by is compulsary, rest all accepts nullable.

	2.To Edit: 
		
	  Url= /threadcard/api/editbookcover/(<bookcover ID>/

		pk is id of perticular card
	3. To List all Cards:
	   Url=/threadcard/api/listbookcover/
		

*  Thread Cards

	1. to crate a ThreadCard i.e posting all thread data at once to create card for the first time

 	   Url= /threadcard/api/createthread/

	json formate:
		[{"name":"CP-1","message":"ondu","bookcoverowner":4,"bookcover":19},
		{"name":"CP-2","message":"eradu","bookcoverowner":4,"bookcover":19},
		{"name":"CP-4","message":"test12344","bookcoverowner":4,"bookcover":19},
		{"name":"CP-5","message":"yesfe","bookcoverowner":4,"bookcover":19}]

	name is optinal remaining is compulsary, message is content/comment of thread . bookowner is creator User-ID. and bookcover is Main 		thread ID. 

	2. to create a single card, which helps in adding the new card after creating the Thread:
	   
	   Url= /threadcard/api/addthread/

	json formate:
		{
		"name": "optional",
		"message": "Comment message here",
		"bookcoverowner": Creator ID,
		"bookcover": Bookcover/Card ID
		}

	3. To list All the Threads Wrt Card/Bookcover 
      	   url= /threadcard/api/listthread/(<bookcover ID>)/


	4. to Edit Indivisual Thread

       	   url= /threadcard/api/editthread/(<threadcard ID >)/

* Subcomments:
	1. Adding sub comment:
		url = /threadcard/api/addsubcomment/
		{
		    "comment": "",
		    "thread": 1,
		    "created_by": 2
		}
	2. edit :
		url = /threadcard/api/editsubcomment/(<subcomment ID >)/

       	3. List adll subcomments of thread .
		
		Url= /threadcard/api/listsubcomment/(<Thread ID>)/


