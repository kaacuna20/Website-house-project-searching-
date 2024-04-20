<div class="row ">
	<div class="col ">
		<h1  style="color:#C6AB7C; font-size: 80px; font-weight:bold;">HOUSE FINDER</h1>
	</div>
</div>

<h4 style="text-align: justify">In the Atlantico department - Colombia, there are many housing projects, of many types (VIS, VIP, NO VIS) where people of all classes can get their own home, but there are many options and I thought the following, why not create a website where people can search all options in one site instead to do it website by website? I decided start to create my first big project, using my knowlegde of HTML, CSS,Bootstrap, Python and Flask.</h4> 

### Features of website

- Let view housing projects in Atlantico - Colombia, specifically in Puerto Colombia, Barranquilla and Soledad city, filter the search by construction company, location and city;
- User can register and login section, personalize their profiles and save their favorites projects on their accounts;
- got the option to change their passwords or get a new password in section forgot password where the new password is sent to their email;
- Each project page there is a comment section where each user can leave their opinions about the project;
- There is a section for developer where can read the documentation about the API, whatching the routes to make the requests, the differents responses and restrictions;
- Developers can generate their apikey to be allowed making requests;

### Instalation
#### On Windows type:

`$ python -m pip install -r requirements.txt`
#### On MacOS type:

`$ pip3 install -r requirements.txt`

<p style="text-align: justify">I always wanted to create a website where both, users and developers can access the information, so, I decided created a section for users where can create their acount and save their favorites projects and section for developers through a RESTful API.</p>

### Steps
<p style="text-align: justify">Having clear my goals, I started creating the main templates, I relied on '@ajlkn's' template from https://html5up.net/ and Flask-Bootstrap, later I created the database and their relationships using Flask-SQLAlchemy, the scheme is file 'Model database.pdf', the images like user photo profile, logos and background images were store in database like string of routes, either using the link directly from the web page where it was scraped or writing the path to the static folder, and go creating the routes using Flask. The funcionality of these relationships should allow users to filter at the moment to search by any item, like city, location or company, and also to save any project on their profiles.</p>

<p style="text-align: justify">In parallel, I was editing the templates with Jinja2, using the file 'form' and generate the forms to register and login users, comments form and forgot password using WTForms and this let me managed the information since the frontend with database, CKEditor for the comment section and storage in database.</p>

<p style="text-align: justify">After that, I focus on authorization and authentication with Flask-login and Werkzeug, the passwords were encrypted with SHA-256 with salting.</p>

<p style="text-align: justify">Next step was creating the routes for API requests and to authenticate them with a token or apikey by user, two routes GET to get json response with information about projects, one POST response to post a record about a new project that's not stored in database, PATCH to update a price of any project, because the prices are dynamics and they are changing over time and DELETE to delete a record project but just allowed by administer token, all of these using jsonify to make the response and JWT to generate and validate the token by using decorator functions (wraps), to test the API I used Postman.</p>

<p style="text-align: justify">Finally, I start to clean the code and tmeplates, fill the project class table using the project "web_scrapping_database", save the sensible information in enviroment variables.</p>
