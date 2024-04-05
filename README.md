# MundoTextil

## Igmhar Augusto Sanchez Canales 

### Video Demo: 

### General idea: Web Application Created for a Textile Fabric of Robes. Designed to make it easier for the staff to register an order called "Release". Also since sometimes the fabric works on large databases, making a web application for more friendly user interface is better. Plus search and save valuable information on an easier way is always valuable to save time in every industry. The information is easily save with a relational database using SQLite3. This project was created using Python, Flask, Jinja Templating, HTML, JavaScript and CSS.

### Context:
I build this web app having in my mind a family business. On my family they have a **Textiles Fabric**, which takes order from across Mexico and ships them customize clothes, mainly robes. Since they need to ship to a lot of different locations taking orders became quite a tedious process. 

The employees or staff I've seen them register their orders in an non-automated way, which is on an Excel. Although Excel can handle a lot of information when it comes to finding information it has become tedious for them on this file. And also the staff has minimal knowledge on excel making it difficult to keep track of orders. 

Another problematic they face is that sometimes they do not register the orders on the excel so they lost track of certain orders, they do not know how to search important information on an excel file and since multiple staff members use the same excel it is quite tedious to pass the excel file via email. 

Therefore, with what I learned through the CS50 course, I decided to focus my final project on improving **Textile Releases Recording** in the industry, which focus on keeping track on the orders and register multiple type of order. 

Having this kind of data easily accessible on the industry makes process easier. Since the web app is able to found information of an order easily as it is with the date of the order or the name of the contact who made the order. Also in the industry having the data ordered is a huge deal to keep track of how much needs to produce or how much fabric needs to be ordered to produce the robes. It's important to mention that this idea can be implemented into ANY type of enterprise that needs to keep track of certain orders, in this case I made it personalized to the Fabric called MUNDO TEXTIL, but with minor changes or adaptations can be used in different types.  
On this project I will referred to release as the name of every order since the company calls it by this name, ex. This form takes the data of the release. 

Clarification: The page is written in Spanish since I make it for the use or the purpose of the company to use it furthermore, and since the staff members have everything in Spanish of the information and is their native speaking language I decided to make it so the user interfaces is in Spanish, but the documentation will be all in English.  
### Implementation Details
#### Database
The first thing I did was to create my database called `textil.db`. This is a Relational Database with 3 tables: `users, textile_releases and color_quantities`. The textile_releases table **references** the other tables being the central table of the database. This table records the details of textile releases. Each entry includes information such as the `release id`, `planta_key` (indicating the specific plant or location associated with the release), contact details (`telefono_contacto`, `nombre_contacto`), address information (`domicilio`, `ciudad`, `municipio_estado`, `codigo_postal`), the `prendas_solicitadas` (number of garments requested), the release `fecha` (date), a **reference** to the `user_id` of the responsible user, and the current `status` of the release. This table effectively links the operational aspects of textile releases with user management and oversight.

The color_quantities table stores detailed records on the quantities of textiles by `color` and `size` for each release. Each record is uniquely identified by an `id` and links back to the textile_release_id.  

Lastly the "users" table is used to register the users who have access to the system as well as their *hashed* passwords (which were created with a python function from the library *werkzeug.security*).

Here is the diagram that explains how the tables are related as well as the attributes of each table:

#### Templates

Then, I created the `/templates` folder inside my project. Which was composed of all of the HTML files that were going to be accessed in each of my routes. `/templates` has 9 HTML files in total, each will be explained in the following segment: 

- `layout.html`: This is the skeleton of the whole web application. It contains a ***NavBar*** with some *Jinja* logic that displays different elements in which the user can navigate. The *jinja* logic helps display **LogIn** and **Register** if the user is not logged in, and in case the user is logged in, it displays 6 options: **Logo, Capture, Colors, Search Color, Search Release** (which is a dropdown menu divided into Search by Date, by Name and by ID) and finally the **Log Out** option. This layout will be *extended* onto every other HTML file with *Jinja* so that only the body can be modified and every option can be accessed at all times. At the bottom I put a small footer that contains information of development of me. 
![relational_model](https://github.com/Vizard16/CS50-Final-project/blob/master/screenshots/Layout.png)
- `login.html`: The login page consists of a form with 2 inputs, a text input where the username needs to be the input, and a password input where the user types its password. If the input is correct, it queries the database and gets the user and password, and if they match, logs the user in automatically and allows them to use the app's functions. If they do not match it will redirect to the same page with an alert saying what was the issue. The page looks like the following: 
![relational_model](https://github.com/Vizard16/CS50-Final-project/blob/master/screenshots/LogIn.png )
- `register.html`: The template is almost identical to `login.html`, only that it contains a form with 3 inputs: a username input, and two password inputs which means the input will be censored with "*" (one of them sets the password and the second one is used to confirm the password). If the passwords don't match **or** the username is already in existence, a *flash alert* is displayed. If the input is correct, it inserts the data into the database and immediately logs the user in. It is shown on the following image: 
![relational_model](https://github.com/Vizard16/CS50-Final-project/blob/master/screenshots/Register.png)
- `index.html`: This template is the first that the user sees when they log in or register. It displays a *Welcome* message and a table of the most recent orders that have been registered. This table was created with Jinja Templating, using a loop that iterates through every element of a **SQL** query containing every study made throughout time. The table shows the ID of the release order, the plant's key, the data of the localization that will be shipped, Contact Phone, Name of the contact, the number of the ordered clothes, the date of the order, the status of the order and a button for deleting each order. The status its a dropdown menu which contains In Process status or Delivered, which it's changed here and changed on the database. This was made using JQuery methods on a JavaScript script inside the HTML file. The delete button sends a request by using AJAX to the flask app. This is what it looks like. 

- `release.html`: The release template is the file used to POST a new release into the database. This was develop as a submit form as in any type of webpage. There are information previously said that needs to be POST each time an order is register. What makes it different is that it was develop using JQuery JavaScript to make a cloneable section so that the user can add more clothes to the order of different colors, sizes to whatever the user needs. Also it has a counter so that the user can see if the total matches the pre registered total amount of clothes they ordered. If it doesn't match I made using AJAX to send a POST to handle a flash that says that they don't match. All fields needs to be required in order to submit the form. And finally, a Submit Button that triggers the insertion into the database as long as the input data is correct. This what it looks like: 

- `colors.html`: This file is used as a GET method to see the part of the colors and sizes of the color_quantities **TABLE** which is used using a JINJA, using a loop that iterates through every element of the database. It also is accommodated in a table type so the user can see the release and associate with the index table and see the amount of clothes ordered by size and color easily. Here is how it looks like: 
![relational_model]()
- `search_colors.html`: The search method is to having a text input on top of the page that whenever I put an ID on the input it will dynamically display a table just like in `colors.html` without the need of refreshing the page where it shows the ID and colors of the table or the information. This was done with ***JavaScript*** and a *** JSON *** format of data, the *innerHTML*.  
![relational_model]()
- `search_date.html`: The search files all work quite in the same way. In this case, the template has a **date** input which dynamically displays a table just like in `index.html` without the need of refreshing the page. With some ***JavaScript*** and a *** JSON *** format of data, the *innerHTML* of the table's body is modified so that its value is updated depending on the user's input.
![relational_model]()
- `search_name.html`: Similar to lasts templates, *`search_name.html`* has a text input which uses ***JavaScript*** and a *** JSON *** format of data, updates the contents of the table (modifying the innerHTML) according to what the user types in. It looks like this initially:
![relational_model]()
Now if the user types **ANY letter**, as long as it is inside the name of any of the doctors, the data will change dynamically:
![relational_model]()
- `search_id.html`: This works like the `search_colors.html`, only instead of making a query on the color database it makes on the textile release database. It works with the same ***JavaScript*** and a *** JSON ***  method. It looks like this:
![relational_model]()
#### Design decisions
The color design was focused only on what I think more of the identity of the company and since they say that the main color of robes they receive is gray I decided to make it gray but a gray getting close to blue to not look sad. I created a `/static` folder which contains the `styles.css` file and a `/favicon.ico` icon of the **Globe Logo** which since the company is named MUNDO TEXTIL and the translation of TEXTILE WORLD I put the following logo. 
![relational_model]()

#### Backend Functionality
The backend functionality is made using Flask in Python. The Python code is divided into two files:
- `app.py`: Establishes the necessary routes for the application to work properly. **ALMOST** every route works with both a **POST** and a **GET** method for almots all of the methods. The **POST** method is mainly used to insert data into the database, obtaining data from the form using the function `request.form.get()`. I made completely sure that every single input is filled in before *posting*. In fact, if the user were to misinput, *flash* error messages appear on the screen. Finally, with the **GET** method we can render our template and connect variables between python and the HTML file. This file contains the **whole functionality** of the application.

- `functions.py`: Simply contains the function `login_required()` which is imported into `app.py` and helps us ensure that certain routes are only available to the user if they're logged in.
    ##### Routes
    - /: Home page displaying textile releases.
    - /login: Login page for users.
    - /register: Registration page for new users.
    - /logout: Route to log out the current user.
    - /release: Page to create new textile releases.
    - /colors: Page to view color quantities for each textile release.
    - /search_date: Page to search for textile releases by date.
    - /search_name: Page to search for textile releases by name.
    - /search_id: Page to search for textile releases by ID.
    - /search_colors: Page to search for textile releases by colors.


#### Further Development
For the further development of this page I have planed to have more types of search. And also the company of mundo textile not only has robes on the inventory, so implementing to all the available catalogue would be great for them, but since robes is the main product for now is enough. Also I belive there is a lot of area of opportunities to make the design better. So knowing more about UX/UI design is one of the purpouses for further development. 

#### Final Thoughts 
Mundo Textil web page is meant to have an impactful meaning results on the company. While it was made for automate a simple task as it is registering on an Excel some data, this will save time and help the staff members have a more visualization of the data. This can prevent for forgetting some orders or viewing the status of the orders in order to manage the textiles inventory if there is some orders and the textile is missing. The power of saving information easily makes productivity a lot better which is what this webpage is designed to achieve. 






#### ------------------------ created by Igmhar Sanchez Canales --------------------------------