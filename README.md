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

Lastly the "users" table is used to register the users who have access to the system as well as their *hashed* passwords (which were created with a python function from the library **werkzeug.security**).

Here is the diagram that explains how the tables are related as well as the attributes of each table:

#### Templates

Then, I created the `/templates` folder inside my project. Which was composed of all of the HTML files that were going to be accessed in each of my routes. `/templates` has 9 HTML files in total, each will be explained in the following segment: 

- `layout.html`:

- `login.html`:

- `register.html`:

- `index.html`:

- `release.html`:

- `colors.html`:

- `search_colors.html`: 

- `search_date.html`: 

- `search_name.html`: 

- `search_id.html`: 

#### Design decisions
The color design was focused only on what I think more of the identity of the company and since they say that the main color of robes they receive is gray I decided to make it gray but a gray getting close to blue to not look sad. I created a `/static` folder which contains the `styles.css` file and a `/favicon.ico` icon of the **Globe Logo** which since the company is named MUNDO TEXTIL and the translation of 

#### Backend Functionality


#### Final Thoughts 






#### ---------------- created by Igmhar Sanchez Canales --------------------------------