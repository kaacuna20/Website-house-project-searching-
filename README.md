<div class="row ">
							<div class="col ">
								<h1  style="color:#C6AB7C; font-size: 80px; font-weight:bold;">HOUSE <br />FINDER</h1>
							</div>
							<div class="col">
								<img src="https://github.com/kaacuna20/Website-house-project-searching-/blob/master/static/images/logo.gif" style="border-radius: 8px;" class="d-block mx-lg-auto img-fluid" width="200" height="200">
							</div>
						</div>


In the Atlantico department - Colombia, there are many housing projects, of many types (VIS, VIP, NO VIS) where people of all classes can get their own home, but there are many options and I thought the following, why not create a website where people can search all options in one site instead to do it website by website? I decided start to create my first big project, using my knowlegde of HTML, CSS, Python and Flask. 

First, I always wanted to create a website where both users and developers can access the information, so, I decided created a section for users where can create their acount and save their favorites projects and section for developers through a RESTful API.

Having clear my goals, I started creating the main templates, I relied on '@ajlkn's' template from https://html5up.net/ and Flask-Bootstrap, later I created the database and their relationships using Flask-SQLAlchemy, the scheme is file 'Model database.pdf' , and go creating the routes using Flask. The funcionality of these relationships should allow users to filter at the moment to search by any item, like city, location or company, and also to save any project on their profiles.

In parallel, I was editing the templates with Jinja2, using the file 'form' and generate the forms to register and login users using WTForms and this let me managed the information since the frontend with database, CKEditor for the comment section and storage in database.

After that, I focus on authorization and authentication with Flask-login and Werkzeug, the users password were encrypted with HAS-256 with salting.

Next step was creating the routes for API requests and to authenticate them with a token or apikey by user, two routes GET to get json response with information about projects, one POST response to post a record about a new project that's not stored in database, PATCH to update a price of any project, because the prices are dynamics and they are changing over time and DELETE to delete a record project but just allowed by administer token, all of these using jsonify to make the response and JWT to generate and validate the token by using decorator functions (wraps), to test the API I used Postman.

Finally, I start to clean the code and tmeplates, fill the project class table using the project "web_scrapping_database", save the sensible information in enviroment variables.
