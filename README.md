<div class="row ">
	<div class="col ">
		<h1  style="color:#C6AB7C; font-size: 80px; font-weight:bold;">HOUSE FINDER</h1>
	</div>
</div>

<h4 align="justify">In the Atlantico department - Colombia, there are many housing projects, of many types (VIS, VIP, NO VIS) where people of all classes can get their own home, but there are many options and I thought the following, why not create a website where people can search all options in one site instead to do it website by website? I decided start to create my first big project, using my knowlegde of HTML, CSS,Bootstrap, Python and Flask.</h4> 

### Features of website

- Let view housing projects in Atlantico - Colombia, specifically in Puerto Colombia, Barranquilla and Soledad city, filter the search by construction company, location and city;
- User can register and login section, personalize their profiles and save their favorites projects on their accounts;
- got the option to change their passwords or get a new password in section forgot password where the new password is sent to their email;
- Each project page there is a comment section where each user can leave their opinions about the project;
- There is a section for developer where can read the documentation about the API, whatching the routes to make the requests, the differents responses and restrictions;
- Developers can generate their apikey to be allowed making requests;

### Virtual Enviroment

`$ python -m virtualenv venv`

#### Execute virtualenv:

#### On Windows type:
`$ venv\Scripts\activate`

#### On MacOS type:
`$ source venv/Scripts/activate`

### Instalation
#### On Windows type:

`$ python -m pip install -r requirements.txt`
#### On MacOS type:

`$ pip3 install -r requirements.txt`

<p align="justify">I always wanted to create a website where both, users and developers can access the information, so, I decided created a section for users where can create their acount and save their favorites projects and section for developers through a RESTful API.</p>

### Steps
<ol>
	<li>
		<p align="justify">
		     Having clear my goals, I started creating the main templates, I relied on <strong>'@ajlkn's'</strong> template from https://html5up.net/ and Flask-Bootstrap, later I 
                     created the database and their relationships using <strong>Flask-SQLAlchemy</strong>, the scheme is file <strong>"Model database.pdf"</strong>, the images like user 
                     photo profile, logos and background images were store in database like string of routes, either using the link directly from the web page where it was scraped or 
                     writing the path to the static folder, and go creating the routes using <strong>Flask</strong>. The funcionality of these relationships should allow users to filter 
                     at the moment to search by any item, like city, location or company, and also to save any project on their profiles.
		</p>
 	</li>
	<li>
	<p align="justify">
		In parallel, I was editing the templates with <strong>Jinja2</strong>, using the file 'form' and generate the forms to register and login users, comments form and forgot 
                password using <strong>WTForm</strong>s and this let me managed the information since the frontend with database, <strong>CKEditor</strong> for the comment section and 
                storage in database.
	</p>
 	</li>
	<li>
		<p align="justify">After that, I focus on authorization and authentication with <strong>Flask-login</strong> and <strong>Werkzeug</strong>, the passwords were encrypted 
                with algorithm SHA-256 and adding a salting.
		</p>
 	</li>
	<li>
		<p align="justify">
		Next step was creating the routes for API requests and to authenticate them with a token or apikey by user, two routes GET to get json response with information about 
                projects, one POST response to post a record about a new project that's not stored in database, PATCH to update a price of any project, because the prices are dynamics 
                and they are changing over time and DELETE to delete a record project but just allowed by administer token, all of these using jsonify to make the response and 
                <strong>JWT</strong> to generate and validate the token by using decorator functions (wraps), to test the API I used <strong>Postman.</strong>
		</p>
	 </li>
	<li>
		<p align="justify">
			Finally, I start to clean the code and templates, fill the project class table using the project <a href="https://github.com/kaacuna20/webscraping-construction- 
                        companies(https://github.com/kaacuna20/webscraping-construction-companies)">"web_scrapping_database</a>", save the sensible information in enviroment variables.
		</p>
	</li>
</ol>
